#target class balance algotithm that detects if there is a bad proportion of classes
import pandas as pd

df = pd.read_csv("heart.xls")
num_columns = df.shape[1]#number of columns

#threashold method
#good if there are little classifiers
def threashold_method(threshold=5/6):
    if any(target_counts > threshold):
        print("\nThe dataset appears to be IMBALANCED.")
        return -1
    else:
        print("\nThe dataset appears to be BALANCED.")
        return 1

#deviation method
#good if there are many classifiers
def deviation_method(deviation=5):    
    mean = target_counts.mean()
    # Check if any class proportion is more than 2 standard deviations away from the mean
    if (any(target_counts/deviation > mean) or any(target_counts*deviation < mean)):
        print("\nThe dataset appears to be IMBALANCED.")
        return -1
    else:
        print("\nThe dataset appears to be BALANCED.")
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
        print(f"\nThe dataset is BALANCED with a score of {score}.")   
    else:
        print(f"\nThe dataset is IMBALANCED with a score of {score}.")
score = 0 #balancing score
for i in range(num_columns):
    # choose column
    target_col = df.columns[i]
    target_counts = df[target_col].value_counts(normalize=True)

    #Display class distribution
    print(f"\nClass distribution in '{target_col}':")
    print(target_counts)
    score += adjusted_method(score)
score_calculation(score)