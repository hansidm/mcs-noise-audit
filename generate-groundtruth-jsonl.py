import jsonlines
import numpy as np
import pandas as pd
from statistics import mode

context_ids = [
    "VC",
    "VC",
    "CV",
    "CV",
    "BW",
    "BW",
    "DC",
    "DC"
]
tabs = [
    "vacationing-abroad-mc",
    "vacationing-abroad-tf",
    "camping-mc",
    "camping-tf",
    "bad-weather-mc",
    "bad-weather-tf",
    "dental-cleaning-mc",
    "dental-cleaning-tf"
]
header = [
    "answerID",
    "questionID",
    "category",
    "A", "B", "C", "D", "E", "F"
]

for i_tab, tab in enumerate(tabs):
    df = pd.read_excel("data/raw/tg-csr-annotation.xlsx", tab, names=header)
    f = open("data/jsonl/" + tab + "-gt.jsonl", "w")
    writer = jsonlines.Writer(f)
    normalize = False
    if tab.endswith("-mc"):
        normalize = True
    for index, row in df.iterrows():
        groundtruth = {
            df.columns[0] : context_ids[i_tab] + str(row[df.columns[0]]),
            df.columns[1] : context_ids[i_tab] + str(row[df.columns[1]]),
            df.columns[2] : row[df.columns[2]],
            "gt" : []
        }
        for annotator in header[3:]:
            to_remove = header[:3]
            to_remove.append(annotator)
            remaining = row.drop(labels=to_remove).to_list()
            remaining = [ int(i) for i in remaining if not pd.isna(i)]
            if normalize:
                for i, label in enumerate(remaining):
                    if label in [1, 2]:
                        remaining[i] = 0
                    elif label in [3, 4]:
                        remaining[i] = 1
            label = None
            if len(remaining) > 0:
                label = mode(remaining)
            else:
                label = np.nan
            gt = {
                "annotatorID" : annotator,
                "label" : label
            }
            groundtruth["gt"].append(gt)
        writer.write(groundtruth)
    writer.close()
    f.close()