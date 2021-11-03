from azure.mgmt.compute import ComputeManagementClient
from msrestazure.azure_cloud import Cloud

def hyperglance_automation(credential, resource: dict, cloud:Cloud, automation_params = ''):
  url = cloud.endpoints.resource_manager
  client = ComputeManagementClient(credential, resource['subscription'], base_url=url, credential_scopes=[url + '/.default']) # subscription id
  client.virtual_machines.begin_delete(resource['attributes']['Resource Group'], resource['name'])


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