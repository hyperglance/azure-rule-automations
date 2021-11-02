import importlib
import sys
from pathlib import Path
import os

def generate_providers(subscriptions: list):
    provider_file = Path(__file__).parents[1].joinpath('modules', 'hyperglance-x-sub', 'provider.tf')
    file_contents = ""
    for subscription in subscriptions:
        file_contents += \
"""# This is a generated configuration and will be overwritten upon reprovisioning
provider "azurerm" {{
  features {{}}
  alias = "subscription-{sub}"
  subscription_id = "{sub}"
}}
""".format(sub = subscription)
    with open(provider_file, 'w') as file:
        file.write(file_contents)

def generate_main(subscriptions: list):
  x_sub_main_file = Path(__file__).parents[1].joinpath('modules', 'hyperglance-x-sub', 'main.tf')
  automations_main_file = Path(__file__).parents[1].joinpath('modules', 'hyperglance-automations', 'main.tf')
  file_contents = \
"""
# <----------------------------Generated------------------------------->

# Give function access to control VMs in current subscription
# Create a new role assignment for each subscription
resource "azurerm_role_assignment" "hyperglance-automations-role-assignment" {{
   scope                = data.azurerm_subscription.primary.id
   role_definition_id   = azurerm_role_definition.hyperglance-automations-role.role_definition_resource_id
   principal_id         = azurerm_function_app.hyperglance-automations-app.identity.0.principal_id
}}

resource "azurerm_role_definition" "hyperglance-automations-role" {{
  name        = random_pet.hyperglance-automations-name.id
  scope       = data.azurerm_subscription.primary.id

  permissions {{
    actions     = {permissions}
    not_actions = []
  }}

}}
""".format(permissions = str(generate_permissions(str(Path(__file__).resolve().parents[3]))).replace("'", "\""))
  with open(automations_main_file, 'a') as file:
        file.write(file_contents)
  file_contents = "" 
  for subscription in subscriptions:
    file_contents += \
"""# This is a generated configuration and will be overwritten upon reprovisioning
# Create a new role assignment for each subscription
resource "azurerm_role_assignment" "hyperglance-automations-role-assignment-{sub}" {{
   provider = azurerm.subscription-{sub}
   scope                = "/subscriptions/{sub}"
   role_definition_id   = azurerm_role_definition.hyperglance-automations-role-{sub}.role_definition_resource_id
   principal_id         = var.function-principal-id
}}

resource "azurerm_role_definition" "hyperglance-automations-role-{sub}" {{
  provider = azurerm.subscription-{sub}
  name        = var.hyperglance-name
  scope       = "/subscriptions/{sub}"
  assignable_scopes = ["${{var.primary-subscription}}", "/subscriptions/{sub}"]

  permissions {{
    actions     = {permissions}
    not_actions = []
  }}

}}
""".format(
  sub=subscription,
  permissions = str(generate_permissions(str(Path(__file__).resolve().parents[3]))).replace("'", "\"")
  )
  with open(x_sub_main_file, 'w') as file:
        file.write(file_contents)

def generate_permissions(function_root) -> dict:
    """ Generates the HyperglanceAutomations.json file

  Returns
  -------
  list
    A json formatted list containing the available automations

  """
    automation_files = os.listdir(os.path.join(function_root, "hyperglance_automations", "actions"))
    automations = [os.path.splitext(f)[0] for f in automation_files if f.endswith('.py')]

    # remove duplicates and present to terraform in the required 'shallow' string map
    permissions = {}

    for index, automation in enumerate(automations):
        automation_module = importlib.import_module(''.join(['hyperglance_automations.','actions.', automation]), package=None)
        for permission in automation_module.info()['permissions']:
            permissions[''.join([permission])] = permission
    return list(permissions.keys())




if __name__ == '__main__':
    sys.path.append(str(Path(__file__).resolve().parents[3]))
    parse_subscriptions = importlib.import_module('deployment.metadata.parse_subscriptions')
    subscription_ids = parse_subscriptions.list_subscriptions('subscriptions.csv').keys()
    generate_providers(subscription_ids)
    generate_main(subscription_ids)
    

    

