from MixedColumnDetector import res
from Z_Score import printresult
from Rarity import score_calculation

import pandas as pd
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

result = res('outliers_heart.csv')
result1 = printresult('outliers_heart.csv')
print(result)
print(result1)

finalresult = result
print("Score final :"+str(result+result1))