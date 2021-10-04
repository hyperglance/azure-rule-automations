import pathlib
import json

def list_subscriptions(csv: pathlib.PurePath) -> dict:
    '''parse the csv into a shallow map required by terraform data external'''
    with open(csv) as file:
        elements = file.read().replace(' ', '').split(',') # read the file and transform to list
    return dict.fromkeys(elements)

subscriptions_csv = pathlib.Path(__file__).parents[1].joinpath('terraform', 'automations', 'subscriptions.csv')
print(json.dumps(list_subscriptions(subscriptions_csv)))