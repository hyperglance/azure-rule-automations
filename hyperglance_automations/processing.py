import importlib
import logging
import azure.identity as identity
from azure.identity import AzureAuthorityHosts
import os

logger = logging.getLogger()


def process_event(automation_data, outputs):
    credential = authenticate()
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
                "".join(["hyperglance_automations.", "actions.", automation_name])
            )
        except Exception as e:
            msg = "Unable to find or load an automation called: %s" % automation_name
            automation["critical_error"] = msg
            return

        ## For each of Resource, execute the automation
        for resource in resources:
            try:
                action_params = automation.get("params", {})
                automation_to_execute.hyperglance_automation(
                    credential, resource, action_params
                )
                automation["processed"].append(resource)

            except Exception as err:
                resource["error"] = str(err)  # augment resource with an error field
                automation["errored"].append(resource)

def authenticate() -> identity.DefaultAzureCredential:
    if('core.windows.net' in os.environ["hyperglanceautomations_STORAGE"]):
        environement = AzureAuthorityHosts.AZURE_PUBLIC_CLOUD
    elif('core.usgovcloudapi.net' in os.environ["hyperglanceautomations_STORAGE"]):
        environement = AzureAuthorityHosts.AZURE_GOVERNMENT
    else:
        raise Exception("the connection string endpoint suffix did not contain a valid value")
    # Environment variables (Function App -> Settings -> Configuration -> Application Settings) 
    # {AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET}
    # or identity (Function App -> Identity) must be used to authenticate.
    return identity.DefaultAzureCredential(authority=environement)    



