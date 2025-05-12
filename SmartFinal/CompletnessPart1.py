import pandas as pd
import numpy as np

def completeness_score(path):

    df = pd.read_csv(path)

    missing_tokens = ["", " ", "NA", "Na", "N/A", "NULL", "null", "-", "?"]
    df.replace(missing_tokens, np.nan, regex=False, inplace=True)
    df.replace(r"^\s+$", np.nan, regex=True, inplace=True)

    target_col = df.columns[-1]

    n = len(df)
    feat_cols    = df.columns.drop(target_col)
    missing_frac = df[feat_cols].isna().sum() / n
    compl_by_col = 1 - missing_frac
    compl_global = compl_by_col.mean()

    return compl_global