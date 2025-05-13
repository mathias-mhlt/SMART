import os
import numpy as np 
import pandas as pd 
import warnings
import seaborn as sns
import matplotlib.pyplot as plt
"import plotly.express as px"
warnings.filterwarnings("ignore")
pd.set_option("display.max_rows",None)
from sklearn import preprocessing
import matplotlib 
matplotlib.style.use('ggplot')
from sklearn.preprocessing import LabelEncoder


def calcul_prop (df, col) :
    prop = df[col].value_counts(normalize=True)
    prop = prop.reset_index()
    prop.columns = [col, "proportion"]
    prop["rapport"] = 0.0
    return prop

def rarity(donnees):

    df=pd.read_csv(donnees)
    df.head()
    string_col = df.select_dtypes(include="object").columns
    df[string_col]=df[string_col].astype("string")
    df.dtypes

    df_tree = df.apply(LabelEncoder().fit_transform)
    df_tree.head()
    df_tree = df.apply(LabelEncoder().fit_transform)
    df_tree.head()

    cpt = 0

    for col in df_tree.columns:
        proportion = calcul_prop(df_tree, col)
        for i in range(len(proportion)):
            autres_proportions = proportion["proportion"].drop(i)
            if len(autres_proportions) > 0:
                moyenne = autres_proportions.mean()
                ecart_type_corrige = autres_proportions.std(ddof=1)
                z = (proportion.at[i, "proportion"] - moyenne) / ecart_type_corrige
                proportion.at[i, "rapport"] = z
                if z < -2:
                    cpt += 1
    pourcentage = cpt / len(df_tree)
    print(f"Proportion de valeurs aberrantes: {pourcentage*100:.2f}%")
    return (1 - pourcentage)

print(rarity("./SmartFinal/heart_10000_with_adversary_move.csv"))