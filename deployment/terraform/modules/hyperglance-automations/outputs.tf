output "storage_account_resource_id" {
  description = "Enter this value into your Hyperglance installation under Automations > Azure > Storage Account Resource ID"
  value       = azurerm_storage_account.hyperglance-automations-storage-account.id
}

output "func-command" {
  description = "Command to deploy function code"
  value       = "func azure functionapp publish ${azurerm_function_app.hyperglance-automations-app.name}"
}

