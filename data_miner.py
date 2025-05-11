import json
from collections import Counter
from write_to_csv import *
from typing import List, Dict, Any
import pandas as pd

# from open_ai_call import get_response
# from google_gemini_call import get_response
from claude_assessment import get_assessment




VERSIONS = ['v1','v2','v3', 'v4', 'v5']


def load_jsonl_data(filepath):
    """Loads data from a JSON Lines (.jsonl) file into a list of dictionaries.

    Args:
        filepath: The path to the .jsonl file.

    Returns:
        A list of dictionaries, where each dictionary represents a line in the file.
        Returns an empty list if there's an error opening or reading the file,
        or if the file is empty.  Prints an error message to the console.
    """
    data = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:  # Important: Specify UTF-8 encoding
            for line in f:
                try:
                    # Attempt to parse each line as JSON. Handle potential JSONDecodeErrors
                    item = json.loads(line.strip())  # Remove leading/trailing whitespace
                    data.append(item)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON on line: {line.strip()}")
                    print(f"Error details: {e}")
                    # Consider appending a None or a placeholder to maintain line count
                    # data.append(None)  % Or: data.append({"error": str(e)})
                    # Or simply skip the problematic line and continue.
                    continue  # Skips to the next line
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
    except Exception as e:  # Catch other potential exceptions (e.g., permission errors)
        print(f"An error occurred: {e}")

    return data


def jsonl_to_json(source, target):
    """
    Converts a JSON Lines (.jsonl) file into a structured JSON format.

    This function loads data from a .jsonl file, filters out posts where:
    - The post is not removed by moderators.
    - The author has only one post in the dataset.
    - The combined title and selftext have fewer than 128 words.

    The filtered data is saved in a dictionary with the author's name as the key.

    Args:
        source (str): Path to the input .jsonl file.
        target (str): Path to save the output JSON file.

    Returns:
        None: Writes filtered data to the specified target JSON file.

    Example:
        jsonl_to_json("input.jsonl", "output.json")
    """
    # Example usage:
    loaded_data = load_jsonl_data(source)

    user_post_counts = Counter([x['author'] for x in loaded_data])

    filtered_data = {}
    for item in loaded_data:
        # print(item['author'], item['title'], item['selftext'])
        if not item['removed_by_category'] and user_post_counts[item['author']] == 1:
            body = item['title'] + ' ' + item['selftext']
            if len(body.split(' ')) < 128:
                filtered_data[item['author']] = {'content': body, 'url': item['url'], 'created': item['created']}

    with open(target, "w") as f:
        json.dump(filtered_data, f, indent=4)

    print(f"Total Data: {len(filtered_data)}")
    print(f"Total Rows Processed: {len(loaded_data)}")


