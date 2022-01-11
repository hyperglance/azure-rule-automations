import asyncio

async def hyperglance_automation(credential, resource: dict, cloud, automation_params = '', **kwargs):
    from azure.mgmt.resource.resources import ResourceManagementClient

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
    "displayName": "Add Tag",
    "description": "Adds a tag to a resource",
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
      "Microsoft.Resources/tags/read",
      "Microsoft.Resources/tags/write"
    ]
  }

  return INFO