import asyncio

async def hyperglance_automation(credential, resource: dict, cloud, automation_params = ''):
  from azure.mgmt.compute import ComputeManagementClient

  url = cloud.endpoints.resource_manager
  client = ComputeManagementClient(credential, resource['subscription'], base_url=url, credential_scopes=[url + '/.default']) # subscription id
  client.ssh_public_keys.delete(resource['attributes']['Resource Group'], resource['name']) 

def info() -> dict:
  INFO = {
    "displayName": "Delete Public Key",
    "description": "Delete a SSH public key",
    "resourceTypes": [
      "SSH Public Key"
    ],
    "params": [

    ],
    "permissions": [ 
      "Microsoft.Compute/sshPublicKeys/delete"
    ]
  }

  return INFO