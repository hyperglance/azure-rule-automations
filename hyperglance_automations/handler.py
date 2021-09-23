import azure.functions as func
import azure.identity as identity
import json
import logging
import hyperglance_automations.processing as processing

logger = logging.getLogger()
 

def main(eventBlob: func.InputStream):
    logger.info("fetching credentials from azure")
    # Environment variables (Function App -> Settings -> Configuration -> Application Settings) 
    # {AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET}
    # or identity (Function App -> Identity) must be used to authenticate.
    credential = identity.DefaultAzureCredential() 

    payload = json.loads(eventBlob.read().decode('utf-8'))
    outputs = []
    blob_key = eventBlob.name
    report_key_prefix = '/'.join(blob_key.split('/')[0:-1]).replace('/events/', '/reports/') + '/'
    
    try:
        processing.process_event(payload, outputs) 
    except Exception as e:
        outputs.extend({'name':'critical_error', 'processed':[], 'errored':[], 'critical_error': ''})
    finally:
        for index, output in enumerate(outputs):
            processing.upload_outputs(index, output, report_key_prefix)
    