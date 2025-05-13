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
    df_tree.drop(target,axis=1,inplace=True)
    df_tree=pd.concat([df_tree,df[target]],axis=1)

    feature_col_tree=df_tree.columns.to_list()
    feature_col_tree.remove(target)


    acc_RandF=[]
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
        acc=roc_auc_score(y_valid,y_pred)
        acc_RandF.append(acc)
        #print(f"The accuracy for {fold+1} : {acc}")
    average_acc=np.mean(acc_RandF)
    print(f"The average accuracy of random forest is : {average_acc}")

    if average_acc>0.85:
        return 1
    else:
        return 0
    
#print(random_forest("SmartFinal/heart_10000.csv"))