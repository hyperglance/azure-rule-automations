import azure.functions as func
import json
import hyperglance_automations.processing as processing
import hyperglance_automations.storage_utils as storage
import logging

logger = logging.getLogger()

def main(eventBlob: func.InputStream):
    payload = json.loads(eventBlob.read().decode('utf-8'))
    outputs = []
    blob_prefix = storage.map_prefix(eventBlob.name)
    try:
        storage.put_pending_status(blob_prefix)
        processing.process_event(payload, outputs) 
    except Exception as e:
        msg = f'Failed to process Rule automations. {e}'
        logger.exception(msg)
        
        # Report critical lambda failure back to Hyperglance
        # For now, we are doing this by creating a dummy automation report to convey the error message
        outputs.append({'name':'critical_error', 'processed':[], 'errored':[], 'critical_error': msg})
    finally:
        for index, output in enumerate(outputs):
            storage.upload_outputs(index, output, blob_prefix)
        storage.remove_pending_status(blob_prefix)
    