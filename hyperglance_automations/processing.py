import importlib
import logging
from time import perf_counter
import azure.identity as identity
from msrestazure.azure_cloud import *
import os
from pathlib import Path
import json
from multiprocessing import Pool

logger = logging.getLogger()

def worker(resources, automation_name, action_params, time_limit, time_elapsed):
    # Report object to return
    report = {
        "processed": [],
        "errored": [],
        "critical_error": None
    }

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

    ## Dynamically load the module that will handle this automation
    try:
        automation_to_execute = importlib.import_module(
            "".join(["hyperglance_automations.", "actions.", automation_name])
        )
    except Exception as e:
        logger.exception(e)
        msg = "Unable to find or load an automation called: %s" % automation_name
        report["critical_error"] = msg
        return report

    ## For each of Resource, execute the automation
    for resource in resources:
        if time_elapsed > time_limit:
            logger.info("time limit exceeded for " + str(resource))
            resource["error"] = \
            "The time limit for the action has surpassed. Consider changing your function app service plan. https://docs.microsoft.com/en-us/azure/app-service/app-service-plan-manage"
            report['errored'].append(resource)
            continue

        before = perf_counter()
        try:
            automation_to_execute.hyperglance_automation(credential, resource, cloud, action_params)
            logger.info(f'resource: {resource} processed successfully')
            report["processed"].append(resource)
        except Exception as err:
            logger.exception(err)
            resource["error"] = str(err)  # augment resource with an error field
            report["errored"].append(resource)
        finally:
            time_elapsed += (perf_counter()-before)
    
    return report


def process_event(automation_data, outputs):
    time_elapsed = 0.0
    concurrency_limit = get_concurrency_limit()
    # time limits so we don't run for longer than the Azure function execution limit
    time_limit = get_time_limit()
    logger.info(f'processing new event with time limit {time_limit} and concurrency limit {concurrency_limit}')
    for chunk in automation_data["results"]:
        if not "automation" in chunk:
            continue
        
        resources = chunk["entities"]
        automation = chunk["automation"]
        automation_name = automation["name"]
        resource_type = chunk['entityType']
        action_params = automation.get("params", {})

        logger.info(f'running {automation_name} for {len(resources)} resources of type {resource_type}')
        
        # Calc pool size
    
        pool_size = max(1, min(len(resources), concurrency_limit))

        logger.info(f'pool size : {pool_size}')

        # Divide the resources into batches for full pool utilisation
        batch_size = max(1, len(resources) // pool_size)

        logger.info(f'batch size : {batch_size}')

        resource_batches = (resources[i:i + batch_size] for i in range(0, len(resources), batch_size))

        # Mix in other args to supply to the worker func
        batches_args = ([
            resource_batch,
            automation_name,
            action_params,
            time_limit,
            time_elapsed
        ] for resource_batch in resource_batches)

        # Run work on process pool, blocks until complete
        with Pool(processes=pool_size) as pool:
            results = pool.starmap(worker, batches_args, 1)

        ## Augment the automation dict to track errors and add to the output, this gets reported back to Hyperglance
        critical_error_msg = "\n".join((r["critical_error"] for r in results if r["critical_error"] is not None)).strip()
        automation["critical_error"] = critical_error_msg if critical_error_msg else None
        automation["processed"] = [resource['processed'] for resource in results for resource['processed'] in resource['processed']]
        automation["errored"] = [resource['errored'] for resource in results for resource['errored'] in resource['errored']]
        outputs.append(automation)

def get_time_limit():
    host_file = Path(__file__).resolve().parents[0].joinpath('host.json')
    try:
        with open(host_file) as file:
            string_value = json.loads(file.read())['functionTimeout']
        constituents = string_value.split(':')
        time_limit = (60*60*int(constituents[0]))+(60*int(constituents[1]))+int(constituents[2])
    except Exception as e:
        logger.exception(e)
        time_limit = 480 # 8 minutes default value
    finally:
       return time_limit - 120 # return the time limit with a 2 minute safty buffer

       
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





