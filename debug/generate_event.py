import sys
from pathlib import Path

def generate_string(prefix, count):
    event = \
"""
"name" : "adhoc-automation-run",
  "results" : [ {
    "automation" : {
      "name" : "vm_delete",
      "params" : {
        "Delete Associated Resources" : "true"
      }
    },
    "entities" : [ 
        """
    for index in range(1, count):
        event += \
    """{
        "accountAlias" : "DevTest",
        "datasource" : "Azure",
        "name" : "{prefix}-vm-{number}",
        "attributes" : {
            "Resource Group" : "{prefix}-resources"
        },
        "subscription" : "40e09a1d-3299-4294-9a9c-ebaede24b9c8",
        "id" : "/subscriptions/40e09a1d-3299-4294-9a9c-ebaede24b9c8/resourceGroups/{prefix}-resources/providers/Microsoft.Compute/virtualMachines/{prefix}-vm-{number}",
        "type" : "Virtual Machine",
        "tags" : {

        }
      },""".format(prefix=prefix, number=count)
    event.strip(',')
    event += """],
    "entityType" : "Virtual Machine"
  } ]
}
"""

if __name__ == '__main__':
    file = Path(__file__).joinpath('event.json')
    with open(file, 'w') as fileout:
        fileout.write(generate_string(sys.argv[1]), sys.argv[2])

