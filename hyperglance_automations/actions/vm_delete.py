from azure.mgmt.compute import ComputeManagementClient

def hyperglance_automation(credential, resource: dict, automation_params = ''):
    client = ComputeManagementClient(credential, resource['subscription']) # subscription id
    client.virtual_machines.begin_delete(resource['attributes']['Resource Group'], resource['attributes']['Computer Name'])


def info() -> dict:
  INFO = {
    "displayName": "Delete VM",
    "description": "Delete a Virtual Machine",
    "resourceTypes": [
      "Virtual Machine"
    ],
    "params": [

    ],
    "permissions": [
    ]
  }

  return INFO