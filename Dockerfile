FROM python:3.11-slim

RUN mkdir /mcs-noise-audit
COPY ./requirements.txt /mcs-noise-audit
COPY ./generate-jsonl.py /mcs-noise-audit
COPY ./data /mcs-noise-audit/data
WORKDIR /mcs-noise-audit
RUN pip install --upgrade pip
RUN pip install wheel
RUN pip install -r requirements.txt