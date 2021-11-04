import importlib
import sys
from pathlib import Path

def generate_providers(subscriptions: list):
    print(Path(__file__).parents[1].absolute())
    return
    #.joinpath('modules', 'hyperglance-x-sub', 'provider.tf')
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
  main_file = Path(__file__).parents[1].joinpath('modules', 'hyperglance-x-sub', 'main.tf')
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
    actions     = var.permissions
    not_actions = []
  }}

}}
""".format(sub=subscription)
  with open(main_file, 'w') as file:
        file.write(file_contents)


if __name__ == '__main__':
    automations_root = Path(__file__).resolve().parents[3]
    sys.path.append(str(automations_root.absolute()))
    parse_subscriptions = importlib.import_module('deployment.metadata.parse_subscriptions')
    subscription_ids = parse_subscriptions.list_subscriptions('subscriptions.csv').keys()
    generate_providers(subscription_ids)
    generate_main(subscription_ids)
    

    

