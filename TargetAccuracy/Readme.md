This document outlines the automated validation criteria used for detecting common data quality issues.
The system checks for:

- Rare categorical values/Numerical outliers
- Simple pattern mismatches and typos
- Feature relationship anomalies

=========================================
2. Validation Criteria
=========================================

-----------------------------------------
2.1 Rare Categorical Values
-----------------------------------------

- Purpose:
  Detect infrequently occurring categorical values.

- Methodology:
  A value is considered rare if:

      Count(value) / Total Rows < τ_rare

- Parameters:
  - τ_rare (frequency threshold): Default = 0.05

- Example:
  A label like "werewolf" appearing in only 0.1% of rows.

-----------------------------------------
2.2 Fuzzy Pattern Matching
-----------------------------------------

- Purpose:
  Detect typos and value variations.

- Methodology (Pseudo-code):

    1. Extract top 5 most frequent values
    2. Generate regex patterns with 1-character edit distance
    3. Match using: (?:pattern){e<=1}
    4. Check: length(value) >= ρ * length(pattern)

- Parameters:
  - Max edit distance: 1
  - Partial ratio ρ: 0.7

- Example:
  "ATAA" flagged as possible typo of "ATA".

-----------------------------------------
2.3 Numerical Outliers
-----------------------------------------

- Purpose:
  Detect extreme numerical values.

- Methodology:

    Modified Z-score = 0.6745 * (x - median) / MAD  
    IQR = Q3 - Q1

- Parameters:
  - Z-score threshold: 3
  - IQR outlier range: [Q1 - 1.5 * IQR, Q3 + 1.5 * IQR]

- Example:
  Weight = 10kg in a dataset where 99% are between 50–100kg.

-----------------------------------------
2.4 Feature Relationship Anomalies
-----------------------------------------

- Purpose:
  Detect illogical combinations of feature values.

- Methodology:

    Mahalanobis Distance:
        D_M = sqrt((x - μ)^T * Σ^(-1) * (x - μ))

  Where:
    - D_M = Mahalanobis distance
    - μ = Mean vector
    - Σ = Covariance matrix

- Parameters:
  - Feature importance threshold: 0.1
  - Mahalanobis distance threshold: 3

- Example:
  "Werewolf" with weight=15kg and height=0.4m matches dog profile.

=========================================
3. Summary Table
=========================================

| Criterion      | Metric            | Threshold | Detection Example               |
|----------------|-------------------|-----------|---------------------------------|
| Rarity         | Frequency          | < 5%      | Rare category values            |
| Typo           | Edit distance      | 1         | "ATAA" → "ATA"                  |
| Outlier        | Modified Z-score   | > 3       | Extreme numerical values        |
| Relationships  | Mahalanobis        | > 3       | Invalid feature combinations    |

=========================================
4. Implementation Notes
=========================================

- Univariate Checks: Applied per column.
- Multivariate Analysis: Validates relationships across features.
- Adaptive Thresholds: Parameters can be configured per dataset.
- Context Awareness: Class-specific pattern validation.

=========================================
