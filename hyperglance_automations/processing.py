import importlib
import logging
from time import perf_counter
import azure.identity as identity
from msrestazure.azure_cloud import *
import os
from pathlib import Path
import json
import asyncio

logger = logging.getLogger()

async def process_event(automation_data, outputs):

    #  TODO on a subscription (per group of subscriptions) basis when resources from hyper backend
    # 1. Have Environment user facing metadata
    # 2. Are grouped per subscription
    if('core.windows.net' in os.environ["hyperglanceautomations_STORAGE"]):
        cloud = AZURE_PUBLIC_CLOUD
    else:
        cloud = AZURE_US_GOV_CLOUD
    
    # Environment variables (Function App -> Settings -> Configuration -> Application Settings) 
    # {AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET}
    # or identity (Function App -> Identity) must be used to authenticate.
    credential = identity.DefaultAzureCredential(environment=cloud.endpoints.active_directory)    
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
            logger.info(e)
            msg = "Unable to find or load an automation called: %s" % automation_name
            automation["critical_error"] = msg
            return

        tasks = []

        ## For each of Resource, execute the automation
        for resource in resources:
            try:
                action_params = automation.get("params", {})
                
                tasks.append(
                    asyncio.create_task(
                        automation_to_execute.hyperglance_automation(
                            credential, resource, cloud, action_params
                        )
                    )
                )

                automation["processed"].append(resource)
            

            except Exception as err:
                logger.info(err)
                resource["error"] = str(err)  # augment resource with an error field
                automation["errored"].append(resource)
                automation["processed"].remove(resource)
        for task in tasks:
            await task
        


def get_concurrency_limit():
    default = 20
    config_file = Path(__file__).resolve().parents[0].joinpath('config.json')
    try:
        with open(config_file) as file:
            value = json.loads(file.read())['concurrent-processes']
    except Exception as e:
        logger.exception('there was a problem loading the config.json file: ' + str(e))
        return default
    return value

def get_time_limit():
    host_file = Path(__file__).resolve().parents[0].joinpath('host.json')
    try:
        with open(host_file) as file:
            string_value = json.loads(file.read())['functionTimeout']
        constituents = string_value.split(':')
        time_limit = (60*60*int(constituents[0]))+(60*int(constituents[1]))+int(constituents[2])
    except Exception as e:
        logger.info(e)
        time_limit = 480 # 8 minutes default value
    finally:
       return time_limit - 120 # return the time limit with a 2 minute safty buffer





