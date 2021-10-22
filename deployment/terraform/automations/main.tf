


module "hyperglance-automations" {
  region = "useast"
  source = "../modules/hyperglance-automations"
  utilised-subscriptions-script = "../../metadata/parse_subscriptions.py"
}
