FROM python:3.11-slim

RUN mkdir /mcs-noise-audit
COPY ./requirements.txt /mcs-noise-audit
COPY ./*.py /mcs-noise-audit
COPY ./data /mcs-noise-audit/data
WORKDIR /mcs-noise-audit
RUN pip install --upgrade pip
RUN pip install wheel
RUN pip install -r requirements.txt

RUN python generate-annotations-jsonl.py
RUN python generate-groundtruth-jsonl.py