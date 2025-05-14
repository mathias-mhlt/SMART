import numpy as np 
import pandas as pd 
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report,roc_auc_score
from sklearn.ensemble import RandomForestClassifier
from sklearn import model_selection

def random_forest(donnees):
    df=pd.read_csv(donnees)

    df_tree = df.apply(LabelEncoder().fit_transform)

    target=df_tree.columns[-1]

    y=df_tree[target].values


    feature_col_tree = [col for col in df_tree.columns if col != target]


    acc_RandF=[]
    average_acc=0

    kf=model_selection.StratifiedKFold(n_splits=5)
    for fold , (trn_,val_) in enumerate(kf.split(X=df_tree,y=y)):
        
        X_train=df_tree.loc[trn_,feature_col_tree]
        y_train=df_tree.loc[trn_,target]
        
        X_valid=df_tree.loc[val_,feature_col_tree]
        y_valid=df_tree.loc[val_,target]
        
        clf=RandomForestClassifier(n_estimators=200,criterion="entropy")
        clf.fit(X_train,y_train)
        y_pred=clf.predict(X_valid)
        #print(f"The fold is : {fold} : ")
        #print(classification_report(y_valid,y_pred))

        n_classes = len(set(y_train))
        
        if n_classes == 2:
            acc = roc_auc_score(y_valid, y_pred)
        else:
            y_pred_proba = clf.predict_proba(X_valid)
            acc = roc_auc_score(y_valid, y_pred_proba, multi_class='ovr')


        acc_RandF.append(acc)
        average_acc += acc
        #print(f"The accuracy for {fold+1} : {acc}")

    average_acc=average_acc/5
    print(f"The average accuracy of random forest is : {average_acc}")

    return average_acc
    
#random_forest("./heart.csv")