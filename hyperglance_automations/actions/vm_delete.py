def hyperglance_automation(credential, resource: dict, cloud, automation_params = ''):
  from azure.mgmt.compute import ComputeManagementClient
  from azure.mgmt.network import NetworkManagementClient


  url = cloud.endpoints.resource_manager
  compute_client = ComputeManagementClient(credential, resource['subscription'], base_url=url, credential_scopes=[url + '/.default']) 
  network_client = NetworkManagementClient(credential, resource['subscription'], base_url=url, credential_scopes=[url + '/.default'])
  
  vm = compute_client.virtual_machines.get(resource['attributes']['Resource Group'], resource['name'])  
  if automation_params["Delete Associated Resources"] == 'true':
      ip_configs = []
      os_disk = vm.storage_profile.os_disk.managed_disk
      data_disks = vm.storage_profile.data_disks
      network_interfaces = vm.network_profile.network_interfaces
      for nic in network_interfaces:
        ip_configs.extend(network_client.network_interfaces.get(nic.id.split('/')[4], nic.id.split('/')[8]).ip_configurations)
  process = compute_client.virtual_machines.begin_delete(resource['attributes']['Resource Group'], resource['name'])
  process.wait(300) # timeout after 300 seconds
  if automation_params["Delete Associated Resources"] == 'true':
    for nic in network_interfaces:
      process = network_client.network_interfaces.begin_delete(nic.id.split('/')[4], nic.id.split('/')[8])
      process.wait(300)
    for config in ip_configs:
      if config.public_ip_address == None:
        continue
      ip_resource_group = config.public_ip_address.id.split('/')[4]
      ip_name = config.public_ip_address.id.split('/')[8]
      network_client.public_ip_addresses.begin_delete(ip_resource_group, ip_name)
    compute_client.disks.begin_delete(os_disk.id.split('/')[4], os_disk.id.split('/')[8]) 
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
      "Microsoft.Compute/virtualMachines/delete",
      "Microsoft.Compute/virtualMachines/read"
    ]
  }

  return INFO