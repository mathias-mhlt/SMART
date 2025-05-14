import pandas as pd 
from sklearn import model_selection
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import classification_report,roc_auc_score
from sklearn.preprocessing import LabelEncoder


def knn(donnees) :
    df=pd.read_csv(donnees)

    # string_col = df.select_dtypes(include="object").columns
    # df[string_col]=df[string_col].astype("string")
    df_nontree = df.apply(LabelEncoder().fit_transform)
    #print(df_nontree.head())

    target=df.columns[-1]

    y=df_nontree[target].values

    feature_col_nontree = [col for col in df_nontree.columns if col != target]

    acc_KNN=[]
    kf=model_selection.StratifiedKFold(n_splits=5)
    average_acc=0
    for fold, (trn_, val_) in enumerate(kf.split(X=df_nontree, y=y)):
        
        X_train = df_nontree.loc[trn_, feature_col_nontree]
        y_train = df_nontree.loc[trn_, target]
        
        X_valid = df_nontree.loc[val_, feature_col_nontree]
        y_valid = df_nontree.loc[val_, target]
        
        ro_scaler = MinMaxScaler()
        X_train = ro_scaler.fit_transform(X_train)
        X_valid = ro_scaler.transform(X_valid)
        
        clf = KNeighborsClassifier(n_neighbors=50)
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_valid)
        
        n_classes = len(set(y_train))
        
        if n_classes == 2:
            acc = roc_auc_score(y_valid, y_pred)
        else:
            y_pred_proba = clf.predict_proba(X_valid)
            acc = roc_auc_score(y_valid, y_pred_proba, multi_class='ovr')
        
        acc_KNN.append(acc)
        average_acc += acc
        #print(f"The accuracy for {fold+1} : {acc}")

    average_acc=average_acc/5
    print(f"The average accuracy of knn is : {average_acc}")

    return average_acc

#knn("SmartFinal/heart_10000.csv")