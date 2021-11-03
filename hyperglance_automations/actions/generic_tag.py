from msrestazure.azure_cloud import Cloud
from azure.mgmt.resource.resources import ResourceManagementClient


def hyperglance_automation(credential, resource: dict, cloud:Cloud, automation_params = ''):
    url = cloud.endpoints.resource_manager
    client = ResourceManagementClient(
        credential,
        resource['subscription'],
        base_url=url,
        credential_scopes=[url + '/.default']).tags
    previous = client.get_at_scope(resource['id'])
    appended = previous.properties.tags
    appended[automation_params['Key']] = automation_params['Value']
    tags = {'properties': {'tags' : appended}}
    client.create_or_update_at_scope(resource['id'], tags)

def info() -> dict:
  INFO = {
    "displayName": "Remove Tag",
    "description": "Removes a tag from a resource",
    "resourceTypes": [
      "Virtual Machine"
    ],
    "params": [
      {
        "name": "Key",
        "type": "string",
        "default": ""
      },
      {
        "name": "Value",
        "type": "string",
        "default": ""
      }
    ],
    "permissions": [
    ]
  }

  return INFO