from azure.mgmt.compute import ComputeManagementClient
from msrestazure.azure_cloud import Cloud

def hyperglance_automation(credential, resource: dict, cloud = Cloud, automation_params = ''):
  url = cloud.endpoints.resource_manager
  client = ComputeManagementClient(credential, resource['subscription'], base_url=url, credential_scopes=[url + '/.default']) # subscription id
  client.disks.begin_delete(resource['attributes']['Resource Group'], resource['name']) 

def info() -> dict:
  INFO = {
    "displayName": "Delete Disk",
    "description": "Deletes a disk. Disks attached to Virtual Machines will not be deleted - these must be detached first",
    "resourceTypes": [
      "Disk"
    ],
    "params": [

    ],
    "permissions": [ 
      "Microsoft.Compute/disks/delete",
    ]
  }

  return INFO