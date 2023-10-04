import json
import os
import pandas as pd

# Define the input and output folder paths
input_folder = "data"  # Replace with the path to your JSONL files folder
output_folder = "output"
original_file_path = os.path.join(input_folder, "en-US.jsonl")  # Path to the original en-US JSONL file

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# # Remove existing XLSX files in the 'output' folder
for filename in os.listdir(output_folder):
    if filename.endswith(".xlsx"):
        os.remove(os.path.join(output_folder, filename))

# Initialize a dictionary to store data for each language
data_by_language = {}

# Initialize a list to store the data from the original en-US file
original_data = []

# Read the original en-US JSONL file
with open(original_file_path, "r", encoding="utf-8") as original_file:
    for line in original_file:
        original_data.append(json.loads(line))

# Iterate through JSONL files in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith(".jsonl"):
        # Extract the language code (e.g., "am" from "am-ET.jsonl")
        language_code = filename.split("-")[0]

        # Initialize an empty list to store data for this language
        data_by_language[language_code] = []

        # Open the JSONL file and append its contents to the list
        with open(os.path.join(input_folder, filename), "r", encoding="utf-8") as file:
            for line in file:
                data = json.loads(line)
                data_by_language[language_code].append(data)

# Iterate through the data and create XLSX files for each language
for language_code, data in data_by_language.items():
    # Create a Pandas DataFrame from the JSON data
    df = pd.DataFrame(data, columns=['id', 'utt', 'annot_utt'])

    # Merge data from the original en-US file based on the 'id' column
    en_us_data = pd.DataFrame(original_data, columns=['id', 'utt', 'annot_utt'])
    df = pd.merge(df, en_us_data, on='id', how='left')

    # Construct the output XLSX file name (e.g., "en-am.xlsx")
    output_filename = f"en-{language_code}.xlsx"

    # Define the full output file path
    output_file_path = os.path.join(output_folder, output_filename)

    # Save the DataFrame to an XLSX file
    df.to_excel(output_file_path, index=False)

print("XLSX files with data have been updated in the 'output' folder.")