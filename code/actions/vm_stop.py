

def hyperglance_automation( resource: dict, automation_params = ''):
    client = ComputeManagementClient(credential, subscription_id, api_version=None, base_url=None, profile=<KnownProfiles.default: <azure.profiles.DefaultProfile object>>, **kwargs)
    # vm name id (resource['id]) or resource['attributes']['Computer Name']?
    compute_client.virtual_machines.begin_power_off(GROUP_NAME, VM_NAME) # crendentials and client config to be added

def info() -> dict:
  INFO = {
    "displayName": "Stop VM",
    "description": "Stop a Virtual Machine",
    "resourceTypes": [
      "Virtual Machine"
    ],
    "params": [

    ],
    "permissions": [
      
    ]
  }

  return INFO