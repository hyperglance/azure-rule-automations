import logging
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os
import json

logger = logging.getLogger()

def upload_outputs(index, report: dict, report_prefix: str):
    automation_name = report["name"]
    num_successful = len(report["processed"])
    num_errored = len(report["errored"])
    total = num_successful + num_errored
    # do not add .json extension - this gives infinite recursion
    report_name = f"report_{automation_name}_total({total})_success({num_successful})_error({num_errored})_{index}" 
    try:
        blob_service_client = BlobServiceClient.from_connection_string(
            os.environ["hyperglanceautomations_STORAGE"]
        )
        blob_client = blob_service_client.get_blob_client(
            container="hyperglance-automations",
            blob="".join([report_prefix, report_name]),
        )
        blob_client.upload_blob(json.dumps(report), overwrite=True)
    except Exception as e:
        logger.error(e)

def put_pending_status(prefix: str):
    blob_service_client = BlobServiceClient.from_connection_string(os.environ["hyperglanceautomations_STORAGE"])
    blob_client = blob_service_client.get_blob_client(
            container="hyperglance-automations",
            blob="".join([prefix, 'is_pending']),
    )
    blob_client.upload_blob('', overwrite=True)

def remove_pending_status(prefix: str):
    blob_service_client = BlobServiceClient.from_connection_string(os.environ["hyperglanceautomations_STORAGE"])
    blob_client = blob_service_client.get_blob_client(
            container="hyperglance-automations",
            blob="".join([prefix, 'is_pending']),
    )
    blob_client.delete_blob()

def map_prefix(event_name: str) -> str:
    parts = event_name.split('/')
    return parts[1] + '/' + 'reports' + '/' + parts[3] + '/' + parts[4] + '/'