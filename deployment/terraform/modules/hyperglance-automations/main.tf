# Generare random suffix for Hyperglance automations associated assets
resource "random_pet" "hyperglance-automations-name" {
  length    = 2
  prefix    = "hyperglance-automations"
  separator = "-"
}

# Storage account name can only consist of lowercase letters and numbers, and must be between 3 and 24 characters long
# Generating separate random string for this
resource "random_string" "hyperglance-automations-storage-account-name" {
  length  = 12
  lower   = true
  upper   = false
  special = false
}

# Create resource group for deployment
resource "azurerm_resource_group" "hyperglance-automations-resource-group" {
  name     = random_pet.hyperglance-automations-name.id
  location = var.region
  tags     = var.tags
}

# Create storage account
resource "azurerm_storage_account" "hyperglance-automations-storage-account" {
  name                     = random_string.hyperglance-automations-storage-account-name.id
  resource_group_name      = azurerm_resource_group.hyperglance-automations-resource-group.name
  location                 = azurerm_resource_group.hyperglance-automations-resource-group.location
  account_tier             = "Standard"
  account_replication_type = "ZRS"
  tags                     = var.tags
}

# Create a service plan for function to be assigned to
resource "azurerm_app_service_plan" "hyperglance-automations-app-service-plan" {
  name                = random_pet.hyperglance-automations-name.id
  location            = azurerm_resource_group.hyperglance-automations-resource-group.location
  resource_group_name = azurerm_resource_group.hyperglance-automations-resource-group.name
  kind                = "FunctionApp"
  reserved            = true
  sku {
    tier = "Dynamic"
    size = "Y1"
  }
  tags = var.tags
}

# Create the function, assign it to service plan and link it to storage account
resource "azurerm_function_app" "hyperglance-automations-app" {
  name                       = random_pet.hyperglance-automations-name.id
  location                   = azurerm_resource_group.hyperglance-automations-resource-group.location
  resource_group_name        = azurerm_resource_group.hyperglance-automations-resource-group.name
  app_service_plan_id        = azurerm_app_service_plan.hyperglance-automations-app-service-plan.id
  storage_account_name       = azurerm_storage_account.hyperglance-automations-storage-account.name
  storage_account_access_key = azurerm_storage_account.hyperglance-automations-storage-account.primary_access_key
  version                    = "~3"
  os_type                    = "linux"
  identity {
    type = "SystemAssigned"
  }
  site_config {
    app_scale_limit = var.app_scale_limit
  }
  app_settings = {
    "hyperglanceautomations_STORAGE" = azurerm_storage_account.hyperglance-automations-storage-account.primary_connection_string
    "AzureWebJobsDisableHomepage"    = true
    "ENABLE_ORYX_BUILD"              = true
    "SCM_DO_BUILD_DURING_DEPLOYMENT" = 1
    "FUNCTIONS_WORKER_RUNTIME"       = "python"
    "BUILD_FLAGS"                    = "UseExpressBuild"
  }
  tags = var.tags
}


# Create storage container for Hyperglance function
resource "azurerm_storage_container" "hyperglance-automations-storage-container" {
  name                  = "hyperglance-automations"
  storage_account_name  = azurerm_storage_account.hyperglance-automations-storage-account.name
  container_access_type = "private"
}

# Upload HyperglanceAutomations.json to storage container
resource "azurerm_storage_blob" "hyperglance-automations-json-blob" {
  name                   = "HyperglanceAutomations.json"
  storage_account_name   = azurerm_storage_account.hyperglance-automations-storage-account.name
  storage_container_name = azurerm_storage_container.hyperglance-automations-storage-container.name
  type                   = "Block"
  source                 = "${path.module}/../../../../files/HyperglanceAutomations.json"
  content_md5            = filemd5("${path.module}/../../../../files/HyperglanceAutomations.json")
}

locals {
  is-windows = substr(pathexpand("~"), 0, 1) == "/" ? false : true
}

data "external" "permissions" {
    program = local.is-windows ? ["py", "-3", var.generate-permissions-script] : ["python3", var.generate-permissions-script]
}

# Get current subscription ID
data "azurerm_subscription" "primary" {
}

#### Permissions ####

module "hyperglance-x-sub" {
  source = "../hyperglance-x-sub"
  function-principal-id = azurerm_function_app.hyperglance-automations-app.identity.0.principal_id
  hyperglance-name = random_pet.hyperglance-automations-name.id
  primary-subscription = data.azurerm_subscription.primary.id
  permissions = keys(data.external.permissions.result)
}

# Give function access to write to storage account
resource "azurerm_role_assignment" "hyperglance-automations-storage-blob-contributor" {
  scope                = azurerm_storage_account.hyperglance-automations-storage-account.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = azurerm_function_app.hyperglance-automations-app.identity.0.principal_id
}


# Give function access to control VMs in current subscription
# Create a new role assignment for each subscription
resource "azurerm_role_assignment" "hyperglance-automations-role-assignment" {
   scope                = data.azurerm_subscription.primary.id
   role_definition_id   = azurerm_role_definition.hyperglance-automations-role.role_definition_resource_id
   principal_id         = azurerm_function_app.hyperglance-automations-app.identity.0.principal_id
}

resource "azurerm_role_definition" "hyperglance-automations-role" {
  name        = random_pet.hyperglance-automations-name.id
  scope       = data.azurerm_subscription.primary.id

  permissions {
    actions     = keys(data.external.permissions.result)
    not_actions = []
  }

}






