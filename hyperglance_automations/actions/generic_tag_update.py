from msrestazure.azure_cloud import Cloud
from azure.mgmt.resource.resources import ResourceManagementClient

def hyperglance_automation(credential, resource: dict, cloud:Cloud, automation_params = ''):
    pass
def info() -> dict:
  INFO = {
    "displayName": "Update Tag",
    "description": "Replaces a tag's key but retains its previous value",
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
    "roles": [
    ]
  }

  return INFO