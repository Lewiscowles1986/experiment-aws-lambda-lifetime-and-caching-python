import json
import os
import re
from dataclasses import dataclass, field

@dataclass(frozen=True, slots=True)
class KeyAlias:
    key: str
    alias: str = field(default_factory=str)

def parse_key_alias(input_string):
    # Regex pattern to capture key and optional alias
    pattern = r"\s*([a-zA-Z0-9_-]+)\s*(:\s*([a-zA-Z0-9_-]+))?"
    match = re.match(pattern, input_string)
    if match:
        key = match.group(1)
        alias = match.group(3) if match.group(3) else key
        return KeyAlias(key=key, alias=alias)
    else:
        raise ValueError(f"Invalid key alias format: {input_string}")

def extract_unique_values(input_file, output_file, keys_with_aliases: list[KeyAlias]):
    # Load the JSON data from the input file
    with open(input_file, 'r') as json_file:
        data = json.load(json_file)

    # Initialize a dictionary to store unique values and counts
    unique_values = {alias.alias: set() for alias in keys_with_aliases}

    # Iterate over each object in the JSON array
    for obj in data:
        for key_alias in keys_with_aliases:
            key = key_alias.key
            alias = key_alias.alias
            if key in obj:
                unique_values[alias].add(obj[key])

    # Prepare the output structure
    output_data = {'inputData': data}
    for alias in unique_values:
        output_data[alias] = {
            'values': list(unique_values[alias]),
            'count': len(unique_values[alias])
        }

    # Write the output data to the output file
    with open(output_file, 'w') as json_output_file:
        json.dump(output_data, json_output_file, indent=4)

    print(f"Processed data written to {output_file}")

# Example usage
input_file = os.path.curdir + '/../logs-combined.json'
output_file = os.path.curdir + '/../output-report.json'
keys_to_extract = ['pid : pids', 'uuid:uuidsGeneratedAtBoot', 'time:cachedTimes']
keys_with_aliases = [parse_key_alias(key) for key in keys_to_extract]
extract_unique_values(input_file, output_file, keys_with_aliases)
