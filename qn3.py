import jsonlines
import json
from google.colab import files
from google.colab import drive

# Authenticate and mount Google Drive
drive.mount('/content/drive')

# Specify the file paths on Google Drive
english_file_path = '/content/drive/MyDrive/path_to_english-train.jsonl'
swahili_file_path = '/content/drive/MyDrive/path_to_swahili-train.jsonl'
german_file_path = '/content/drive/MyDrive/path_to_german-train.jsonl'
output_file_path = '/content/drive/MyDrive/path_to_combined_translations.json'

# Initialize a dictionary to store translations
translations = {}

# Process English data
with jsonlines.open(english_file_path) as reader:
    english_data = list(reader)

for entry in english_data:
    id = entry['id']
    utt = entry['utt']
    translations[id] = {'en': utt, 'translations': {}}

# Process Swahili data
with jsonlines.open(swahili_file_path) as reader:
    swahili_data = list(reader)

for entry in swahili_data:
    id = entry['id']
    utt = entry['utt']
    if id in translations:
        translations[id]['translations']['sw'] = utt

# Process German data
with jsonlines.open(german_file_path) as reader:
    german_data = list(reader)

for entry in german_data:
    id = entry['id']
    utt = entry['utt']
    if id in translations:
        translations[id]['translations']['ge'] = utt

# Save the combined translations to a single JSON file on Google Drive
with open(output_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(translations, json_file, ensure_ascii=False, indent=4)

# Print a success message
print("Combined translations saved to Google Drive:", output_file_path)
