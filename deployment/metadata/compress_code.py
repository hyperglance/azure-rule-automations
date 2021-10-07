import shutil
import sys
import hashlib
import pathlib
import json
import base64 as encoder

def zip_code(output: pathlib.Path, to_zip: pathlib.Path):
    shutil.make_archive(output, 'zip', to_zip)
    with open(output + '.zip',"rb") as f:
        bytes = f.read() 
        return encoder.standard_b64encode(hashlib.sha256(bytes).digest()).decode('utf-8');

function_path = pathlib.Path(__file__).parents[2].joinpath('hyperglance_automations')
digest = zip_code(sys.argv[1], function_path)

# give to terraform 
print(json.dumps({'HASH': digest}))
