from azure.mgmt.compute import ComputeManagementClient
from msrestazure.azure_cloud import Cloud

def hyperglance_automation(credential, resource: dict, cloud:Cloud, automation_params = ''):
  url = cloud.endpoints.resource_manager
  client = ComputeManagementClient(credential, resource['subscription'], base_url=url, credential_scopes=[url + '/.default']) # subscription id
  client.virtual_machines.begin_deallocate(resource['attributes']['Resource Group'], resource['name']) # crendentials and client config to be added

def info() -> dict:
  INFO = {
    "displayName": "Stop (Deallocate) VM",
    "description": "Shuts down the virtual machine and releases the compute resources. Charges are no longer incurred by this VM",
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