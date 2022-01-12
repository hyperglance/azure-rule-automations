def hyperglance_automation(credential, resource: dict, cloud, automation_params = '', **kwargs):
  from azure.mgmt.resource import ResourceManagementClient

  url = cloud.endpoints.resource_manager
  client = ResourceManagementClient(credential, resource['subscription'], base_url=url, credential_scopes=[url + '/.default']) # subscription id
  client.resource_groups.begin_delete(resource['attributes']['Resource Group'])


def info() -> dict:
  INFO = {
    "displayName": "Delete Resource Group",
    "description": "Deletes a Resource Group",
    "resourceTypes": [
      "Virtual Machine",
      "Virtual Network",
      "Disk",
      "Storage Account",
      "Subnet",
      "Public IP Address",
      "Network Interface",
      "Function App",
      "Logic App",
      "Event Grid Topic"
    ],
    "params": [

    ],
    "permissions": [ 
      "Microsoft.Resources/subscriptions/resourcegroups/delete"
    ]
  }

  return INFO