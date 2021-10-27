
# Give function access to control VMs in current subscription
# Create a new role assignment for each subscription
resource "azurerm_role_assignment" "hyperglance-automations-role-assignment" {
   scope                = each.key
   role_definition_id   = azurerm_role_definition.hyperglance-automations-role.role_definition_resource_id
   principal_id         = azurerm_function_app.hyperglance-automations-app.identity.0.principal_id
}


resource "azurerm_role_definition" "hyperglance-automations-role" {
  name        = "hyper"
  scope       = var.subscription-id
  assignable_scopes = var.function-principal-id

  permissions {
    actions     = [
      "Microsoft.Compute/images/delete"
    ]
    not_actions = []
  }

}