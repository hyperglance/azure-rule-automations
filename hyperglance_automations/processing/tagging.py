from msrestazure.azure_cloud import *
from azure.mgmt.resource.resources import ResourceManagementClient

def add_tag(credential, resource: dict, cloud:Cloud, key: str, value: str):
    url = cloud.endpoints.resource_manager
    client = ResourceManagementClient(
        credential,
        resource['subscription'],
        base_url=url,
        credential_scopes=[url + '/.default']).tags
    previous = client.get_at_scope(resource['id'])
    appended = previous.properties.tags
    appended[key] = value
    tags = {'properties': {'tags' : appended}}
    response = client.create_or_update_at_scope(resource['id'], tags)

def rm_tag(credential, resource: dict, cloud:Cloud, key, ):
    url = cloud.endpoints.resource_manager
    client = ResourceManagementClient(
        credential,
        resource['subscription'],
        base_url=url,
        credential_scopes=[url + '/.default']).tags
    previous = client.get_at_scope(resource['id'])
    ammended = previous.properties.tags
    del ammended[key]
    tags = {'properties': {'tags' : ammended}}
    client.create_or_update_at_scope(resource['id'], tags)
