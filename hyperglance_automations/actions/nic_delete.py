import asyncio

async def hyperglance_automation(credential, resource: dict, cloud, automation_params = '', **kwargs):
  from azure.mgmt.network import NetworkManagementClient

  url = cloud.endpoints.resource_manager
  client = NetworkManagementClient(credential, resource['subscription'], base_url=url, credential_scopes=[url + '/.default']) # subscription id
  client.network_interfaces.begin_delete(resource['attributes']['Resource Group'], resource['name'])



def info() -> dict:
  INFO = {
    "displayName": "Delete NIC",
    "description": "Deletes a Network Interface. Network Interfaces which are attached to a Virtual Machine will not be delete - these must be detached first",
    "resourceTypes": [
      "Network Interface"
    ],
    "params": [

    ],
    "permissions": [ 
      "Microsoft.Network/networkInterfaces/delete"
    ]
  }

  return INFO