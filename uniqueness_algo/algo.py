import pandas as pd

#https://arxiv.org/pdf/2207.14529

def calculate_uniqueness(csv_path):
    # READ CSV
    df = pd.read_csv(csv_path)

    # ALL ROWS
    n = len(df)

    if n <= 1:
        print("not enough rows to compute uniqueness of data set.")
        return None

    # UNIQUENESS BASED ON ROWS
    unique_rows = df.drop_duplicates()
    num_unique = len(unique_rows)

    # NORMALIZED UNIQUENESS
    uniqueness = (num_unique - 1) / (n - 1)

    print(f"uniqueness of data set: {uniqueness:.4f}")
    return uniqueness

# CALL:
# ADAPT YOUR CSV-FILE NAME HERE!
csv_datei = 'scenario3_one_correlated.csv'
calculate_uniqueness(csv_datei)