from MixedColumnDetector import res
from Z_Score import printresult
from CompletnessPart1 import completeness_score
from consistent_representation_score import consistent_representation_score
from DIversificationScore import global_dataset_score
from columnCompletness import column_completeness

import pandas as pd
import numpy as np
import random

# Load the dataset
df = pd.read_csv("heart.csv")

# Corrupt the 'Age' column (numeric) by inserting strings like 'M', 'F'
for i in df.index:
    if random.random() < 0.1:  # 30% corruption rate
        df.at[i, 'Age'] = random.choice(['M', 'F', 'ATA', 'NAP'])

# Corrupt the 'Sex' column (categorical) by inserting numbers like ages
for i in df.index:
    if random.random() < 0.3:  # 30% corruption rate
        df.at[i, 'Sex'] = random.randint(20, 80)

# Save the corrupted dataset
df.to_csv("corrupted_heart.csv", index=False)

# Define numeric columns to inject outliers into
numeric_columns = ['Age', 'RestingBP', 'Cholesterol', 'MaxHR', 'Oldpeak']

# Inject a lot of extreme outliers
for col in numeric_columns:
    for i in df.index:
        if random.random()*100 < 60:  # 40% chance to turn a value into an outlier
            try:
                # Skip non-numeric cells (already corrupted)
                float(df.at[i, col])
                # Inject an extreme outlier
                df.at[i, col] = random.choice([9999])
            except:
                continue  # If the cell is not numeric, skip

# Save the dataset with outliers
df.to_csv("outliers_heart.csv", index=False)


# Insert NaN values in dataset
def random_na(df, n=None, max_cols=None, seed=None):
    rng = np.random.default_rng(seed)
    if n is None:
        n = random.randint(1, (df.shape[0] - 1) // 2)
    if max_cols is None:
        max_cols = random.randint(1, df.shape[1] - df.shape[1] // 3)
    col_names = rng.choice(df.columns, size=max_cols, replace=False)
    for col in col_names:
        idx = rng.choice(df.index, size=n, replace=False)
        df.loc[idx, col] = np.nan
        
random_na(df) 




outliersZcoreScore = res('outliers_heart.csv') 
outliersColumnsScore = printresult('outliers_heart.csv') 
diversityScore = global_dataset_score('outliers_heart.csv')
cellsCompletnessScore = completeness_score('outliers_heart.csv')
columnCompletnessScore = column_completeness('outliers_heart.csv')
consistentRepresentationScore = consistent_representation_score('outliers_heart.csv') #entre 0 et 1
print(outliersZcoreScore)
print(outliersColumnsScore)
print(diversityScore)
print(cellsCompletnessScore)
print(columnCompletnessScore)
print(consistentRepresentationScore)


print("Score final :"+str(outliersZcoreScore + outliersColumnsScore + diversityScore + cellsCompletnessScore + columnCompletnessScore + consistentRepresentationScore))
