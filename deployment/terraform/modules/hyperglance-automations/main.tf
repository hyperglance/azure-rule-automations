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
    hyperglanceautomations_STORAGE = azurerm_storage_account.hyperglance-automations-storage-account.primary_connection_string
    AzureWebJobsDisableHomepage    = true
    APPINSIGHTS_INSTRUMENTATIONKEY = azurerm_application_insights.hyperglance-automations-application-insights.instrumentation_key
    ENABLE_ORYX_BUILD              = true
    SCM_DO_BUILD_DURING_DEPLOYMENT = 1
    FUNCTIONS_WORKER_RUNTIME       = "python"
    BUILD_FLAGS                    = "UseExpressBuild"
    #HASH = base64encode(filesha256("hyperglance_automations.zip"))
  }
  tags = var.tags
  depends_on = [null_resource.compressed-code]
}

# Enable application insights for function
resource "azurerm_application_insights" "hyperglance-automations-application-insights" {
  name                = random_pet.hyperglance-automations-name.id
  location            = azurerm_resource_group.hyperglance-automations-resource-group.location
  resource_group_name = azurerm_resource_group.hyperglance-automations-resource-group.name
  application_type    = "other"
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
}

# Upload the function code to a blob for deployment
resource "azurerm_storage_blob" "function-code" {
    name = "hyperglance_automations.zip"
    storage_account_name = azurerm_storage_account.hyperglance-automations-storage-account.name
    storage_container_name = azurerm_storage_container.hyperglance-automations-storage-container.name
    type = "Block"
    source = "hyperglance_automations.zip"

    depends_on = [null_resource.compressed-code]
}

locals {
  is-windows = substr(pathexpand("~"), 0, 1) == "/" ? false : true
}

resource "null_resource" "compressed-code" {
    provisioner "local-exec" {
      command = local.is-windows ? "Compress-Archive ..\\..\\..\\hyperglance_automations hyperglance_automations.zip" : "\"zip -r hyperglance_automations.zip /Users/jake/Dev/azure-rule-automations/hyperglance_automations\"" 
      interpreter = local.is-windows ? ["PowerShell", "-Command"] : ["bash", "-c"]
    }
}

resource "null_resource" "compressed-code-remove" {
  provisioner "local-exec" {
     when = destroy
     # cannot reference locals in a destroy block
     command = (substr(pathexpand("~"), 0, 1) == "/" ? false : true) ? "Remove-Item hyperglance_automations.zip" : "rm -f hyperglance_automations.zip"
     interpreter = (substr(pathexpand("~"), 0, 1) == "/" ? false : true) ? ["PowerShell", "-Command"] : ["bash", "-c"]

    }
}



# Get the utilised subscriptions from the subscriptions.csv
data "external" "utilised-subscriptions" {
    program = local.is-windows ? ["py", "-3", var.utilised-subscriptions-script] : ["python3", var.utilised-subscriptions-script]
}

# data "external" "utilised-subscriptions" {
#     program = local.is-windows ? ["py", "-3", var.utilised-subscriptions-script] : ["python3", var.utilised-subscriptions-script]

# }

# Get the id of all of the subscriptions that are in subscriptions.csv and that we have access to
data "azurerm_subscriptions" "available-subscriptions" {
    for_each = toset(keys(data.external.utilised-subscriptions.result))
    display_name_prefix = each.value
}

#### Permissions ####

# Get current subscription ID
data "azurerm_subscription" "primary" {
}

# Give function access to write to storage account
resource "azurerm_role_assignment" "hyperglance-automations-storage-blob-contributor" {
  scope                = azurerm_storage_account.hyperglance-automations-storage-account.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = azurerm_function_app.hyperglance-automations-app.identity.0.principal_id
}

# Give function access to control VMs in current subscription
# Create a new role assignment for each subscription
resource "azurerm_role_assignment" "hyperglance-automations-x-subscription-virtual-machine-contributor" {
   for_each = toset([for subscription in data.azurerm_subscriptions.available-subscriptions: subscription.subscriptions[0].id if length(subscription.subscriptions) != 0])
   scope                = each.key
   role_definition_name = "Virtual Machine Contributor"
   principal_id         = azurerm_function_app.hyperglance-automations-app.identity.0.principal_id
 }

# Always give these perms for the current account
resource "azurerm_role_assignment" "hyperglance-automations-virtual-machine-contributor" {
  scope                = data.azurerm_subscription.primary.id
  role_definition_name = "Virtual Machine Contributor"
  principal_id         = azurerm_function_app.hyperglance-automations-app.identity.0.principal_id
}