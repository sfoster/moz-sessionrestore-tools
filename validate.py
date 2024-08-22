import json
import jsonschema
from jsonschema import validate
from argparse import ArgumentParser
import os 

def load_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def is_valid_json(json_data, json_schema):
    """Validate JSON data against the given schema."""
    try:
        validate(instance=json_data, schema=json_schema)
        return True
    except jsonschema.exceptions.ValidationError as ve:
        print(f"Validation Error: {ve}")
        return False

script_dir = os.path.dirname(os.path.abspath(__file__))

argparser = ArgumentParser(description="Validate JSON")
argparser.add_argument(
    "in_file",
    help="Path to input file."
)

default_schema_path = os.path.join(script_dir, 'session-schema.json')
argparser.add_argument(
    '--schema', 
    type=str, 
    default=default_schema_path, 
    help='Path to the schema file'
)

parsed_args = argparser.parse_args()

 # Define JSON schema
schema = load_json(parsed_args.schema)

# Load JSON document
json_data = load_json(parsed_args.in_file)

# Validate the JSON data
if is_valid_json(json_data, schema):
    print("Given JSON data is valid.")
else:
    print("Given JSON data is not valid.")
