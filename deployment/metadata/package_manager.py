
import json
from pathlib import Path
import requests
from distutils.version import StrictVersion

def get_urls(package_name) -> list:
    url = f'https://pypi.org/pypi/{package_name}/json'
    data = json.loads(requests.get(url).content)['urls']
    return data

def get_requirements() -> list:
    requirements_file = Path(__file__).resolve().parents[2].joinpath('requirements.txt')
    with open(requirements_file) as requirements:
        lines = requirements.readlines()
        lines = [line for line in lines if not line.strip().startswith('#')]
    return lines

def fetch_packages(package_urls: list):
    for url in package_urls:
        requests.get(url)
    pass


if __name__ == '__main__':
    fetch_packages(get_urls(get_requirements))