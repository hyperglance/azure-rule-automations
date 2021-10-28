from azure.mgmt.resource.resources.v2018_05_01 import operations
from msrestazure.azure_cloud import *
from azure.mgmt.resource.resources import ResourceManagementClient
from azure.mgmt.resource.resources.models import TagsPatchResource

def add_tag(credential, resource: dict, cloud:Cloud, key: str, value: str):
    url = cloud.endpoints.resource_manager
    client = ResourceManagementClient(
        credential,
        resource['subscription'],
        base_url=url,
        credential_scopes=[url + '/.default']).tags()
    client.update_at_scope(resource['scope'], TagsPatchResource('Merge', {key: value}))

def rm_tag(credential, resource: dict, cloud:Cloud, key, value):
    url = cloud.endpoints.resource_manager
    client = ResourceManagementClient(
        credential,
        resource['subscription'],
        base_url=url,
        credential_scopes=[url + '/.default']).tags()
    client.update_at_scope(resource['scope'], TagsPatchResource('Delete', {key: value}))
