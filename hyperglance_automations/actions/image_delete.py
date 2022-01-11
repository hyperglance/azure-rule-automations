import asyncio

async def hyperglance_automation(credential, resource: dict, cloud, automation_params = '', **kwargs):
  from azure.mgmt.compute import ComputeManagementClient
  
  url = cloud.endpoints.resource_manager
  client = ComputeManagementClient(credential, resource['subscription'], base_url=url, credential_scopes=[url + '/.default']) # subscription id
  client.images.begin_delete(resource['attributes']['Resource Group'], resource['name'])



def info() -> dict:
  INFO = {
    "displayName": "Delete Image",
    "description": "Deletes an Image",
    "resourceTypes": [
      "Image"
    ],
    "params": [

    ],
    "permissions": [
      "Microsoft.Compute/images/delete"
    ]
  }

  return INFO