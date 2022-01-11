import asyncio

async def hyperglance_automation(credential, resource: dict, cloud, automation_params = '', **kwargs):
  from azure.mgmt.compute import ComputeManagementClient
  
  url = cloud.endpoints.resource_manager
  client = ComputeManagementClient(credential, resource['subscription'], base_url=url, credential_scopes=[url + '/.default']) # subscription id
  client.virtual_machines.begin_power_off(resource['attributes']['Resource Group'], resource['name'])

def info() -> dict:
  INFO = {
    "displayName": "Power Off",
    "description": "Powers Off (Pauses) a Virtual Machine. Charges are still incurred for allocated resources such as IP addresses",
    "resourceTypes": [
      "Virtual Machine"
    ],
    "params": [

    ],
    "permissions": [
      "Microsoft.Compute/virtualMachines/powerOff/action"
    ]
  }

  return INFO