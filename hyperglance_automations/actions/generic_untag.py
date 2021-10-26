from msrestazure.azure_cloud import Cloud
import hyperglance_automations.processing.tagging as tagging

def hyperglance_automation(credential, resource: dict, cloud:Cloud, automation_params = ''):
  tagging.rm_tag(credential, resource, cloud)

def info() -> dict:
  INFO = {
    "displayName": "Add Tag",
    "description": "Adds a tag to a resource",
    "resourceTypes": [
      "Virtual Machine" 
    ],
    "params": [

    ],
    "roles": [
      
    ]
  }

  return INFO