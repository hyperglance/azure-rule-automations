import azure.functions as func
import azure.identity as identity
import json
import logging
import hyperglance_automations.processing as processing
import hyperglance_automations.storage_utils as storage
from azure.identity import AzureAuthorityHosts

logger = logging.getLogger()
 

def main(eventBlob: func.InputStream):
    payload = json.loads(eventBlob.read().decode('utf-8'))
    outputs = []
    blob_prefix = storage.map_prefix(eventBlob.name)
    try:
        storage.put_pending_status(blob_prefix)
        processing.process_event(payload, outputs) 
    except Exception as e:
        outputs.append({'name':'critical_error', 'processed':[], 'errored':[], 'critical_error': str(e)})
    finally:
        for index, output in enumerate(outputs):
            storage.upload_outputs(index, output, blob_prefix)
        storage.remove_pending_status(blob_prefix)
    