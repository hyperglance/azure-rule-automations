import azure.functions as func
import azure.identity as identity
import json
import importlib
import logging

logger = logging.getLogger()
 

def main(eventBlob: func.InputStream):
    payload = json.loads(eventBlob.read().decode('utf-8'))
    outputs = []
    process_event(payload, outputs) 


def process_event(automation_data, outputs):    
   
    # Environment variables (Function App -> Settings -> Configuration -> Application Settings)
    # or identity (Function App -> Identity) must be used to authenticate.
    credential = identity.DefaultAzureCredential() 
    
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
    