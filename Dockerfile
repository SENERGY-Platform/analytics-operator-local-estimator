FROM python:3.7

ADD . /opt/app
WORKDIR /opt/app
RUN pip install -U numpy
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python", "./main.py" ]