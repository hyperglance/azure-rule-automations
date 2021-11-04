def hyperglance_automation(credential, resource: dict, cloud: Cloud, automation_params = ''):
  from azure.mgmt.compute import ComputeManagementClient

  url = cloud.endpoints.resource_manager
  client = ComputeManagementClient(credential, resource['subscription'], base_url=url, credential_scopes=[url + '/.default']) # subscription id
  client.virtual_machines.begin_power_off(resource['attributes']['Resource Group'], resource['name'])

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