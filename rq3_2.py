import json
import pandas as pd
import copy
import csv
import numpy as np
from statistics import mode
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from scipy.stats import sem

def read_Json_file(filepath):
    f = open(filepath, 'r')
    file = json.load(f)
    return file

# Using ComVE data, calculate the annotation accuracy per person using the mode metric as the ground-truth

def calculate_performance(AnnDf, threshold, flag):
    AnnAcc = []
    for columnName in AnnDf:
        annNNanQueryIdx = annotationsDF_copy[annotationsDF_copy[columnName].notna()].index.tolist()
        ann = annotationsDF_copy.loc[annNNanQueryIdx, :].drop(columns=columnName)
        PerformanceCnt = []
        for idx, row in ann.iterrows():
            testAnn = annotationsDF_copy.loc[idx, columnName]
            otherAnn = row.dropna().to_list()
            if otherAnn.count(0) == otherAnn.count(1):  # Skip the statements that receive an equal number of positive (1) and negative (0) annotation labels
                continue  
            annMode = mode(otherAnn) # Get mode as ground-truth

            if annMode == testAnn:
                PerformanceCnt.append(1)
            else:
                PerformanceCnt.append(0)
        if len(PerformanceCnt) > 0:  
            tmp = [columnName, ann.shape[0], len(PerformanceCnt), sum(PerformanceCnt) / len(PerformanceCnt)]
            AnnAcc.append(tmp)

    # Continuously write the accurcay results into a csv file

    with open(f'ComVE_Ann_Acc_{flag}_limit.csv', 'a+') as f:
        csv_writer = csv.writer(f)
        f.write(f"The annotation limit threshold is set as {threshold}. \n")
        csv_writer.writerow(['Annotator ID', '# Annotations', '# Annotations in Acc Cal', 'Acc'])
        csv_writer.writerows(AnnAcc)

    Performance = [line[3] for line in AnnAcc]
    return Performance


# Loads annotations for the json file of ComVE dataset

annotations = read_Json_file("data/raw/ComVE-annotation.json")
annotators = list(set(list(np.concatenate([[ann['workerId'] for ann in annotations[k]['annotations']] for k in annotations.keys()]).flat)))

# Read the annotation files as a Dataframe

annotationsDF_ = pd.DataFrame(index=list(annotations.keys()),
                             columns=list(annotators))
for k in annotations.keys():
    for ann in annotations[k]["annotations"]:
        annotationsDF_.loc[k, ann['workerId']] = ann["annotation"]
annotationsDF_copy = copy.deepcopy(annotationsDF_)


Acc = []
annotationsDF = copy.deepcopy(annotationsDF_)

# Controling the minimum allowable label for each Turker

for aF in range(0, 251, 10):
    cnt = 0
    for index in annotationsDF.columns:
        if index in annotators:
            if len(annotations) - annotationsDF.loc[list(annotations.keys()), index].isna().sum() <= aF:
                cnt += 1
                annotationsDF.loc[list(annotations.keys()), index] = np.nan
    annDF = annotationsDF.dropna(axis=1, how='all').columns.to_list()
    perf = calculate_performance(annDF, aF, 'min')
    Acc.append(perf)

# Draw the boxplot of Annotator's accuracy when controlling the minimum allowable label for each Turker

x = range(0, 251, 10)
fig, ax = plt.subplots(figsize =(20, 8))
bp = ax.boxplot(Acc)
ax.set_xlabel('Minimum allowable labels per Turker', fontsize=16)
ax.set_ylabel('Accuracy', fontsize=16)
ax.set_ylim(0.2, 1.1)
ax.set_yticklabels([round(x, 2) for x in np.arange(0.2, 1.1, 0.2)], fontsize=14)

ax.set_xticks(range(1, 27, 1), x)
ax.set_xticklabels(x, fontsize=14)
# plt.xticks(range(1, 27, 1), x, fontsize=14)
plt.savefig("ComVE_acc_boxplot_when_set_min_limit.png")

Acc = []
annotationsDF = copy.deepcopy(annotationsDF_)

# Controling the maximum allowable label for each Turker

for aF in reversed(range(0, 251, 10)):
    cnt = 0

    for index in annotationsDF.columns:
        if index in annotators:
            if len(annotations) - annotationsDF.loc[list(annotations.keys()), index].isna().sum() >= aF:
                cnt += 1
                annotationsDF.loc[list(annotations.keys()), index] = np.nan
    annDF = annotationsDF.dropna(axis=1, how='all').columns.to_list()
    perf = calculate_performance(annDF, aF, "max")
    Acc.append(perf)

# Draw the boxplot of Annotator's accuracy when controlling the maximum allowable label for each Turker

fig, ax = plt.subplots(figsize =(20, 8))
bp = ax.boxplot(Acc)
ax.set_xlabel('Maximum allowable labels per Turker', fontsize=16)
ax.set_ylabel('Accuracy', fontsize=16)
ax.set_ylim(0.2, 1.1)
ax.set_yticklabels([round(x, 2) for x in np.arange(0.2, 1.1, 0.2)], fontsize=14)

ax.set_xticks(range(1, 27, 1), reversed(x))
ax.set_xticklabels(reversed(x), fontsize=14)
# plt.xticks(range(1, 27, 1), x, fontsize=14)
plt.savefig("ComVE_acc_boxplot_when_set_max_limit.png")

