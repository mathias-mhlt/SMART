import numpy as np 
import pandas as pd 
from sklearn.preprocessing import LabelEncoder


def cohens_d(group1, group2):
    mean1, mean2 = np.mean(group1), np.mean(group2)
    var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
    n1, n2 = len(group1), len(group2)
    pooled_std = np.sqrt(((n1-1)*var1 + (n2-1)*var2) / (n1+n2-2))
    
    d = abs(mean1 - mean2) / pooled_std
    return d

def size(donnees):
    df=pd.read_csv(donnees)
    df.head()
    string_col = df.select_dtypes(include="object").columns
    df[string_col]=df[string_col].astype("string")
    df.dtypes
    # df_tree=pd.get_dummies(df,columns=string_col,drop_first=False)
    # df_tree.head()

    df_tree = df.apply(LabelEncoder().fit_transform)
    df_tree.head()

    target = df.columns[-1]
    X = df.drop(target, axis=1)
    y = df[target]

    numeric_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()

    effect_sizes = {}
    for col in numeric_cols:
        group0 = df[df[target] == 0][col].values
        group1 = df[df[target] == 1][col].values
        effect_sizes[col] = cohens_d(group0, group1)

    effect_sizes_df = pd.DataFrame(list(effect_sizes.items()), columns=['Facteur', "Taille d'effet"])
    effect_sizes_df = effect_sizes_df.sort_values("Taille d'effet", ascending=False)
    moyenne = effect_sizes_df["Taille d'effet"].mean()

    #print("Tailles d'effet selon l'échelle de Cohen:")
    #print(effect_sizes_df)
    #print(f"Taille d'effet moyenne: {effect_sizes_df["Taille d'effet"].mean():.4f} (attendu pour une bonne taille de dataset : 0.5)")
    return moyenne

print(size("SmartFinal/heart_10000.csv"))