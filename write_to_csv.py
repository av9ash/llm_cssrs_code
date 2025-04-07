import csv

def write_dict_list_to_csv(data, filename):
    if not data:
        print("No data provided.")
        return

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())

        # Write the header
        writer.writeheader()

        # Write the data rows
        writer.writerows(data)


def write_dict_to_csv(data, filename):
    if not data:
        print("No data provided.")
        return

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())

        # Write the header
        writer.writeheader()

        # Write the data row
        writer.writerow(data)


def read_csv_file(file_path):
    """
    Reads a CSV file and prints its contents.

    Args:
        file_path (str): The path to the CSV file.
    """

    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        return csv_reader


# # Example usage
# data = [
#     {"Name": "Alice", "Age": 25, "City": "New York"},
#     {"Name": "Bob", "Age": 30, "City": "San Francisco"},
#     {"Name": "Charlie", "Age": 35, "City": "Los Angeles"}
# ]
#
# write_dict_list_to_csv(data, "output.csv")