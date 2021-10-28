from msrestazure.azure_cloud import Cloud
import hyperglance_automations.processing.tagging as tagging


def hyperglance_automation(credential, resource: dict, cloud:Cloud, automation_params = ''):
    tagging.add_tag(
      credential,
      resource,
      cloud,
      automation_params['Key'],
      automation_params['Value']
    )

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
    "roles": [
    ]
  }

  return INFO