# Machine Common Sense (MCS) Noise Audit

## Requirements

- Python 3
- Requirements in `requirements.txt`

## Instructions

### 1. Data preparation

All required data is already present in the `/data` directory, therefore there is no need to prepare them and you can safely skip this step. However, if you want to re-generate the JSONL files from the raw data, follow these instructions.

To generate annotations:

```
python generate-annotations-jsonl.py
```

To generate modal ground-truth:

```
python generate-groundtruth-jsonl.py
```

### 2. Computing noise

The code in `rq1.py` will compute noise levels using Kahneman's noise framework, as well as our modified version of the noise framework. To compute noise levels for a dataset, use the following:

```
python rq1.py dataset-id
```

### 3. Computing accuracy with 95% confidence intervals

The code in `rq2.py` will compute accuracy scores when considering, at a time, one annotator's labels as predictions against the modal ground-truth constructed with the remaining annotators' labels. In addition, it will compute the 95% confidence interval assuming normal distribution.

```
python rq2.py dataset-id
```

Valid `dataset-id`s for both `rq1.py` and `rq2.py` can be found in the table below

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
