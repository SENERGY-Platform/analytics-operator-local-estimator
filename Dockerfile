FROM python:3.9-slim

ADD . /opt/app
WORKDIR /opt/app
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python", "./main.py" ]