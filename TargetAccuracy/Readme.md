1 Validation Criteria
=========================================

-----------------------------------------
1.1 Rare Categorical Values
-----------------------------------------

- Purpose:
  Detect infrequently occurring categorical values.

- Methodology:
  A value is considered rare if:

      Count(value) / Total Rows < τ_rare

- Parameters:
  - τ_rare (frequency threshold): Default = 0.05

-----------------------------------------
1.2 Fuzzy Pattern Matching
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
1.3 Numerical Outliers
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
1.4 Feature Relationship Anomalies
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
