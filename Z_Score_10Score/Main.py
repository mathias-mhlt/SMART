import pandas as pd
import numpy as np
from scipy import stats

# Load dataset
df = pd.read_csv('Heart.csv')

# Select numeric columns
numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()

outliers_info = {}

for col in numerical_cols:
    # Convert to numeric and drop NaNs
    df[col] = pd.to_numeric(df[col], errors='coerce')
    data = df[col].dropna()

    if len(data) < 1:
        print(f"Column '{col}' has no non-NaN values. Skipping.")
        outliers_info[col] = {'outlier_count': 0, 'outlier_score': 1.0}
        continue

    # Calculate Z-scores and identify outliers
    z_scores = np.abs(stats.zscore(data))
    threshold = 3
    outlier_mask = z_scores > threshold
    outlier_count = np.sum(outlier_mask)
    total_valid = len(data)
    outlier_score = 1 - (outlier_count / total_valid) if total_valid != 0 else 1.0

    # Store results
    outliers_info[col] = {
        'outlier_count': outlier_count,
        'outlier_score': outlier_score
    }

    # Print details
    print(f"\nColumn: {col}")
    print(f"Outliers (Z > {threshold}):")
    print(df.loc[data.index[outlier_mask], col])
    print(f"Outlier Score: {outlier_score:.4f}")

# Convert results to DataFrame for clarity
outliers_df = pd.DataFrame.from_dict(outliers_info, orient='index')
outliers_df['total_non_nan'] = [len(df[col].dropna()) for col in numerical_cols]

print("\nOutlier Summary:")
print(outliers_df[['outlier_score']].mean())