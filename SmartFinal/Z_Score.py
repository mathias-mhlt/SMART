import pandas as pd
import numpy as np
from scipy import stats

def printresult(path):
    # Load dataset
    df = pd.read_csv(path)

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
        #print(z_scores)
        threshold = 1
        outlier_mask = z_scores > threshold
        outlier_count = np.sum(outlier_mask)
        total_valid = len(data)
        outlier_score = 1 - (outlier_count / total_valid) if total_valid != 0 else 1.0
        return outlier_score