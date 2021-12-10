
import json
from pathlib import Path
import tarfile
import requests
import re
from wheel_filename import parse_wheel_filename
import os 
import shutil
import importlib

def setup_tars(package_name) -> str:
    url = f'https://pypi.org/pypi/{package_name}/json'
    raw_content = requests.get(url).content
    data = json.loads(raw_content)['urls']
    for url in data:
        if 'tar.gz' in url['url']:
            fetch_package(url['url'])
            filename = url['filename']
            with tarfile.open(f'.tmp/{filename}') as tarf:
                tarf.extractall('.tmp/')
            importlib.import_module('.tmp')
    

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
    dependencies = [re.sub(regex, '', dependency).strip() for dependency in dependencies] # remove version info
    return lines + dependencies

def fetch_package(package_url: str):
    filename = package_url.split('/')[-1]
    request = requests.get(package_url)
    with open(f'.tmp/{filename}', 'wb') as wheel:
        wheel.write(request.content)



if __name__ == '__main__':
    shutil.rmtree('.tmp', ignore_errors=True)
    os.mkdir('.tmp')
    packages = get_requirements()
    for package in packages:
        setup_tars(package)
    #print(package_urls)
    # for url in package_urls:
    #     fetch_package(url)

