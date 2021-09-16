

def hyperglance_automation( resource: dict, automation_params = ''):
    client = ComputeManagementClient(credential, subscription_id, api_version=None, base_url=None, profile=<KnownProfiles.default: <azure.profiles.DefaultProfile object>>, **kwargs)
    compute_client.virtual_machines.begin_delete(GROUP_NAME, VM_NAME) # crendentials and client config to be added


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