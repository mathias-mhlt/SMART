import pandas as pd 
from sklearn import model_selection
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import classification_report,roc_auc_score


def knn(donnees) :
    df=pd.read_csv(donnees)

    string_col = df.select_dtypes(include="object").columns
    df[string_col]=df[string_col].astype("string")
    df_nontree=pd.get_dummies(df,columns=string_col,drop_first=False)

    target=df.columns[-1]
    y=df_nontree[target].values
    df_nontree.drop(target,axis=1,inplace=True)
    df_nontree=pd.concat([df_nontree,df[target]],axis=1)

    feature_col_nontree=df_nontree.columns.to_list()
    feature_col_nontree.remove(target)
    acc_KNN=[]
    kf=model_selection.StratifiedKFold(n_splits=5)
    average_acc=0
    for fold , (trn_,val_) in enumerate(kf.split(X=df_nontree,y=y)):
        
        X_train=df_nontree.loc[trn_,feature_col_nontree]
        y_train=df_nontree.loc[trn_,target]
        
        X_valid=df_nontree.loc[val_,feature_col_nontree]
        y_valid=df_nontree.loc[val_,target]
        
        ro_scaler=MinMaxScaler()
        X_train=ro_scaler.fit_transform(X_train)
        X_valid=ro_scaler.transform(X_valid)
        
        clf=KNeighborsClassifier(n_neighbors=50)
        clf.fit(X_train,y_train)
        y_pred=clf.predict(X_valid)
        #print(f"The fold is : {fold} : ")
        #print(classification_report(y_valid,y_pred))
        acc=roc_auc_score(y_valid,y_pred)
        acc_KNN.append(acc)
        average_acc+=acc
        #print(f"The accuracy for {fold+1} : {acc}")
        
        pass

    average_acc=average_acc/5
    print(f"The average accuracy of knn is : {average_acc}")

    if average_acc>0.8:
        return 1
    else:
        return 0
    



















import pandas as pd
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report,roc_auc_score
from sklearn.preprocessing import MinMaxScaler
import numpy as np

def logistic_regression(donnees):
    df=pd.read_csv(donnees)

    string_col = df.select_dtypes(include="object").columns
    df[string_col]=df[string_col].astype("string")
    df_nontree=pd.get_dummies(df,columns=string_col,drop_first=False)

    target=df.columns[-1]
    y=df_nontree[target].values
    df_nontree.drop(target,axis=1,inplace=True)
    df_nontree=pd.concat([df_nontree,df[target]],axis=1)

    feature_col_nontree=df_nontree.columns.to_list()
    feature_col_nontree.remove(target)

    acc_log=[]

    kf=model_selection.StratifiedKFold(n_splits=5)
    for fold , (trn_,val_) in enumerate(kf.split(X=df_nontree,y=y)):
        
        X_train=df_nontree.loc[trn_,feature_col_nontree]
        y_train=df_nontree.loc[trn_,target]
        
        X_valid=df_nontree.loc[val_,feature_col_nontree]
        y_valid=df_nontree.loc[val_,target]
        
        ro_scaler=MinMaxScaler()
        X_train=ro_scaler.fit_transform(X_train)
        X_valid=ro_scaler.transform(X_valid)
        
        
        clf=LogisticRegression()
        clf.fit(X_train,y_train)
        y_pred=clf.predict(X_valid)
        # print(f"The fold is : {fold} : ")
        # print(classification_report(y_valid,y_pred))
        acc=roc_auc_score(y_valid,y_pred)
        acc_log.append(acc)
        #print(f"The accuracy for Fold {fold+1} : {acc}")
        pass

    average_acc=np.mean(acc_log)
    print(f"The average accuracy of logistic regression is : {average_acc}")

    if average_acc>0.75:
        return 1
    else:
        return 0
    












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
    





