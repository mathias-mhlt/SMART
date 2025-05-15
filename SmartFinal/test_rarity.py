import numpy as np, pandas as pd
import tempfile, os, matplotlib.pyplot as plt
from knn import knn
from Rarity import rarity



def random_data(df, N, seed=None):
    nb_cols = len(df.columns) - 1
    rng = np.random.default_rng(seed)

    for i in range(N*100):
        random_row = rng.integers(0, len(df)-1)
        random_col = rng.integers(0, nb_cols-1)
        random_length = rng.integers(1, 11)
        random_chars = [chr(rng.integers(32, 127)) for _ in range(random_length)]
        random_value = ''.join(random_chars)

        df.iloc[random_row, random_col] = random_value


    return df


def test_rarity(donnees, N=100, seed=42):
    rng   = np.random.default_rng(seed)
    base  = pd.read_csv(donnees)

    precisions, scores, lignes = [], [], []

    for i in range (N):
        df = base.copy()
        df = random_data(df, i, seed=int(rng.integers(1e9)))

        tmp_path = tempfile.mktemp(suffix=".csv")
        df.to_csv(tmp_path, index=False)

        scores.append(rarity(tmp_path))
        #precisions.append(random_forest(tmp_path))
        precisions.append(knn(tmp_path))

        os.remove(tmp_path)
    #print(f"nb ligne : {len(df)}, score : {precisions}, precision : {scores}")

    plt.figure(figsize=(6, 4))
    plt.scatter(scores, precisions, alpha=0.7)
    plt.xlabel("Score de cohérence de rareté")
    plt.ylabel("Précision KNN")
    plt.title(f"Impact de la rareté sur la précision (N={N})")
    plt.grid(True)
    plt.show()


    return

test_rarity("./heart.csv", N=100, seed=42)