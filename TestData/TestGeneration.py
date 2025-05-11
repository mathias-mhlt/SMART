import pandas as pd
import numpy as np
import random
from sklearn.preprocessing import LabelEncoder

# Load the original dataset
df = pd.read_csv("heart.csv")

# Define categorical and numerical columns
categorical_cols = ['Sex', 'ChestPainType', 'RestingECG', 'ExerciseAngina', 'ST_Slope']
numerical_cols = [col for col in df.columns if col not in categorical_cols and col != 'HeartDisease']

# Encode categorical variables for internal use
label_encoders = {col: LabelEncoder().fit(df[col]) for col in categorical_cols}
encoded_df = df.copy()
for col in categorical_cols:
    encoded_df[col] = label_encoders[col].transform(df[col])

# Scenario 1: Fully random (same values, no correlation)
def generate_fully_random():
    random_df = df.copy()
    for col in categorical_cols:
        random_df[col] = np.random.choice(df[col].unique(), size=len(df))
    for col in numerical_cols:
        random_df[col] = np.random.choice(df[col].values, size=len(df))
    random_df['HeartDisease'] = np.random.choice(df['HeartDisease'].values, size=len(df))
    random_df.to_csv("scenario1_fully_random.csv", index=False)

# Scenario 2: Correlated columns (simulate correlation)
def generate_correlated():
    correlated_df = df.copy()
    base = encoded_df[numerical_cols].copy()
    base = (base - base.mean()) / base.std()
    weights = np.random.rand(len(numerical_cols))
    correlated_base = base @ weights
    for col in numerical_cols:
        correlated_df[col] = correlated_base + np.random.normal(0, 0.1, size=len(df))
    for col in categorical_cols:
        correlated_df[col] = df[col]
    correlated_df['HeartDisease'] = df['HeartDisease']
    correlated_df.to_csv("scenario2_correlated.csv", index=False)

# Scenario 3: One correlated feature, rest random
def generate_one_correlated():
    correlated_col = 'MaxHR'
    random_df = df.copy()
    base = encoded_df[numerical_cols].copy()
    weights = np.random.rand(len(numerical_cols))
    correlated_values = base @ weights + np.random.normal(0, 0.1, size=len(df))
    for col in numerical_cols:
        if col == correlated_col:
            random_df[col] = correlated_values
        else:
            random_df[col] = np.random.choice(df[col].values, size=len(df))
    for col in categorical_cols:
        random_df[col] = np.random.choice(df[col].values, size=len(df))
    random_df['HeartDisease'] = np.random.choice(df['HeartDisease'].values, size=len(df))
    random_df.to_csv("scenario3_one_correlated.csv", index=False)

# Scenario 4: Overproportionate / scaled numerical values
def generate_scaled_extremes():
    scaled_df = df.copy()
    for col in numerical_cols:
        scale_factors = np.random.choice([0.1, 1, 10, 100], size=len(df))
        scaled_df[col] = df[col] * scale_factors
    scaled_df.to_csv("scenario4_scaled_extremes.csv", index=False)

# Scenario 5: Mix labels into numerical columns
def generate_label_number_mix():
    mixed_df = df.copy()
    label_source = df['ChestPainType'].unique()
    mixed_cols = random.sample(numerical_cols, k=3)
    for col in mixed_cols:
        mixed_df[col] = np.random.choice(label_source, size=len(df))
    mixed_df.to_csv("scenario5_label_number_mix.csv", index=False)

# Scenario 6: Creative – Simulate noise spikes in MaxHR based on odd/even row
def generate_creative_noise():
    noise_df = df.copy()
    noise_df['MaxHR'] = df['MaxHR'] + np.where(noise_df.index % 2 == 0,
                                               np.random.normal(50, 10, size=len(df)),
                                               np.random.normal(-50, 10, size=len(df)))
    noise_df.to_csv("scenario6_creative_noise.csv", index=False)

# Generate all scenarios
generate_fully_random()
generate_correlated()
generate_one_correlated()
generate_scaled_extremes()
generate_label_number_mix()
generate_creative_noise()

print("All synthetic datasets generated.")
