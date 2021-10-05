output "storage_account_resource_id" {
  description = "Enter this value into your Hyperglance installation under Automations > Azure > Storage Account Resource ID"
  value       = module.hyperglance-automations.storage_account_resource_id
}

output "func-command" {
  description = "Command to deploy function code"
  value       = module.hyperglance-automations.func-command
}

