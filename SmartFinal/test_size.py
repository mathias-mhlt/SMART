from size import size
import pandas as pd
import numpy as np
import csv
import random
import tempfile, os, matplotlib.pyplot as plt
from random_forest import random_forest
from knn import knn

def random_rows(df, N, seed=None):
    rng = np.random.default_rng(seed)
    random_row = rng.integers(0, len(df)-1)
    ref = df.iloc[random_row].tolist()
    #print(f"random_row : {random_row}, ref : {ref}")

    rows_removed = 0
    attempts = 0
    max_attempts = N * 10
    
    while rows_removed < N and attempts < max_attempts and len(df) > 1:
        attempts += 1
        random_row = rng.integers(0, len(df)-1)
        current_row = df.iloc[random_row].tolist()
        
        has_match = False
        for i in range(3):
            if current_row[i] == ref[i]:
                has_match = True
                break
                
        if has_match:
            df = df.drop(df.index[random_row])
            rows_removed += 1
    
    return df



def test_size (donnees, N=100, seed=42):
    rng   = np.random.default_rng(seed)
    base  = pd.read_csv(donnees)

    precisions, scores, lignes = [], [], []
    
    for i in range (N):
        df = base.copy()
        df = random_rows(df, i, seed=int(rng.integers(1e9)))

        tmp_path = tempfile.mktemp(suffix=".csv")
        df.to_csv(tmp_path, index=False)

        scores.append(size(tmp_path))
        lignes.append(len(df))
        #precisions.append(random_forest(tmp_path))
        precisions.append(knn(tmp_path))

        os.remove(tmp_path)
    #print(f"nb ligne : {len(df)}, score : {precisions}, precision : {scores}")


    plt.figure(figsize=(6, 4))
    plt.scatter(lignes, scores, alpha=0.7)
    plt.xlabel("nombre de lignes dans le dataset")
    plt.ylabel("score de taille")
    plt.title(f"Evolution du score de size en fonction du nombre de lignes")
    plt.grid(True)
    
    plt.figure(figsize=(6, 4))
    plt.scatter(scores, precisions, alpha=0.7)
    plt.xlabel("score de taille")
    plt.ylabel("Précision knn")
    plt.title(f"Impact de la taille sur la précision (N={N})")
    plt.grid(True)

    plt.figure(figsize=(6, 4))
    plt.scatter(lignes, precisions, alpha=0.7)
    plt.xlabel("nombre de lignes dans le dataset")
    plt.ylabel("Précision knn")
    plt.title(f"Impact de la taille du dataset sur la précision (N={N})")
    plt.grid(True)
    plt.show()
    return

test_size("./heart.csv", 500, 43) 


    

