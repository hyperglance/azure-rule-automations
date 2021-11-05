def hyperglance_automation(credential, resource: dict, cloud, automation_params = ''):
  from azure.mgmt.network import NetworkManagementClient

  url = cloud.endpoints.resource_manager
  client = NetworkManagementClient(credential, resource['subscription'], base_url=url, credential_scopes=[url + '/.default']) # subscription id
  client.public_ip_addresses.begin_delete(resource['attributes']['Resource Group'], resource['name']) 

def info() -> dict:
  INFO = {
    "displayName": "Delete Public IP",
    "description": "Deletes a public IP address. The IP Address must not be allocated to any resources",
    "resourceTypes": [
      "Public IP Address"
    ],
    "params": [

    ],
    "permissions": [ 
      "Microsoft.Network/publicIPAddresses/delete"
    ]
  }

  return INFO