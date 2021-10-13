from azure.mgmt.compute import ComputeManagementClient

def hyperglance_automation( credential, resource: dict, automation_params = ''):
    client = ComputeManagementClient(credential, resource['subscription']) # subscription id
    client.virtual_machines.begin_power_off(resource['attributes']['Resource Group'], resource['name']) # crendentials and client config to be added

def info() -> dict:
  INFO = {
    "displayName": "Stop VM",
    "description": "Stops (Pauses) a Virtual Machine. Charges are still incurred for allocated resources such as IP addresses",
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