def hyperglance_automation(credential, resource: dict, cloud, automation_params = ''):
  from azure.mgmt.compute import ComputeManagementClient
  from azure.mgmt.network import NetworkManagementClient


  url = cloud.endpoints.resource_manager
  compute_client = ComputeManagementClient(credential, resource['subscription'], base_url=url, credential_scopes=[url + '/.default']) 
  network_client = NetworkManagementClient(credential, resource['subscription'], base_url=url, credential_scopes=[url + '/.default'])
  
  vm = compute_client.virtual_machines.get(resource['attributes']['Resource Group'], resource['name'])
  compute_client.virtual_machines.begin_delete(resource['attributes']['Resource Group'], resource['name'])
  if automation_params["Delete Associated Resources"] == True:
    delete_resources(compute_client, network_client, vm)

def delete_resources(compute_client, network_client, vm):
  network_interfaces = vm.network_profile.network_interfaces
  for nic in network_interfaces:
    nic_resource_group = nic.id.split('/')[4]
    nic_name = nic.id.split('/')[8]
    for config in network_client.network_interfaces.get(nic_resource_group, nic_name).ip_configurations:
      ip_resource_group = config.public_ip_address.id.split('/')[4]
      ip_name = config.public_ip_address.id.split('/')[8]
    network_client.network_interfaces.begin_delete(nic_resource_group, nic_name)
  os_disk = vm.storage_profile.os_disk.managed_disk
  compute_client.disks.begin_delete(os_disk.id.split('/')[4], os_disk.id.split('/')[8]) 
  data_disks = vm.storage_profile.data_disks
  for disk in data_disks:
    resource_group = disk.managed_disk.id.split('/')[4]
    name = disk.managed_disk.id.split('/')[8]
    compute_client.disks.begin_delete(resource_group, name) 
  



def info() -> dict:
  INFO = {
    "displayName": "Delete VM",
    "description": "Delete a Virtual Machine",
    "resourceTypes": [
      "Virtual Machine"
    ],
    "params": [
      {
        "name": "Delete Associated Resources",
        "type":"boolean",
        "default":"false"
      }

    ],
    "permissions": [
      "Microsoft.Compute/virtualMachines/delete"
    ]
  }

  return INFO