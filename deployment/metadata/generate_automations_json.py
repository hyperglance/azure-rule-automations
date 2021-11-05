"""Get Automation List

Returns the list of available automations for use in Hyperglance.
"""

import os
import importlib
import sys
import pathlib
import json


def generate_json(automations_root) -> str:
    automation_files = os.listdir(os.path.join(automations_root, "hyperglance_automations", "actions"))
    automations = [os.path.splitext(f)[0] for f in automation_files if f.endswith('.py')]
    root = {"automations": []}

    for index, automation in enumerate(automations):
        automation_module = importlib.import_module(''.join(['hyperglance_automations.', 'actions.', automation]), package=None)
        automation_info = {"name": automation}
        automation_info.update(automation_module.info())
        root["automations"].append(automation_info)
    return json.dumps(root)

if __name__ == '__main__':
    automations_root = pathlib.Path(__file__).resolve().parents[2]
    automations_file = automations_root.joinpath("files", "HyperglanceAutomations.json")
    sys.path.append(str(automations_root.absolute()))
    with open(automations_file, 'w') as file:
      file.write(generate_json(automations_root))
    print(json.dumps({str(automations_file) : str(automations_file)}))
