from azure.mgmt.compute import ComputeManagementClient

def hyperglance_automation( credential, resource: dict, automation_params = ''):
    client = ComputeManagementClient(credential, resource['subscription']) # subscription id
    client.virtual_machines.begin_deallocate(resource['attributes']['Resource Group'], resource['name']) # crendentials and client config to be added

def info() -> dict:
  INFO = {
    "displayName": "Deallocate Virtual Machine",
    "description": "Shuts down the virtual machine and releases the compute resources. You are not billed for the compute resources that this virtual machine uses.",
    "resourceTypes": [
      "Virtual Machine"
    ],
    "params": [

    ],
    "roles": [
      "Virtual Machine Contributor"
    ]
  }

  return INFO