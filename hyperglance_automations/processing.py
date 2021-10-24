import importlib
import azure.identity as identity
from msrestazure.azure_cloud import *
import os

def process_event(automation_data, outputs):
    #  TODO on a subscription (per group of subscriptions) basis when resources from hyper backend
    # 1. Have Environment user facing metadata
    # 2. Are grouped per subscription
    if('core.windows.net' in os.environ["hyperglanceautomations_STORAGE"]):
        cloud = AZURE_PUBLIC_CLOUD
    else:
        cloud = AZURE_US_GOV_CLOUD
    credential = authenticate(cloud)  
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
                "".join(["actions.", automation_name])
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
                    credential, resource, cloud, action_params
                )
                automation["processed"].append(resource)

            except Exception as err:
                resource["error"] = str(err)  # augment resource with an error field
                automation["errored"].append(resource)

def authenticate(cloud: Cloud) -> identity.DefaultAzureCredential:
    # Environment variables (Function App -> Settings -> Configuration -> Application Settings) 
    # {AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET}
    # or identity (Function App -> Identity) must be used to authenticate.
    return identity.DefaultAzureCredential(environment=cloud.endpoints.active_directory)    



