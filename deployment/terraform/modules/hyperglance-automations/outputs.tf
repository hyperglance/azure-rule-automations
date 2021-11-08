output "storage_account_resource_id" {
  description = "Enter this value into your Hyperglance installation under Automations > Azure > Storage Account Resource ID"
  value       = azurerm_storage_account.hyperglance-automations-storage-account.id
}



