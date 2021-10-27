import importlib
import sys
from pathlib import Path
import subprocess


constant_contents = \
"""
# We strongly recommend using the required_providers block to set the
# Azure Provider source and version being used
terraform {
  required_version = ">= 0.13.6"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 2.78.0"
    }
  }
}
# Configure the Microsoft Azure Provider
provider "azurerm" {
  features {}
}

"""

def generate_providers(subscriptions: list):
    provider_file = Path(__file__).parents[1].joinpath('modules', 'hyperglance-automations', 'provider.tf')
    global constant_contents
    variable_contents = ""
    for subscription in subscriptions:
        variable_contents += \
"""
provider "azurem" {
  features {{}}
  alias = "{sub}"
  subscription_id = "{sub}"
}
""".format(sub = subscription)
    file_contents = constant_contents + variable_contents
    with open(provider_file, 'w') as file:
        file.write(file_contents)

if __name__ == '__main__':
    automations_root = Path(__file__).parents[3]
    sys.path.append(str(automations_root.absolute()))
    parse_subscriptions = importlib.import_module('deployment.metadata.parse_subscriptions')
    generate_providers(parse_subscriptions.list_subscriptions('subscriptions.csv').keys())
    subprocess.run(['terraform', 'init'])
    subprocess.run(['terraform', 'apply', '--auto-approve'])

    

