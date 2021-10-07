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
  description = "Location of the script which parses subscriptions.csv"
  default = "../../metadata/parse_subscriptions.py"
}

variable "compress-code-script" {
  type = string
  description = "Location of the script which compresses hyperglance_automations function code and generates a sha256 digest"
  default = "../../metadata/compress_code.py"
}

# Cap the number of workers that can be allocated to the function
variable "app_scale_limit" {
  type = number
  description = "Maximum number of workers that can be allocated to the function"
  default = 5
}

# Cap the number of workers that can be allocated to the function
variable "zip-location" {
  type = string
  description = "The location at which the hyperglance_automations.zip file is generated (relative to the compress_code script)"
  default = "../terraform/automations/hyperglance_automations"
}


