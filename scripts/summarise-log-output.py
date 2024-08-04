import json
import os

def extract_unique_values(input_file, output_file, keys_to_extract):
    # Load the JSON data from the input file
    with open(input_file, 'r') as json_file:
        data = json.load(json_file)
    
    # Initialize a dictionary to store unique values and counts
    unique_values = {key: set() for key in keys_to_extract}

    # Iterate over each object in the JSON array
    for obj in data:
        for key in keys_to_extract:
            if key in obj:
                unique_values[key].add(obj[key])

    # Prepare the output structure
    # Prepare the output structure
    output_data = {'inputData': data}
    for key in keys_to_extract:
        output_data[key] = {
            'values': list(unique_values[key]),
            'count': len(unique_values[key])
        }

    # Write the output data to the output file
    with open(output_file, 'w') as json_output_file:
        json.dump(output_data, json_output_file, indent=4)

    print(f"Processed data written to {output_file}")

# Example usage
input_file = os.path.curdir + '/../logs-combined.json'
output_file = os.path.curdir + '/../output-report.json'
keys_to_extract = ['pid', 'uuid', 'time']
extract_unique_values(input_file, output_file, keys_to_extract)
