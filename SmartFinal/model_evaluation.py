from knn import knn
from random_forest import random_forest
from logistic_regression import logistic_regression


def evaluation (donnees):

    knn_result = knn(donnees)
    rf_result = random_forest(donnees)
    lr_result = logistic_regression(donnees)

    if (knn_result + rf_result + lr_result) == 3:
        return 1.0
    else:
        return 0.0
    

print(evaluation("SmartFinal/weatherHistory.csv"))