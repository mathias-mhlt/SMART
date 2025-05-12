import pandas as pd

df = pd.read_csv("heart.xls")
num_columns = df.shape[1]
def threashold_method(threshold=0.6):
    if any(target_counts > threshold):
        return -1
    else:
        return 1

def deviation_method(deviation=2):
    mean = target_counts.mean()
    # Check if any class proportion is more than 2 standard deviations away from the mean
    if (any(target_counts/deviation > mean) or any(target_counts*deviation < mean)):
        return -1
    else:
        return 1

# Adjusted method to keep precision of little and many classifiers
def adjusted_method(score=0):
    # takes threashold and deviation methods for a more accurate result depending on their size
    if len(target_counts) <= 5:
        return threashold_method(5/6)
    else:
        return deviation_method(5)

#calculate balancing score
def score_calculation(score):
    #score = num_columns
    if score >= 0:
        return score
    else:
        return score
score = 0 #balancing score
for i in range(num_columns):
    # choose column
    target_col = df.columns[i]
    target_counts = df[target_col].value_counts(normalize=True)

    #Display class distribution
    score += adjusted_method(score)
score_calculation(score)