FROM python:3.7-slim

ADD . /opt/app
WORKDIR /opt/app
RUN apt-get update && \
    apt-get install -y \
        build-essential \
        make \
        gcc \
    && pip install numpy \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get remove -y --purge make gcc build-essential \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*
CMD [ "python", "./main.py" ]