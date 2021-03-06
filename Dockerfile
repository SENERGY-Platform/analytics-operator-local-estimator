FROM python:3.7

ADD . /opt/app
WORKDIR /opt/app
RUN apt-get update -y && apt-get install -y libatlas-base-dev python-dev
RUN pip install -U numpy --extra-index-url https://www.piwheels.org/simple
RUN pip install --no-cache-dir -r requirements.txt --extra-index-url https://www.piwheels.org/simple
CMD [ "python", "./main.py" ]