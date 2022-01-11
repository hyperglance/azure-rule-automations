import shutil
import sys
import hashlib
import pathlib
import json
import base64 as encoder
import os
import time

def zip_code(output: pathlib.Path, to_zip: pathlib.Path):
    shutil.make_archive(output, 'zip', to_zip)
    with open(output + '.zip',"rb") as f:
        bytes = f.read() 
        return encoder.standard_b64encode(hashlib.sha256(bytes).digest()).decode('utf-8');

def cp_deployment(deployment_root: pathlib.Path, output: pathlib.Path):
    excluded = ['deployment', 'files', 'LICENSE', 'README.md', '.git', 'SECURITY.md', 'bitbucket-pipelines.yml']
    
    os.mkdir(output)
    
    for item in deployment_root.iterdir() :
        if not any(word in str(item) for word in excluded):
            if item.is_dir():
                shutil.copytree(item, os.path.join(output,str(item.name)), ignore=shutil.ignore_patterns('__pycache__'))
            else:
                shutil.copy(item,  os.path.join(output,str(item.name)))

if __name__ == '__main__':
    hyperglance_root = pathlib.Path(__file__).resolve().parents[2]
    cp_deployment(hyperglance_root, 'temp')
    digest = zip_code(sys.argv[1], 'temp')
    shutil.rmtree('temp', ignore_errors=True)
    # give to terraform 
    print(json.dumps({'HASH': digest}))
