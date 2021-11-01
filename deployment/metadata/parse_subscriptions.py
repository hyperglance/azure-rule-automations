import pathlib
import json
import subprocess
import os

def list_subscriptions(csv: pathlib.PurePath) -> dict:
    '''parse the csv into a shallow map of subscription ids'''
    try:
        with open(csv) as file:
            elements = file.read().replace(' ', '').split(',') # read the file and transform to list
    except: 
        print('there was a problem parsing the list of subscriptions, returning an empty map')
        return {}
    result = subprocess.run(
        ['bash', '-c', 'az account list'] if os.name == 'posix' else ['cmd', '/C az account list'],
        stdout=subprocess.PIPE)
    try:
        az_response = json.loads(result.stdout)
    except Exception as e:
        print('There was a problem parsing the api response from azure - returning an empty map')
        return {}
    for item in az_response:
        subscription_ids = (
            subscription['id'] for subscription in az_response \
                 if subscription['name'] in elements and subscription['isDefault'] == False
                 )
    return dict.fromkeys(subscription_ids)

if __name__ == '__main__':
    subscriptions_csv = pathlib.Path(__file__).parents[1].joinpath('terraform', 'automations', 'subscriptions.csv')
    print(json.dumps(list_subscriptions(subscriptions_csv)))