def load_json(filepath: str):
    """
    Loads a JSON file and returns its contents.

    Args:
        filepath (str): The path to the JSON file.

    Returns:
        Any: The parsed JSON data, which could be a dictionary or list.
             Returns None if the file is missing or contains invalid JSON.

    Example:
        data = load_json("config.json")
    """
    try:
        with open(filepath, 'r', encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found - {filepath}")
    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse JSON in {filepath} - {e}")
    except Exception as e:
        print(f"Unexpected error while reading {filepath}: {e}")

    return None  # Return None if an error occurs.


def get_llm_eval(data: Dict[str, Any], start: int, stop: int, step: int = 100, llm='gpt_labels') -> None:
    """Evaluate data using LLM and store results in JSON files."""
    i = 0
    while start < stop:
        new_data = {}
        try:
            for k in sorted(data.keys())[start:start + step]:
                i += 1
                print(i)
                new_data[k] = {'content': data[k]['content']}
                response = get_assessment(data[k]['content'])

                try:
                    parsed_response = json.loads(response)
                    new_data[k]['severity_score'] = parsed_response['severity']
                    # new_data[k]['response'] = json.dumps(parsed_response, indent=4)
                except (json.JSONDecodeError, KeyError) as e:
                    print(f"Error parsing LLM response: {e}")

        except Exception as e:
            print(f"Unexpected error in LLM evaluation: {e}")

        with open(f"{llm}/llm-eval-{start}-{start + step}.json", "w", encoding="utf-8") as f:
            json.dump(new_data, f, indent=4)

        start += step
        if start < stop:
            print('Processing Batch: ', start, start-step)
    print("LLM evaluation complete.")


def combine_dump(version: str, start: int, end: int, step: int = 100, llm='gpt_labels') -> None:
    """Combine JSON dumps into a single file."""
    combined_data = {}
    for i in range(start, end, step):
        combined_data.update(load_json(f'{llm}/llm-eval-{i}-{i + step}.json'))

    with open(f'{llm}/{version}_labels/llm-eval-{start}-{end}.json', 'w', encoding="utf-8") as f:
        json.dump(combined_data, f, indent=4)


def combine_ratings(start: int, stop: int, llm='gpt_labels') -> None:
    res_set = load_json(f'{llm}/v1_labels/llm-eval-{start}-{stop}.json')
    res = {k: {} for k in res_set}

    for k, v in res_set.items():
        print(k)
        del(res_set[k]['severity_score'])

    for version in VERSIONS:
        lbl_set = load_json(f'{llm}/{version}_labels/llm-eval-{start}-{stop}.json')
        for k in res:
            print(version, k)
            res_set[k][f'{version}_label'] = int(lbl_set[k]['severity_score'])

    with open(f'combined_labels/llm-eval-{start}-{stop}-combined-{llm}.json', 'w') as f:
        json.dump(res_set, f, indent=4)


def consistent_labels_to_csv(start: int, stop: int, filename: str) -> None:
    res = []
    labels = [f'{v}_label' for v in VERSIONS]
    total = 0
    with open(f'combined_labels/llm-eval-{start}-{stop}-combined.json', 'r') as f:
        data = json.load(f)

    with open('input_additional.json', 'r') as f:
        post_details = json.load(f)

    for author, dkt in data.items():
        x = [dkt[v_lbl] for v_lbl in labels]
        if x.count(x[0]) == len(x):
            total += 1
            tmp = {'id':total, 'author': str(author.replace('=-','')), 'content': dkt['content'], 'url': post_details[author]['url'],
                   'created': post_details[author]['created'], 'severity': x[0]}
            res.append(tmp)

    write_dict_list_to_csv(res, filename)
    print(total)


def label_posts(start: int, end: int, llm = 'gpt_labels') -> None:
    """Label posts using different versions."""
    for version in VERSIONS:
        data = load_json('llm-input.json')
        if data:
            get_llm_eval(data, start, end, llm=llm)
            combine_dump(version, start, end, llm=llm)


def combine_predictions() -> None:
    # Load CSV into a dictionary
    csv_file_path = "labeled_reddit_posts_reviewed.csv"  # Replace with your file path
    data_dict = {}

    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)  # Reads the CSV as a dictionary
        for row in reader:
            key = row['author']  # Replace 'author' with the column you want as the key
            data_dict[key] = row  # Store the row in the dictionary

    with open('combined_labels/llm-eval-0-3000-combined-gemini_labels.json', 'r', encoding='utf-8') as f:
        gemini_data = json.load(f)

    for k,v in data_dict.items():
        print(k)
        # Code for SOTC
        voted_severity = Counter([gemini_data[k][f'v{i}_label'] for i in range(1,6)]).most_common()[0][0]
        v['gemini_label'] = voted_severity
        field_names = list(v.keys())

    with open('output.csv', mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=field_names)

        # Write the header
        writer.writeheader()

        # Write the rows
        for row in data_dict.values():
            writer.writerow(row)


# Load JSON list and dump information in dictionary format to input json.
# jsonl_to_json('r_SuicideWatch_posts_12.jsonl', 'llm-input.json')

# Load posts, label posts from start to end index. save them in the versioned folder.
label_posts(start=0, end=3000, llm='ds_labels')
# combine_ratings(start=0, stop=3000, llm='gemini_labels')
# consistent_labels_to_csv(start=0, stop=3000, filename='labeled_reddit_posts_all.csv')
# combine_predictions()

# print(get_consitent_ratings())
