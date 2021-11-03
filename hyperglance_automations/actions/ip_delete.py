from azure.mgmt.network import NetworkManagementClient
from msrestazure.azure_cloud import Cloud

def hyperglance_automation(credential, resource: dict, cloud = Cloud, automation_params = ''):
  url = cloud.endpoints.resource_manager
  client = NetworkManagementClient(credential, resource['subscription'], base_url=url, credential_scopes=[url + '/.default']) # subscription id
  client.public_ip_addresses.begin_delete(resource['attributes']['Resource Group'], resource['name']) 

def info() -> dict:
  INFO = {
    "displayName": "Delete Public IP",
    "description": "Deletes a public IP address",
    "resourceTypes": [
      "Public IP Address"
    ],
    "params": [

    ],
    "roles": [ 
      
    ]
  }

  return INFO