
FROM python:3.6


WORKDIR /StreamingEventCompliance
ADD . /StreamingEventCompliance
RUN pip install -r requirements.txt

EXPOSE 5000


