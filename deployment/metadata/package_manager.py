
import json
from pathlib import Path
import requests
import re
from wheel_filename import parse_wheel_filename
from distutils.version import StrictVersion

def get_urls(package_name) -> list:
    url = f'https://pypi.org/pypi/{package_name}/json'
    data = json.loads(requests.get(url).content)['urls']
    files = {url['filename']: url['url'] for url in data if url['filename'].endswith('.whl')}
    parsed = []
    for file in files:
        parsed += parse_wheel_filename(file[0])
    print(files)

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
    get_urls('cryptography')
    #fetch_packages(get_urls(get_requirements))