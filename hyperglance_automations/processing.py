import importlib
import logging
import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

logger = logging.getLogger()

def process_event(credential, automation_data, outputs):    
    for chunk in automation_data["results"]:
        if not "automation" in chunk:
            continue
        resources = chunk["entities"]
        automation = chunk["automation"]
        automation_name = automation["name"]

        ## Augment the automation dict to track errors and add to the output, this gets reported back to Hyperglance
        automation["processed"] = []
        automation["errored"] = []
        automation["critical_error"] = None
        outputs.append(automation)

        ## Dynamically load the module that will handle this automation
        try:
            automation_to_execute = importlib.import_module(''.join(['hyperglance-automations.', 'actions.', automation_name]))
        except Exception as e:
            logger.error(str(e))
            msg = "Unable to find or load an automation called: %s" % automation_name
            automation["critical_error"] = msg
            return

        ## For each of Resource, execute the automation
        for resource in resources:
            try:
                action_params = automation.get("params", {})
                logger.info('resource ' + str(resource))
                logger.info('action params ' + str(action_params))
                logger.info('automation to execute ' + str(automation_to_execute))

                automation_to_execute.hyperglance_automation(credential, resource, action_params)
                automation["processed"].append(resource)

            except Exception as err:
                logger.info(err)
                resource["error"] = str(err)  # augment resource with an error field
                automation["errored"].append(resource)

def upload_outputs(index, report: dict, report_prefix: str):
  all_resources = report['processed'] + report['errored']
  automation_name = report['name']
  num_successful = len(report['processed'])
  num_errored = len(report['errored'])
  total = num_successful + num_errored
  report_name = f'report_{automation_name}_total({total})_success({num_successful})_error({num_errored})_{index}.json'
  try:
        blob_service_client = BlobServiceClient.from_connection_string(os.environ['hyperglanceautomations_STORAGE'])
        blob_client = blob_service_client.get_blob_client(
            container='hyperglance-automations',
            blob=''.join([report_prefix, report_name]))
        blob_client.upload_blob(str(report))
  except Exception as e:
        logger.error(e)
    