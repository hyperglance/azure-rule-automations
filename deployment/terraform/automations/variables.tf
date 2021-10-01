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
  description = "value"
  default     = "East US"
}

# Cap the number of workers that can be allocated to the function
variable "app_scale_limit" {
  type = number
  description = "Maximum number of workers that can be allocated to the function"
  default = 5
}
