
resource "random_pet" "hyperglance-automations-name" {
  length    = 2
  prefix    = "hyperglance-automations"
  separator = "-"
}

# Storage account name can only consist of lowercase letters and numbers, and must be between 3 and 24 characters long
resource "random_string" "hyperglance-automations-storage-account-name" {
  length = 12
  lower = true
  upper = false
  special = false
}

# Create resource group for deployment
resource "azurerm_resource_group" "hyperglance-automations-resource-group" {
  name     = random_pet.hyperglance-automations-name.id
  location = "East US"
  tags = var.tags
}

# Create storage account
resource "azurerm_storage_account" "hyperglance-automations-storage-account" {
  name                     = random_string.hyperglance-automations-storage-account-name.id
  resource_group_name      = azurerm_resource_group.hyperglance-automations-resource-group.name
  location                 = azurerm_resource_group.hyperglance-automations-resource-group.location
  account_tier             = "Standard"
  account_replication_type = "ZRS"
  tags = var.tags
  }

# Create a service plan for function to be assigned to
resource "azurerm_app_service_plan" "hyperglance-automations-app-service-plan" {
  name                = random_pet.hyperglance-automations-name.id
  location            = azurerm_resource_group.hyperglance-automations-resource-group.location
  resource_group_name = azurerm_resource_group.hyperglance-automations-resource-group.name
  kind                = "FunctionApp"
  reserved = true
  sku {
    tier = "Dynamic"
    size = "Y1"
  }
  tags = var.tags
}

# Create the function, assign it to service plan, link it to storage account and assign
# WEBSITE_RUN_FROM_PACKAGE setting to load function from blob using SAS
resource "azurerm_function_app" "hyperglance-automations-app" {
  name                       = random_pet.hyperglance-automations-name.id
  location                   = azurerm_resource_group.hyperglance-automations-resource-group.location
  resource_group_name        = azurerm_resource_group.hyperglance-automations-resource-group.name
  app_service_plan_id        = azurerm_app_service_plan.hyperglance-automations-app-service-plan.id 
  storage_account_name       = azurerm_storage_account.hyperglance-automations-storage-account.name
  storage_account_access_key = azurerm_storage_account.hyperglance-automations-storage-account.primary_access_key
  version = "~3"
  os_type = "linux"
  identity {
    type = "SystemAssigned"
  }
  app_settings = {
    "AzureWebJobsDisableHomepage" = true
    "WEBSITE_RUN_FROM_PACKAGE"    = "https://${azurerm_storage_account.hyperglance-automations-storage-account.name}.blob.core.windows.net/${azurerm_storage_container.hyperglance-automations-storage-container.name}/${azurerm_storage_blob.hyperglance-automations-blob.name}${data.azurerm_storage_account_blob_container_sas.hyperglance-automations-blob-container-sas.sas}",
  }
  tags = var.tags
}

# Create storage container to store zip that is loaded by function
resource "azurerm_storage_container" "hyperglance-automations-storage-container" {
  name                  = "${random_pet.hyperglance-automations-name.id}-releases"
  storage_account_name  = azurerm_storage_account.hyperglance-automations-storage-account.name
  container_access_type = "private"
}

# Generate ZIP to ready for upload to storage container
data "archive_file" "hyperglance-automations-file" {
  type        = "zip"
  source_dir  = "../../../"
  output_path = "Hyperglance_Automations_Function.zip"
  excludes    = [ "deployment" ]
}

# Upload ZIP to storage container, to be ingested by function app
resource "azurerm_storage_blob" "hyperglance-automations-blob" {
  name = "${filesha256(data.archive_file.hyperglance-automations-file.output_path)}.zip"
  storage_account_name = azurerm_storage_account.hyperglance-automations-storage-account.name
  storage_container_name = azurerm_storage_container.hyperglance-automations-storage-container.name
  type = "Block"
  source = data.archive_file.hyperglance-automations-file.output_path
}

# Generate SAS to enable function app to load ZIP from blob
data "azurerm_storage_account_blob_container_sas" "hyperglance-automations-blob-container-sas" {
  connection_string = azurerm_storage_account.hyperglance-automations-storage-account.primary_connection_string
  container_name    = azurerm_storage_container.hyperglance-automations-storage-container.name

  start = "2021-01-01T00:00:00Z"
  expiry = timeadd(timestamp(), "87660h")

  permissions {
    read   = true
    add    = false
    create = false
    write  = false
    delete = false
    list   = false
  }
}