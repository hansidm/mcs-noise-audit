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

with jsonlines.open(file) as reader:
    for obj in reader:
        labels_prompt = []
        for label in obj["labels"]:
            labels_prompt.append(label["label"])
        labels_matrix.append(labels_prompt)

prompt_means = np.nanmean(labels_matrix, axis=1)
prompt_stdevs = np.nanstd(labels_matrix, axis=1, ddof=1)
annotator_means = np.nanmean(labels_matrix, axis=0)

print(annotator_means)

level_noise = np.nanstd(annotator_means, ddof=1)
pattern_noise_orig = np.nanstd(prompt_means, ddof=1)
pattern_noise_mod = np.nanstd(prompt_stdevs, ddof=1)
system_noise_orig = math.sqrt((level_noise ** 2) + (pattern_noise_orig ** 2))
system_noise_mod = math.sqrt((level_noise ** 2) + (pattern_noise_mod ** 2))

results = []
results.append(["Level noise", level_noise])
results.append(["Pattern noise (original)", pattern_noise_orig])
results.append(["Pattern noise (modified)", pattern_noise_mod])
results.append(["System noise (original)", system_noise_orig])
results.append(["System noise (modified)", system_noise_mod])

for result in results:
    name, value = result
    print ("{:>25}  {:<15}".format(name, value))
