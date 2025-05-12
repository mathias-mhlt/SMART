import re
import pandas as pd


def res(path):
    # Load the CSV data into a DataFrame
    data = pd.read_csv(path)

    # Regular expression to match numeric values (integers and decimals)
    numeric_pattern = re.compile(r'^[+-]?\d+(?:\.\d+)?$')

    mixed_columns = []

    # Analyze each column
    for col in data.columns:
        col_data = data[col].astype(str)  # Convert all values to strings for regex matching

        num_count = 0
        str_count = 0
        has_number = False
        has_string = False

        for val in col_data:
            if numeric_pattern.match(val):
                num_count += 1
                has_number = True
            else:
                str_count += 1
                has_string = True

        if has_number or has_string:
            mixed_columns.append((col, num_count, str_count))
    # Determine and print the relevant columns
    result = []

    total_wrongly_attributed_percentage = 0
    for col_name, num, strs in mixed_columns:
        wrongly_attributed_percentage = min(strs, num) / (strs + num) * 100
        total_wrongly_attributed_percentage += wrongly_attributed_percentage
        if 10 <= total_wrongly_attributed_percentage <= 90:
            return 0
        else:
            return 1
