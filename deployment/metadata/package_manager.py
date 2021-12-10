
import json
from pathlib import Path
import requests
import re
from wheel_filename import parse_wheel_filename
from distutils.version import StrictVersion

def get_url(package_name) -> str:
    url = f'https://pypi.org/pypi/{package_name}/json'
    accepted_tags = [
        'manylinux2010_x86_64',
        'manylinux2014_x86_64',
        'manylinux_2_17_x86_64', 
        'manylinux_2_24_x86_64',
        'any'
    ]
    data = json.loads(requests.get(url).content)['urls']
    files = {url['filename']: url['url'] for url in data if url['filename'].endswith('.whl')}
    parsed_items = []
    for tag in accepted_tags:
        for file in files:
            item = parse_wheel_filename(file)
            if tag in item.platform_tags:
                print('tag is ' + tag)
                print('platform tags ' + str(item.platform_tags))
                return files[str(item)]
    raise Exception('no suitable package versions for the plaform were found')

def get_requirements() -> list:
    requirements_file = Path(__file__).resolve().parents[2].joinpath('requirements.txt')
    dependencies = []
    regex = re.compile("[\(;].*$")
    with open(requirements_file) as requirements:
        lines = requirements.readlines()
        lines = [line.replace('\n', '') for line in lines if not line.startswith('#') and not len(line) == 1]
    for line in lines:
        url = f'https://pypi.org/pypi/{line}/json'
        dependencies += json.loads(requests.get(url).content)['info']['requires_dist']
    dependencies = [re.sub(regex, '', dependency) for dependency in dependencies] # remove version info
    return lines + dependencies

def fetch_packages(package_urls: list):
    for url in package_urls:
        requests.get(url)
    pass

class Package:
    def __init__(self, name: str, version: str):
        self.name = name
        self.version = version


if __name__ == '__main__':
    #print(get_requirements())
    print(get_url('mypy'))
    #fetch_packages(get_urls(get_requirements))

