import pandas as pd

def analyze_column_types(csv_path, column_name):
    df = pd.read_csv(csv_path)

    if column_name not in df.columns:
        print(f"❌ Column '{column_name}' not found.")
        return

    total = df[column_name].notna().sum()
    int_count = 0
    str_count = 0

    for val in df[column_name].dropna():
        try:
            # Try converting to integer
            if str(val).isdigit():
                int_count += 1
            else:
                str_count += 1
        except:
            str_count += 1

    if total == 0:
        print("⚠️ No non-null values in the column.")
        return

    # Compute percentages
    int_pct = int_count / total * 100
    str_pct = str_count / total * 100

    # print(f"📊 Column: '{column_name}'")
    # print(f"→ Integer-like values: {int_count} ({int_pct:.2f}%)")
    # print(f"→ Non-integer strings: {str_count} ({str_pct:.2f}%)")
    return int_pct, str_pct
# print(f"Integer-like values: {integer_percantage:.2f}%")
# print(f"Non-integer strings: {string_percentage:.2f}%")

integer_percantage,string_percentage = analyze_column_types("data.xls", "Age")
if integer_percantage > string_percentage:
    final_percentage = integer_percantage
else:
    final_percentage = string_percentage
# print(f"Final percentage: {final_percentage:.2f}%")
