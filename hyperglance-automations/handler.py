import azure.functions as func
import json
import importlib
import logging

logger = logging.getLogger()


def main(eventBlob: func.InputStream):
    payload = json.loads(eventBlob.read().decode('utf-8'))
    outputs = []
    process_event(payload, outputs) # do something with outputs. I also need creds.

def execute_on_resource(credentials, automation_to_execute, resource, action_params):
    ## Grab the account and region (some resources don't have a region, default to us-east-1)
    automation_account_id = resource["account"]
    # look at arn not region - s3 does not have a region

    ## Run the automation!
    automation_to_execute.hyperglance_automation(credentials, resource, action_params)


def process_event(automation_data, outputs):
    ## For each chunk of results, execute the automation
    credential = DefaultAzureCredential() # please can I do things azure? configure in identity in function app.
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
            automation_to_execute = importlib.import_module(
                "".join(["automations.", automation_name]), package=None
            )
        except:
            msg = "Unable to find or load an automation called: %s" % automation_name
            automation["critical_error"] = msg
            return

        ## For each of Resource, execute the automation
        for resource in resources:
            try:
                action_params = automation.get("params", {})

                automation_to_execute_output = execute_on_resource(
                    credential,
                    automation_to_execute,
                    resource,
                    action_params
                )
                automation["processed"].append(resource)

            except Exception as err:
                resource["error"] = str(err)  # augment resource with an error field
                automation["errored"].append(resource)
    