
def synonyme_from_api(word):
    url = f"https://api.datamuse.com/words?rel_syn={word}"
    response = requests.get(url)
    if response.status_code == 200:
        return [item['word'] for item in response.json()]
    return []


def consistent_representation_score (file) : 
    df = pd.read_csv(file)
    # Récupérer uniquement les colonnes de type texte (objet = chaîne)
    text_columns = df.select_dtypes(include="object").columns
    total_text_columns = len(text_columns)             #nombre de colonnes textuelles
    total_text_entries_columns = df[text_columns].size #nombre de données par colonnes
    print("colonnes retenues (celles qui sont reconnues pour être du texte) : ", text_columns)

    #init compte des valeurs à changer par synonymes dans la BD 
    count_val_to_change=0

    # Boucle sur chaque ligne des colonnes texte
    for col in text_columns:
        #intialisation des set
        set_mot_base = set()
        set_synonymes = set()
        for val in df[col].dropna():  # ici on a enlever les valeurs nulles des colonnes car on ne traite pas ce cas dans ce critère
            if val not in set_mot_base : 
                if val not in set_synonymes : 
                    set_mot_base.add(val)
                    liste_syn = synonyme_from_api(val)
                    for synonyme in liste_syn : 
                        set_synonymes.add(synonyme)
                else:
                    count_val_to_change+=1
        print(set_mot_base)
        print(set_synonymes)
    return 1-1/df.size*(count_val_to_change/df.shape[1])