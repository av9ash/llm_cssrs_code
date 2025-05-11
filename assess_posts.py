import json
import csv
import re
from copy import deepcopy
from tqdm import tqdm
import matplotlib.pyplot as plt

# from claude_assessment import get_assessment
# from llama_assessment import get_assessment
# from mistral_assessment import get_assessment
# from gpt_assessment import get_assessment
from gemini_assessment import get_assessment

def extract_severity(text):
    """Extracts integer severity value from JSON-like text."""
    match = re.search(r'"severity"\s*:\s*(\d+)', text)
    return int(match.group(1)) if match else None


def save_json_checkpoint(data, path):
    """Saves current progress to a JSON file."""
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)


def process_csv(input_path, output_path, response_path, model_name):
    label_column = f"{model_name}_label"
    response_column = f"{model_name}_response"
    full_responses = []

    with open(input_path, mode='r', newline='', encoding='utf-8') as infile, \
         open(output_path, mode='w', newline='', encoding='utf-8') as outfile:

        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + [label_column]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for idx, row in enumerate(tqdm(reader, desc="Processing rows")):
            if idx > 169:
                original_row = deepcopy(row)
                assessment = get_assessment(row['content'])

                original_row[response_column] = assessment
                full_responses.append(original_row)

                row[label_column] = extract_severity(assessment)
                writer.writerow(row)

                # Periodic checkpointing every 10 rows
                if (idx + 1) % 10 == 0:
                    save_json_checkpoint(full_responses, response_path)

    # Final save
    save_json_checkpoint(full_responses, response_path)
    print(f"Updated CSV saved as: {output_path}")


if __name__ == "__main__":
    model = 'gemini'
    input_csv = 'labeled_posts_full_set_manual.csv'
    output_csv = f'labeled_posts_{model}.csv'
    json_output = f'{model}_assessment.json'

    process_csv(input_csv, output_csv, json_output, model)
