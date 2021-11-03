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
  previous_tags = previous.properties.tags
  placeholder = previous_tags[automation_params["Old Key"]]
  del previous_tags[automation_params['Old Key']]
  previous_tags[automation_params['New Key']] = placeholder
  tags = {'properties': {'tags' : previous_tags}}
  client.create_or_update_at_scope(resource['id'], tags)
    

def info() -> dict:
  INFO = {
    "displayName": "Update Tag",
    "description": "Replaces a tag's key but retains its previous value",
    "resourceTypes": [
      "Virtual Machine"
    ],
    "params": [
      {
        "name": "Old Key",
        "type": "string",
        "default": ""
      },
      {
        "name": "New Key",
        "type": "string",
        "default": ""
      }
    ],
    "permissions": [
      "Microsoft.Resources/tags/read",
      "Microsoft.Resources/tags/write"
    ]
  }

  return INFO