from knn import knn
from random_forest import random_forest
from logistic_regression import logistic_regression


def evaluation (donnees):

    knn_result = knn(donnees)
    lr_result = logistic_regression(donnees)
    rf_result = random_forest(donnees)
    
    cpt = 0

    if knn_result>0.75:
        cpt += 1
    if lr_result>0.70:
        cpt += 1
    if rf_result>0.80:
        cpt += 1

    if cpt == 3:
        return 1.0
    else:
        return 0.0
    

print(evaluation("SmartFinal/weatherHistory.csv"))