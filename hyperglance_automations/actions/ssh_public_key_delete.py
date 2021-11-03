from azure.mgmt.compute import ComputeManagementClient
from msrestazure.azure_cloud import Cloud

def hyperglance_automation(credential, resource: dict, cloud = Cloud, automation_params = ''):
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
    "roles": [ 

    ]
  }

  return INFO