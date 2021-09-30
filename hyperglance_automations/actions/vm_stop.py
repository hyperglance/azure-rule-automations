from azure.mgmt.compute import ComputeManagementClient

def hyperglance_automation( credential, resource: dict, automation_params = ''):
    client = ComputeManagementClient(credential, resource['subscription']) # subscription id
    client.virtual_machines.begin_power_off(resource['attributes']['Resource Group'], resource['attributes']['computer name']) # crendentials and client config to be added

def info() -> dict:
  INFO = {
    "displayName": "Stop VM",
    "description": "Stop a Virtual Machine",
    "resourceTypes": [
      "Virtual Machine"
    ],
    "params": [

    ],
    "permissions": [
      
    ]
  }

  return INFO