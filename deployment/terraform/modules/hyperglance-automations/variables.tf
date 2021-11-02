# Tags to deploy against resources
variable "tags" {
  type        = map(string)
  description = "Resource Tags to Apply"
  default = {
    Name        = "Hyperglance Automations"
    Persistent  = "True"
    Description = "Resources Required by Hyperglance Automations"
    Help        = "https://support.hyperglance.com/"
    Source      = "https://github.com/hyperglance/azure-rule-automations"
  }
}

# Define the Azure region to deploy the resources in
variable "region" {
  type        = string
  description = "Azure region to deploy resources in e.g. East US"
  default = "East US"
}

variable "utilised-subscriptions-script" {
  type = string
  description = "location of the script which parses subscriptions.csv"
}

# Cap the number of workers that can be allocated to the function
variable "app_scale_limit" {
  type = number
  description = "Maximum number of workers that can be allocated to the function"
  default = 5
}

variable "generate-permissions-script" {
  type = string
  description = "The path of the script which generates the required permissions for the hyperglance role"
  default = "../../metadata/generate_permissions.py"
}

variable "generate-automations-script" {
  type = string
  description = "The path of the script which generates the HyperglanceAutomations.json"
  default = "../../metadata/generate_automations_json.py"
}
