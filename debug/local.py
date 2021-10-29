import pathlib 
import json
import json
import sys
import importlib


def main(path: str):
    hyperglance_path = pathlib.Path(__file__).absolute().parents[1]
    sys.path.append(str(hyperglance_path.absolute()))
    processing = importlib.import_module("hyperglance_automations.processing.processing")
    file = pathlib.Path(path)
    with open(file, 'r', encoding='utf-8') as instream:
        mock_blob = instream.read()
    payload = json.loads(mock_blob)
    outputs = []
    try:
        processing.process_event(payload, outputs) 
    except Exception as e:
        print(e)
    

if __name__ == "__main__":
    main("event.json")