# Machine Common Sense (MCS) Noise Audit

## Requirements

- Python 3
- Requirements in `requirements.txt`

## Instructions

### 1. Data preparation (Optional step)

All required data is already present in the `/data` directory, therefore there is no need to prepare them and you can safely skip this step. However, if you want to re-generate the JSONL files for the TG-CSR benchmark from the raw data, follow these instructions.

To generate annotations:

```
python generate-annotations-jsonl.py
```

To generate modal ground-truth:

```
python generate-groundtruth-jsonl.py
```

The manual plausibility annotation file of ComVE dataset is also included in the `/data/raw` directory, named ComVE-annotation.json, and does not require further preprocessing.

### 2. Computing noise in TG-CSR annotations

The code in `rq1_tgcsr.py` will compute noise levels in TG-CSR annotations using Kahneman's noise framework, as well as our modified version of the noise framework. To compute noise levels for a dataset in TG-CSR, use the following:

```
python rq1_tgcsr.py dataset-id
```

### 3. Computing accuracy with 95% confidence intervals in TG-CSR annotations

The code in `rq2_tgcsr.py` will compute accuracy scores in TG-CSR annotations, when considering, at a time, one annotator's labels as predictions against the modal ground-truth constructed with the remaining annotators' labels. In addition, it will compute the 95% confidence interval assuming normal distribution.

```
python rq2_tgcsr.py dataset-id
```

Valid `dataset-id`s for both `rq1_tgcsr.py` and `rq2_tgcsr.py` can be found in the table below:

| Dataset ID              | Description                     |
| ----------------------- | ------------------------------- |
| `vacationing-abroad-mc` | Vacationing Abroad Multi-Choice |
| `vacationing-abroad-tf` | Vacationing Abroad True/False   |
| `camping-mc`            | Camping Vacation Multi-Choice   |
| `camping-tf`            | Camping Vacation True/False     |
| `bad-weather-mc`        | Bad Weather Multi-Choice        |
| `bad-weather-tf`        | Bad Weather True/False          |
| `dental-cleaning-mc`    | Dental Cleaning Multi-Choice    |
| `dental-cleaning-tf`    | Dental Cleaning True/False      |


### 4. Computing noise in ComVE annotations

The code in `rq1_comve.py` will follow the same noise framework to calculate the different noise levels in the ComVE annotation file, while setting different min/max allowed label limits for each Turker. Simply run the following command to obtain the corresponding noise levels with different cutoffs:

```
python rq1_comve.py
```

The noise level results are saved in two separate csv files, corresponding to the two different cutoffs.


### 5. Computing accuracy in  ComVE annotations

The code in `rq2_comve.py` will compute the annotation accuracy of Turkers on the ComVE dataset when controlling the minimum/maximum allowable labels for each Turker, with the ground truth computed using the mode metric from the remaining annotators. Please use the following commands to get detailed accuracy results and corresponding visualizations while implementing the two cutoff methods:

```
python rq2_comve.py
```

The accuracy results are stored in two distinct CSV files, while the visualizations are saved in two separate PNG files, each corresponding to one of the two different cutoff methods.

