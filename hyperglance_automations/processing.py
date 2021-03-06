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

    event_loop = asyncio.get_event_loop()

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
        
        resource_map = {}

        ## For each of Resource, execute the automation
        for resource in resources:
            action_params = automation.get("params", {})
            resource['attributes']['Resource Group'] = resource['attributes']['Resource Group'].lower()

            task = event_loop.create_task(
                automation_to_execute.hyperglance_automation(
                    credential,
                    resource, 
                    cloud, 
                    action_params, 
                    start=perf_counter(), 
                    time_limit= get_time_limit()
                )
            )

            resource_map[task] = resource
                
    # nb. Use these deprecated methods instead of asyncio.all_tasks() and asyncio.current_task() for Azure's asyncio version
    pending = asyncio.tasks.Task.all_tasks() - {asyncio.Task.current_task()}
    try:
        await asyncio.gather(*pending)
    except Exception as e:
        pass # we will collect these separately

    for task in pending:
        resource = resource_map[task]
        problem = task.exception()
        if problem is None:
            automation['processed'].append(resource)
        else:
            resource['error'] = str(problem)
            automation['errored'].append(resource)

    


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





