import pandas as pd
import numpy as np
import regex
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from scipy.spatial.distance import mahalanobis
from scipy.stats import chi2_contingency
from numpy.linalg import pinv

def validate_dataset(file_path="heart.csv",
                     rare_threshold=0.05,
                     z_threshold=3,
                     partial_ratio=0.7,
                     max_typo_distance=1,
                     feature_importance_threshold=0.1,
                     mahalanobis_threshold=3):
    """Dataset validation with explicit feature relationship reporting"""

    df = pd.read_csv(file_path)
    errors = []

    def log_error(row, col, value, issue, details):
        errors.append({
            'row': row, 'column': col, 'value': value,
            'issue': issue, 'details': details
        })

    # 1. Rare Categorical Values
    for col in df.select_dtypes(include=['object', 'category']).columns:
        value_counts = df[col].value_counts(normalize=True)
        rare_values = value_counts[value_counts < rare_threshold].index.tolist()
        for idx, value in df[col].items():
            if value in rare_values:
                log_error(idx, col, value, "Rare categorical value",
                          f"Frequency: {value_counts[value]:.2%} < {rare_threshold:.0%}")

    # 2. Fuzzy Pattern Matching
    for col in df.select_dtypes(include=['object']).columns:
        threshold = len(df) * 0.10
        common_values = df[col].value_counts()
        common_values = common_values[common_values > threshold].nsmallest(5).index.tolist()
        print("Best matches:", common_values)
        if not common_values:
            continue

        patterns = [regex.escape(str(v)) for v in common_values]
        fuzzy_patterns = [rf"(?:{p}){{e<={max_typo_distance}}}" for p in patterns]
        combined_pattern = r"|".join(fuzzy_patterns)

        for idx, value in df[col].items():
            current = str(value).strip()
            if current in common_values:
                continue

            if regex.search(combined_pattern, current, regex.IGNORECASE | regex.BESTMATCH):
                candidates = []
                for pattern in common_values:
                    if len(current) >= len(pattern) * partial_ratio:
                        if regex.search(rf"(?:{regex.escape(pattern)}){{e<={max_typo_distance}}}",
                                        current, regex.IGNORECASE):
                            candidates.append(pattern)

                if candidates:
                    best_matches = sorted(candidates, key=lambda x: (-len(x), -common_values.index(x)))[:3]
                    log_error(idx, col, value, "Potential typo",
                              f"Similar to: {', '.join(best_matches)}")

    # 3. Numerical Outliers
    for col in df.select_dtypes(include=np.number).columns:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        median = df[col].median()
        mad = (df[col] - median).abs().median()
        modified_z = 0.6745 * (df[col] - median) / mad

        for idx, (value, z) in enumerate(zip(df[col], modified_z)):
            if abs(z) > z_threshold and (value < (q1-1.5*iqr) or value > (q3+1.5*iqr)):
                log_error(idx, col, value, "Numerical outlier",
                          f"Z: {z:.1f}, IQR: [{q1-1.5*iqr:.1f}-{q3+1.5*iqr:.1f}]")

    # 4. Enhanced Multivariate Analysis
    target_col = next((col for col in df.columns if df[col].nunique() < len(df)//2 and
                       df[col].dtype in ['object', 'category']), None)

    if target_col:
        X = df.drop(columns=[target_col])
        y = df[target_col]
        le = LabelEncoder()
        encoded_y = le.fit_transform(y)

        # Feature importance analysis
        model = RandomForestClassifier(n_estimators=50)
        numeric_cols = X.select_dtypes(include=np.number).columns
        model.fit(X[numeric_cols], encoded_y)
        num_importances = pd.Series(model.feature_importances_, index=numeric_cols)
        important_features = num_importances[num_importances > feature_importance_threshold].index.tolist()

        # Calculate class statistics
        class_stats = {}
        for cls in df[target_col].unique():
            cls_data = df[df[target_col] == cls][important_features]
            if len(cls_data) > 1:
                try:
                    cov_matrix = cls_data.cov()
                    inv_cov = pinv(cov_matrix + 1e-6*np.eye(cov_matrix.shape[0]))  # Regularized inverse
                    class_stats[cls] = {
                        'mean': cls_data.mean().values,
                        'inv_cov': inv_cov,
                        'features': important_features
                    }
                except Exception as e:
                    continue

        # Validate instances
        for idx, row in df.iterrows():
            cls = row[target_col]
            if cls not in class_stats:
                continue

            stats = class_stats[cls]
            try:
                values = row[stats['features']].values.astype(float)
                mahal_dist = mahalanobis(values, stats['mean'], stats['inv_cov'])

                if mahal_dist > mahalanobis_threshold:
                    # Create detailed comparison
                    comparisons = [
                        f"{feat}: {row[feat]} (class avg: {stats['mean'][i]:.2f})"
                        for i, feat in enumerate(stats['features'])
                    ]

                    log_error(
                        idx,
                        ', '.join(stats['features']),  # Show all involved features
                        None,
                        "Feature relationship anomaly",
                        f"Mahalanobis distance: {mahal_dist:.2f} | " +
                        f"Feature comparisons: {'; '.join(comparisons)}"
                    )
            except Exception as e:
                continue

    # Reporting
    if errors:
        error_df = pd.DataFrame(errors)
        print(f"\nFound {len(error_df)} potential issues:")
        print("=" * 60)
        print(error_df[['row', 'column', 'issue', 'details']]
              .sort_values(['row', 'column'])
              .head(20)
              .to_string(index=False, max_colwidth=60))
        print("\nIssue Type Summary:")
        print(error_df['issue'].value_counts().to_string())
        return error_df
    else:
        print("\nNo data quality issues detected!")
        return None

if __name__ == "__main__":
    validate_dataset()