
FROM python:3.6

RUN apt-get update
RUN apt-get -y install python3-pydot python-pydot python-pydot-ng graphviz

ADD . /StreamingEventCompliance
WORKDIR /StreamingEventCompliance

RUN pip install -r requirements.txt

EXPOSE 5000
CMD python -u server.py

