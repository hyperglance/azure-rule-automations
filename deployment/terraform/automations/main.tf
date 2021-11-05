module "hyperglance-automations" {
  region = "eastus"
  source = "../modules/hyperglance-automations"
  utilised-subscriptions-script = "../../metadata/parse_subscriptions.py"
  
  # optionally set these
  # region = ""
  # zip-location = ""
}
