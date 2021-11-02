"""Get the aggregated permissions required to run all automations

Returns list (json) of all required permissions
"""

import importlib
import json
import os
import pathlib
import sys


def fetch_permissions_list(function_root) -> dict:
    """ Generates the HyperglanceAutomations.json file

  Returns
  -------
  list
    A json formatted list containing the available automations

  """
    automation_files = os.listdir(os.path.join(function_root, "actions"))
    automations = [os.path.splitext(f)[0] for f in automation_files if f.endswith('.py')]

    # remove duplicates and present to terraform in the required 'shallow' string map
    permissions = {}

    for index, automation in enumerate(automations):
        automation_module = importlib.import_module(''.join(['actions.', automation]), package=None)
        for permission in automation_module.info()['permissions']:
            permissions[''.join([permission])] = permission
    return permissions

if __name__ == '__main__':
  function_root = pathlib.Path(os.path.abspath(__file__)).parents[2].joinpath('hyperglance_automations')
  sys.path.append(str(function_root))
  print(json.dumps(fetch_permissions_list(function_root)))
