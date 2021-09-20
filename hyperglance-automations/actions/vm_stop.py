logger = logging.getLogger()

def hyperglance_automation( credential, resource: dict, automation_params = ''):
    logger.info('executing stop vm automation')
    client = ComputeManagementClient(credential, resource['subscription'])
    client.virtual_machines.begin_power_off(resource['attributes']['Resource Group'], resource['attributes']['Computer Name']) # crendentials and client config to be added

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