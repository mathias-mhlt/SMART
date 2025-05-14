from model_evaluation import evaluation
from VarianceInflationFactor import vif_score

def column_completeness(path):

    score = (vif_score(path) + evaluation(path)) / 2

    return score

print(column_completeness("SmartFinal/weatherHistory.csv"))