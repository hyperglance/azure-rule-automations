import asyncio

async def hyperglance_automation(credential, resource: dict, cloud, automation_params = ''):
  from azure.mgmt.compute import ComputeManagementClient 
  
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