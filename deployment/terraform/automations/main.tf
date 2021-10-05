


module "hyperglance-automations" {
  source = "../modules/hyperglance-automations"
  utilised-subscriptions-script = "../../metadata/parse_subscriptions.py"
}
