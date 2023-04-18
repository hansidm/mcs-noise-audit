# sample size , non missing values only
# Annotator X: accuracy
# 95% CI standard deviation (lower-bound - upper-bound)

import jsonlines
import scipy.stats
import sys
from math import sqrt
from sklearn.metrics import accuracy_score

pred_matrix = [[],[],[],[],[],[]]
true_matrix = [[],[],[],[],[],[]]

if sys.argv[1] is not None:
    file = sys.argv[1]
else:
    print("File missing.")
    exit

pred_file = "data/jsonl/" + file + ".jsonl"
true_file = "data/jsonl/" + file + "-gt.jsonl"

# Loads annotations for the parametrized dataset
# Reads JSONL and builds the prediction matrix (pred_matrix)
# Each column is a prompt, each row is an annotator
with jsonlines.open(pred_file) as reader:
    for obj in reader:
        i = 0
        for label in obj["labels"]:
            pred_matrix[i].append(label["label"])
            i = i + 1

# Loads ground-truth for the parametrized dataset
# Reads JSONL and builds the modal ground-truth matrix (true_matrix)
# Each column is a prompt, each row is an annotator
with jsonlines.open(true_file) as reader:
    for obj in reader:
        i = 0
        for label in obj["gt"]:
            true_matrix[i].append(label["label"])
            i = i + 1

# Removes all missing values from the prediction matrix and...
# ...respective values in the ground-truth matrix (cleaned_pred, cleaned_true)
cleaned_true = [[],[],[],[],[],[]]
cleaned_pred = [[],[],[],[],[],[]]
for annotator in range(6):
    for i, x in enumerate(pred_matrix[annotator]):
        if str(x) != 'nan':
            cleaned_pred[annotator].append(x)
            cleaned_true[annotator].append(true_matrix[annotator][i])

# Obtains z_value for 95% CI
confidence = 0.95
z_value = scipy.stats.norm.ppf((1 + confidence) / 2.0)

# One annotator at a time, calculates accuracy of the prediction against the modal ground truth,...
# ...calculates the confidence interval assuming Gaussian distribution,
# ...and prints the output
for annotator in range(6):
    accuracy = accuracy_score(cleaned_true[annotator], cleaned_pred[annotator])
    size = len(cleaned_pred[annotator])
    interval = z_value * sqrt((accuracy * (1 - accuracy)) / size)
    print("Annotator", annotator, ":", accuracy)
    print("Sample size:", size)
    print("95% CI:", interval)
    print("Lower - Uppder:", accuracy-interval, "-", accuracy+interval)
    print("----------------------------")
