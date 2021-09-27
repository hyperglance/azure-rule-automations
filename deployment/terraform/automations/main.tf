
resource "random_pet" "hyperglance-automations-name" {
  length    = 2
  prefix    = "hyperglance-automations"
  separator = "-"
}

resource "azurerm_function_app" "hyperglance-automations-app" {
  name                       = "hyperglance-automations-{random-pet.hyperglance-automations-name.id}"
  location                   = azurerm_resource_group.hyperglance-automations-resource-group.location
  resource_group_name        = azurerm_resource_group.example.name
  app_service_plan_id        = azurerm_app_service_plan.example.id 
  storage_account_name       = azurerm_storage_account.hyperglance-automations-storage-account.id
  storage_account_access_key = azurerm_storage_account.hyperglance-automations-storage-account.primary_access_key
}

resource "azurerm_resource_group" "hyperglance-automations-resource-group" {
  name     = "hyperglance-automations-{random_pet.hyperglance-automations-name.id}"
  location = "East US"
}

resource "azurerm_storage_account" "hyperglance-automations-storage-account" {
  name                     = "hyperglance-automations-{random_pet.hyperglance-automations-name.id}"
  resource_group_name      = azurerm_resource_group.hyperglance-automations-resource-group.id
  location                 = azurerm_resource_group.hyperglance-automations-resource-group.location
  account_tier             = "Standard"
  account_replication_type = "GRS"
  }