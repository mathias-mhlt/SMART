import numpy as np
import pandas as pd
from scipy.stats import norm, chi2, chisquare
from scipy.spatial.distance import jensenshannon
from pingouin import partial_corr


def dispersion_numeric(arr, p=0.10, n_iter=5000, alpha=0.05, q_tol=0.10):
    n, k, ok_cnt = len(arr), int(p * len(arr)), 0
    z = norm.ppf(1 - alpha / 2)

    for _ in range(n_iter):
        idx_test = np.random.choice(n, size=k, replace=False)
        idx_ref  = np.setdiff1d(np.arange(n), idx_test)
        test, ref = arr[idx_test], arr[idx_ref]

        # moyenne
        m_ref, s_ref = ref.mean(), ref.std(ddof=1)
        ic_mean = (m_ref - z * s_ref / np.sqrt(len(ref)),
                   m_ref + z * s_ref / np.sqrt(len(ref)))
        ok_mean = ic_mean[0] <= test.mean() <= ic_mean[1]

        # variance
        v_ref, df_ref = s_ref**2, len(ref) - 1
        chi_low = chi2.ppf(alpha / 2, df_ref)
        chi_up  = chi2.ppf(1 - alpha / 2, df_ref)
        ic_var  = ((df_ref * v_ref) / chi_up, (df_ref * v_ref) / chi_low)
        ok_var  = ic_var[0] <= test.var(ddof=1) <= ic_var[1]

        # quartiles
        q_ref  = np.percentile(ref, [25, 50, 75])
        q_test = np.percentile(test, [25, 50, 75])
        tol    = q_tol * (q_ref[2] - q_ref[0])
        ok_q   = np.all(np.abs(q_test - q_ref) <= tol)

        if sum([ok_mean, ok_var, ok_q]) >= 2:
            ok_cnt += 1

    return ok_cnt / n_iter


def dispersion_categorical(series, p=0.10, n_iter=5000, alpha=0.05, js_thresh=0.05):
    s = series.dropna()
    n, k = len(s), int(p * len(s))
    cats = s.unique()
    ok_cnt = 0

    for _ in range(n_iter):
        idx_test = np.random.choice(n, size=k, replace=False)
        idx_ref  = np.setdiff1d(np.arange(n), idx_test)
        f_test   = s.iloc[idx_test].value_counts().reindex(cats, fill_value=0)
        f_ref    = s.iloc[idx_ref].value_counts().reindex(cats, fill_value=0)

        p_test, p_ref = f_test / f_test.sum(), f_ref / f_ref.sum()

        # Ki2
        exp_test = p_ref * f_test.sum()
        chi2_stat, p_val = chisquare(f_test, exp_test)
        ok_chi = p_val >= alpha

        # JS
        ok_js = jensenshannon(p_test, p_ref) <= js_thresh

        if ok_chi and ok_js:
            ok_cnt += 1

    return ok_cnt / n_iter



def global_dataset_score(path, p=0.10, n_iter=5000, alpha=0.05, q_tol=0.10, js_thresh=0.05):
    # Lecture
    df = pd.read_csv(path)

    target = df.columns[-1]

    # Encodage simple des catégorielles pour les corrélations
    df_enc = df.copy()
    cat_cols_enc = df_enc.select_dtypes(exclude="number").columns.difference([target])
    df_enc[cat_cols_enc] = df_enc[cat_cols_enc].apply(lambda c: c.astype("category").cat.codes)

    # Importance (corrélations partielles)
    X_cols = df_enc.columns.difference([target])
    partials = {}
    for col in X_cols:
        others = [c for c in X_cols if c != col]
        res = partial_corr(data=df_enc, x=col, y=target, covar=others, method="spearman")
        partials[col] = res.iloc[0]["r"] if not res.empty else np.nan
    importance = pd.Series(partials).abs().dropna()

    # Stabilité / dispersion
    num_cols = df.select_dtypes(include="number").columns.difference([target])
    cat_cols = df.select_dtypes(exclude="number").columns.difference([target])

    stability_num = { col: dispersion_numeric(df[col].dropna().values, p=p, n_iter=n_iter, alpha=alpha, q_tol=q_tol) for col in num_cols}
    stability_cat = {col: dispersion_categorical(df[col], p=p, n_iter=n_iter, alpha=alpha, js_thresh=js_thresh) for col in cat_cols}
    stability = pd.Series({**stability_num, **stability_cat})

    # Fusion & score global
    df_all = pd.concat([stability.rename("stability"), importance.rename("importance")], axis=1).dropna()
    df_all["score_abs"] = df_all["stability"] * df_all["importance"]

    score_global = df_all["score_abs"].sum() / df_all["importance"].sum()
    return score_global

