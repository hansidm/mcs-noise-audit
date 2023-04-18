import jsonlines
import numpy as np
import pandas as pd

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
    f = open("data/jsonl/" + tab + ".jsonl", "w")
    writer = jsonlines.Writer(f)
    normalize = False
    if tab.endswith("-mc"):
        normalize = True
    for index, row in df.iterrows():
        prompt = {
            df.columns[0] : context_ids[i_tab] + str(row[df.columns[0]]),
            df.columns[1] : context_ids[i_tab] + str(row[df.columns[1]]),
            df.columns[2] : row[df.columns[2]],
            "labels" : []
        }
        for annotator in header[3:]:
            if not pd.isna(row[annotator]):
                value = int(row[annotator])
                if normalize:
                    if value in [1, 2]:
                        value = 0
                    if value in [3, 4]:
                        value = 1
            else:
                value = np.nan
            label = {
                "annotatorID" : annotator,
                "label" : value
            }
            prompt["labels"].append(label)
        writer.write(prompt)
    writer.close()
    f.close()