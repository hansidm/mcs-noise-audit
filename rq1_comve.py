import json
import copy
import pandas as pd
import numpy as np
import math

def read_Json_file(filepath):
    f = open(filepath, 'r')
    file = json.load(f)
    return file


# Loads annotations for the json file of ComVE dataset
# Each item is a statement with five annotations from five annotators

annotations = read_Json_file("data/raw/ComVE-annotation.json")
annotators = list(set(list(np.concatenate([[ann['workerId'] for ann in annotations[k]['annotations']] for k in annotations.keys()]).flat)))
print(len(set(annotators)))

# Read the annotation files as a Dataframe

annotationsDF_ = pd.DataFrame(index=list(annotations.keys()),
                             columns=list(annotators))
for k in annotations.keys():
    for ann in annotations[k]["annotations"]:
        annotationsDF_.loc[k, ann['workerId']] = ann["annotation"]


annotationFrequency = []
LevelNoise = []
PattenNoise = []
PattenNoiseMod = []
SentenceSTD = []
SentenceSTDMod = []
FilteredAnnotators = []

ZeroAnn = []
OneAnn = []
TwoAnn = []
ThreeAnn = []
FourAnn = []
FiveAnn = []

annotationsDF = copy.deepcopy(annotationsDF_)

# Controling the minimum allowable label for each Turker

for aF in range(0, 251, 10):
    cnt = 0
    for index in annotationsDF.columns:
        if index in annotators:
            if len(annotations) - annotationsDF.loc[list(annotations.keys()), index].isna().sum() <= aF:
                cnt += 1
                annotationsDF.loc[list(annotations.keys()), index] = np.nan
    FilteredAnnotators.append(cnt)

    # Calculate noise using equations (1), (2), (3), and (4) from the article

    annotationsDF["Sentence Mean"] = annotationsDF.loc[list(annotations.keys()) , list(annotators)].mean(axis=1)
    annotationsDF["Sentence Standard Deviation"] = annotationsDF.loc[list(annotations.keys()), list(annotators)].std(axis=1)
    annotationsDF.loc["Annotator Mean", list(annotators)] = annotationsDF.loc[list(annotations.keys()), list(annotators)].mean(axis=0)
    ZeroAnn.append(sum(annotationsDF.loc[annotationsDF.index!="Annotator Mean"].loc[list(annotations.keys()), list(annotators)].count(axis=1) == 0))
    OneAnn.append(sum(annotationsDF.loc[annotationsDF.index!="Annotator Mean"].loc[list(annotations.keys()), list(annotators)].count(axis=1) == 1))
    TwoAnn.append(sum(annotationsDF.loc[annotationsDF.index!="Annotator Mean"].loc[list(annotations.keys()), list(annotators)].count(axis=1) == 2))
    ThreeAnn.append(sum(annotationsDF.loc[annotationsDF.index!="Annotator Mean"].loc[list(annotations.keys()), list(annotators)].count(axis=1) == 3))
    FourAnn.append(sum(annotationsDF.loc[annotationsDF.index!="Annotator Mean"].loc[list(annotations.keys()), list(annotators)].count(axis=1) == 4))
    FiveAnn.append(sum(annotationsDF.loc[annotationsDF.index!="Annotator Mean"].loc[list(annotations.keys()), list(annotators)].count(axis=1) == 5))

    LN = annotationsDF.loc['Annotator Mean', list(annotators)].std()
    LevelNoise.append(LN)
    PN = annotationsDF.loc[list(annotations.keys()), 'Sentence Mean'].std()
    PattenNoise.append(PN)
    PNM = annotationsDF.loc[list(annotations.keys()), 'Sentence Standard Deviation'].std()
    PattenNoiseMod.append(PNM)
    SS = math.sqrt(LN*LN + PN*PN)
    SentenceSTD.append(SS)
    SSM = math.sqrt(LN*LN + PNM*PNM)
    SentenceSTDMod.append(SSM)

# Save the noise results in ComVE_noise_min_limit_analysis.csv 

