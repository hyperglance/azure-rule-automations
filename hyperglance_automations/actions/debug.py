import time

def hyperglance_automation(credential, resource: dict, cloud, automation_params = ''):
  time.sleep(500)

def info() -> dict:
  INFO = {
    "displayName": "DEBUG",
    "description": "Remove a tag from a resource",
    "resourceTypes": [
      "Virtual Machine" 
    ],
    "params": [
      {
        "name": "Key",
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