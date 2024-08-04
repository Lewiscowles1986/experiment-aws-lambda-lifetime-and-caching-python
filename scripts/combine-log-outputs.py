import os
import json

def combine_json_files(folder_path, output_file):
    # List to store all JSON objects
    combined_data = []

    # Iterate over all files in the given folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)

            # Open and read the JSON file
            with open(file_path, 'r') as json_file:
                try:
                    # Load the JSON object
                    data = json.load(json_file)

                    # Ensure data is a dictionary (JSON object)
                    if isinstance(data, dict):
                        combined_data.append(data)
                    else:
                        print(f"Skipping {filename}: not a JSON object")

                except json.JSONDecodeError as e:
                    print(f"Error reading {filename}: {e}")

    # Write the combined data to the output file
    with open(output_file, 'w') as output_json_file:
        json.dump(combined_data, output_json_file, indent=4)

    print(f"Combined JSON written to {output_file}")

# Example usage
folder_path = os.path.curdir + '/../logs'
output_file = os.path.curdir + '/../logs-combined.json'
combine_json_files(folder_path, output_file)
