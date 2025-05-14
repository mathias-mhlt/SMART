from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.preprocessing import OrdinalEncoder
import statsmodels.api as sm
import pandas as pd


def vif_score(path):
    """
    Score de multicolinéarité basé sur le VIF :
      • 1.0 si tous les VIF < 5
      • 0.5 si aucun VIF ≥ 10 mais au moins un VIF ∈ [5,10[
      • 0.0 si au moins un VIF ≥ 10

    Lignes incomplètes (NaN) et colonnes constantes sont simplement supprimées.
    """
    df = pd.read_csv(path)
    #X  = df.drop(columns=df.columns[-1]).copy()  # exclut la dernière colonne (cible)

    #cols = df.columns.tolist()
    #pos = len(df.columns) - 1
    #df.insert(pos, "Ferheineit", df[cols[3]]*(9/5) + 32)  

    #cols_to_drop = [df.columns[-1], df.columns[-9]]

    cols_to_drop = [df.columns[-1]]
    X = df.drop(columns=cols_to_drop).copy()

    cat = X.select_dtypes(exclude="number").columns
    if len(cat):
        enc      = OrdinalEncoder()
        X[cat]   = enc.fit_transform(X[cat])

    X = X.dropna(axis=0, how="any")

    Xc = sm.add_constant(X)
    vifs = pd.Series([variance_inflation_factor(Xc.values, i) for i in range(1, Xc.shape[1])], index=X.columns, name="VIF")
    
    #print(vifs)

    if   (vifs >= 10).any(): return 0.0
    elif (vifs >=  5).any(): return 0.5
    else:                    return 1.0


#print(vif_score("SmartFinal/weatherHistory.csv"))
