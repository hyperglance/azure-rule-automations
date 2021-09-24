import azure.functions as func
import azure.identity as identity
import json
import logging
import hyperglance_automations.processing as processing
import hyperglance_automations.storage_utils as storage

logger = logging.getLogger()
 

def main(eventBlob: func.InputStream):
    logger.info("fetching credentials from azure")
    # Environment variables (Function App -> Settings -> Configuration -> Application Settings) 
    # {AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET}
    # or identity (Function App -> Identity) must be used to authenticate.
    credential = identity.DefaultAzureCredential() 

    payload = json.loads(eventBlob.read().decode('utf-8'))
    outputs = []
    blob_prefix = storage.map_prefix(eventBlob.name)
    try:
        storage.put_pending_status(blob_prefix)
        processing.process_event(credential, payload, outputs) 
    except Exception as e:
        outputs.append({'name':'critical_error', 'processed':[], 'errored':[], 'critical_error': str(e)})
    finally:
        for index, output in enumerate(outputs):
            storage.upload_outputs(index, output, blob_prefix)
        storage.remove_pending_status(blob_prefix)
    