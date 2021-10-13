from azure.mgmt.compute import ComputeManagementClient

def hyperglance_automation(credential, resource: dict, automation_params = ''):
    client = ComputeManagementClient(credential, resource['subscription']) # subscription id
    client.images.begin_delete(resource['attributes']['Resource Group'], resource['name'])


def info() -> dict:
  INFO = {
    "displayName": "Delete Image",
    "description": "Deletes an Image",
    "resourceTypes": [
      "Image"
    ],
    "params": [

    ],
    "roles": [
        "Virtual Machine Contributor"
    ]
  }

  return INFO