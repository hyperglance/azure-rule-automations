import time

def hyperglance_automation(credential, resource: dict, cloud, automation_params = ''):
  for i in range(300): 
      time.sleep(1)


def info() -> dict:
  INFO = {
    "displayName": "Dummy",
    "description": "",
    "resourceTypes": [
      "Virtual Machine"
    ],
    "params": [

    ],
    "permissions": [ 
      "Microsoft.Compute/disks/delete",
    ]
  }

  return INFO