noiseAnalysis = {"Level Noise": LevelNoise, "Pattern Noise": PattenNoise, "Pattern Noise Modified": PattenNoiseMod,
"Sentence STD": SentenceSTD, "Sentence STD modified": SentenceSTDMod,"# Filtered Annotators": FilteredAnnotators, "# Statements with 0 annotator":
ZeroAnn, "# Statements with 1 annotator": OneAnn, "# Statements with 2 annotators": TwoAnn, "# Statements with 3 annotators": ThreeAnn,
"# Statements with 4 annotators": FourAnn, "# Statements with 5 annotators": FiveAnn}
Analysis = pd.DataFrame(noiseAnalysis, index=list(range(0, 251, 10)))
Analysis.to_csv("ComVE_noise_min_limit_analysis.csv")



annotationFrequency = []
LevelNoise = []
PattenNoise = []
PattenNoiseMod = []
SentenceSTD = []
SentenceSTDMod = []
FilteredAnnotators = []

ZeroAnn = []
OneAnn = []
TwoAnn = []
ThreeAnn = []
FourAnn = []
FiveAnn = []

annotationsDF = copy.deepcopy(annotationsDF_)

# Controling the maximum allowable label for each Turker

for aF in reversed(range(0, 251, 10)):
    cnt = 0
    for index in annotationsDF.columns:
        if index in annotators:
            if len(annotations) - annotationsDF.loc[list(annotations.keys()), index].isna().sum() >= aF:
                annotationsDF.loc[list(annotations.keys()), index] = np.nan
            if annotationsDF.loc[list(annotations.keys()), index].isna().sum() == len(annotations):
                cnt += 1

    FilteredAnnotators.append(cnt)
    annotationsDF["Sentence Mean"] = annotationsDF.loc[list(annotations.keys()) , list(annotators)].mean(axis=1)
    annotationsDF["Sentence Standard Deviation"] = annotationsDF.loc[list(annotations.keys()), list(annotators)].std(axis=1)
    annotationsDF.loc["Annotator Mean", list(annotators)] = annotationsDF.loc[list(annotations.keys()), list(annotators)].mean(axis=0)
    
    ZeroAnn.append(sum(annotationsDF.loc[annotationsDF.index!="Annotator Mean"].loc[list(annotations.keys()), list(annotators)].count(axis=1) == 0))
    OneAnn.append(sum(annotationsDF.loc[annotationsDF.index!="Annotator Mean"].loc[list(annotations.keys()), list(annotators)].count(axis=1) == 1))
    TwoAnn.append(sum(annotationsDF.loc[annotationsDF.index!="Annotator Mean"].loc[list(annotations.keys()), list(annotators)].count(axis=1) == 2))
    ThreeAnn.append(sum(annotationsDF.loc[annotationsDF.index!="Annotator Mean"].loc[list(annotations.keys()), list(annotators)].count(axis=1) == 3))
    FourAnn.append(sum(annotationsDF.loc[annotationsDF.index!="Annotator Mean"].loc[list(annotations.keys()), list(annotators)].count(axis=1) == 4))
    FiveAnn.append(sum(annotationsDF.loc[annotationsDF.index!="Annotator Mean"].loc[list(annotations.keys()), list(annotators)].count(axis=1) == 5))

    LN = annotationsDF.loc['Annotator Mean', list(annotators)].std()
    LevelNoise.append(LN)
    PN = annotationsDF.loc[list(annotations.keys()), 'Sentence Mean'].std()
    PattenNoise.append(PN)
    PNM = annotationsDF.loc[list(annotations.keys()), 'Sentence Standard Deviation'].std()
    PattenNoiseMod.append(PNM)
    SS = math.sqrt(LN*LN + PN*PN)
    SentenceSTD.append(SS)
    SSM = math.sqrt(LN*LN + PNM*PNM)
    SentenceSTDMod.append(SSM)

# Save the noise results in ComVE_noise_max_limit_analysis.csv 

noiseAnalysis = {"Level Noise": LevelNoise, "Pattern Noise": PattenNoise, "Pattern Noise Modified": PattenNoiseMod,
"Sentence STD": SentenceSTD, "Sentence STD modified": SentenceSTDMod,"# Filtered Annotators": FilteredAnnotators, "# Statements with 0 annotator":
ZeroAnn, "# Statements with 1 annotator": OneAnn, "# Statements with 2 annotators": TwoAnn, "# Statements with 3 annotators": ThreeAnn,
"# Statements with 4 annotators": FourAnn, "# Statements with 5 annotators": FiveAnn}
Analysis = pd.DataFrame(noiseAnalysis, index=list(reversed(range(0, 251, 10))))
Analysis.to_csv("ComVE_noise_max_limit_analysis.csv")