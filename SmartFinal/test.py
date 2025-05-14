import tempfile, os, matplotlib.pyplot as plt
import numpy as np, pandas as pd
from random_forest import random_forest
from DIversificationScore import global_dataset_score
import random


def random_na(df, n_min=1, n_max=None, max_cols=None, seed=None):

    rng = np.random.default_rng(seed)

    feat_cols = df.columns[:-1]
    n_feat    = len(feat_cols)

    if max_cols is None or max_cols > n_feat:
        max_cols = n_feat

    k = rng.integers(1, max_cols + 1) 

    chosen_cols = rng.choice(feat_cols, size=k, replace=False)

    if n_max is None or n_max > (len(df) - 1):
        n_max = (len(df) - 1) // 2
    n_max = max(n_max, n_min)

    for col in chosen_cols:
        n_rows_col = rng.integers(n_min, n_max + 1)
        idx        = rng.choice(df.index, size=n_rows_col, replace=False)
        df.loc[idx, col] = np.nan

    return df





def score_vs_auc(path, N=5, seed=42):
    rng   = np.random.default_rng(seed)
    base  = pd.read_csv(path)

    scores, aucs = [], []

    for _ in range(N):
        df = base.copy()
        random_na(df, seed=int(rng.integers(1e9)))

        tmp_path = tempfile.mktemp(suffix=".csv")
        df.to_csv(tmp_path, index=False)

        scores.append(global_dataset_score(tmp_path))
        aucs.append(random_forest(tmp_path))

        os.remove(tmp_path)

    plt.figure(figsize=(6, 4))
    plt.scatter(scores, aucs, alpha=0.7)
    plt.xlabel("Score complétude 1")
    plt.ylabel("Précision Random Forest")
    plt.title(f"Impact de la complétude sur la précision (N={N})")
    plt.grid(True)
    plt.show()

    return pd.DataFrame({"score completude 1": scores, "precision": aucs})


res = score_vs_auc("heart.csv", N=30, seed=2025)
print(res.head())
