from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.preprocessing import OrdinalEncoder
import statsmodels.api as sm
import pandas as pd

def vif_score(path):
    """
    Renvoie un score de redondance basé sur les VIF :
        - 1.0 si toutes les colonnes ont VIF < 5
        - 0.5 si aucune ≥ 10 mais au moins une entre [5, 10[
        - 0.0 si au moins une colonne a un VIF ≥ 10
    """

    dataset = pd.read_csv(path)

    cols = dataset.columns.tolist()

    pos = len(dataset.columns) - 1
    dataset.insert(pos, "Duplicat", dataset[cols[-5]])  

    cat_cols = dataset.select_dtypes(include="object").columns

    enc = OrdinalEncoder()
    dataset[cat_cols] = enc.fit_transform(dataset[cat_cols])

    for col, cats in zip(cat_cols, enc.categories_):
        mapping = {cat: int(code) for code, cat in enumerate(cats)}

    X_feat = dataset.drop(columns=dataset.columns[-1])

    Xc = sm.add_constant(X_feat)
    vifs = pd.Series([variance_inflation_factor(Xc.values, i) for i in range(1, Xc.shape[1])], index=X_feat.columns)

    if (vifs >= 10).any():
        return 0.0
    elif (vifs >= 5).any():
        return 0.5
    else:
        return 1.0
