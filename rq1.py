import jsonlines
import math
import numpy as np
import sys

labels_matrix = []
prompt_means = []
prompt_stdevs = []
annotator_means = []

if sys.argv[1] is not None:
    file = sys.argv[1]
else:
    print("File missing.")
    exit

file = "data/jsonl/" + file + ".jsonl"

# Loads annotations for the parameterized dataset
# Reads JSONL and builds the labels_matrix
# Each column is an annotator, each row is a prompt
with jsonlines.open(file) as reader:
    for obj in reader:
        labels_prompt = []
        for label in obj["labels"]:
            labels_prompt.append(label["label"])
        labels_matrix.append(labels_prompt)

# Calculates prompt means and stdevs, and annotator means
# ddof=1 for stdevs indicates Sample Standard Deviation instead of Population
# Calculated means and stdev ignore missing values (nanmean/nanstd)
# OBS: nanmean for the vacationing-abroad-tf dataset will trigger a warning...
# ...due to prompts without annotation (this is intentional and documented in the article)
prompt_means = np.nanmean(labels_matrix, axis=1)
prompt_stdevs = np.nanstd(labels_matrix, axis=1, ddof=1)
annotator_means = np.nanmean(labels_matrix, axis=0)

# Calculates equations (1), (2), (3), and (4) from the article
# ddof=1 for stdevs indicate Sample Standard Deviation instead of Population
level_noise = np.nanstd(annotator_means, ddof=1)
pattern_noise_orig = np.nanstd(prompt_means, ddof=1)
pattern_noise_mod = np.nanstd(prompt_stdevs, ddof=1)
system_noise_orig = math.sqrt((level_noise ** 2) + (pattern_noise_orig ** 2))
system_noise_mod = math.sqrt((level_noise ** 2) + (pattern_noise_mod ** 2))

# Prepares output
results = [
    ["Level noise", level_noise],
    ["Pattern noise (original)", pattern_noise_orig],
    ["Pattern noise (modified)", pattern_noise_mod],
    ["System noise (original)", system_noise_orig],
    ["System noise (modified)", system_noise_mod]
]

# Prints output
for result in results:
    name, value = result
    print ("{:>25}  {:<15}".format(name, value))
