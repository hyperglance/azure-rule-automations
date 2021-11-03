from azure.mgmt.network import NetworkManagementClient
from msrestazure.azure_cloud import Cloud

def hyperglance_automation(credential, resource: dict, cloud = Cloud, automation_params = ''):
  url = cloud.endpoints.resource_manager
  client = NetworkManagementClient(credential, resource['subscription'], base_url=url, credential_scopes=[url + '/.default']) # subscription id
  client.network_interfaces.begin_delete(resource['attributes']['Resource Group'], resource['name']) 

def info() -> dict:
  INFO = {
    "displayName": "Delete NIC",
    "description": "Deletes a network interface",
    "resourceTypes": [
      "Network Interface"
    ],
    "params": [

    ],
    "roles": [ 
      
    ]
  }

  return INFO