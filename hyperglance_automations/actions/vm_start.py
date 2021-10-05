from azure.mgmt.compute import ComputeManagementClient

def hyperglance_automation(credential, resource: dict, automation_params = ''):
    client = ComputeManagementClient(credential, resource['subscription']) # subscription id
    client.virtual_machines.begin_start(resource['attributes']['Resource Group'], resource['name']) 

def info() -> dict:
  INFO = {
    "displayName": "Start VM",
    "description": "Start a Virtual Machine",
    "resourceTypes": [
      "Virtual Machine"
    ],
    "params": [

    ],
    "roles": [ 
      "Virtual Machine Contributor"
    ]
  }

  return INFO