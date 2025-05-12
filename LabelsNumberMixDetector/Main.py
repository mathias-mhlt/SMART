import re
import pandas as pd

# Load the CSV data into a DataFrame
data = pd.read_csv("scenario5_label_number_mix.csv")

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

    if has_number and has_string:
        mixed_columns.append((col, num_count, str_count))

# Determine and print the relevant columns
result = []
total_wrongly_attributed_percentage = 0

for col_name, num, strs in mixed_columns:
    wrongly_attributed_percentage = min(strs, num) / (strs + num) * 100

    total_wrongly_attributed_percentage += wrongly_attributed_percentage

    if 30 <= total_wrongly_attributed_percentage <= 70:
        result.append(f"Column '{col_name}' has {wrongly_attributed_percentage:.2f}% wrongly attributed. Result: 0.")
    else:
        result.append(f"Column '{col_name}' has {wrongly_attributed_percentage:.2f}% wrongly attributed. Result: {total_wrongly_attributed_percentage:.2f}%.")

# Print the result or a message if no mixed columns found
if result:
    print('\n'.join(result))
else:
    print("No columns contain both numbers and strings.")
