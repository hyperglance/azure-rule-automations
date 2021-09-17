

def hyperglance_automation(credential, resource: dict, automation_params = ''):
    client = ComputeManagementClient(credential, resource['subscription'], api_version=None, base_url=None, profile=<KnownProfiles.default: <azure.profiles.DefaultProfile object>>, **kwargs)
    client.virtual_machines.begin_delete(resource['attributes']['Resource Group'], resource['attributes']['Computer Name'])


def info() -> dict:
  INFO = {
    "displayName": "Delete VM",
    "description": "Delete a Virtual Machine",
    "resourceTypes": [
      "Virtual Machine"
    ],
    "params": [

    ],
    "permissions": [
    ]
  }

  return INFO