
FROM python:3.6


WORKDIR /StreamingEventCompliance
ADD . /StreamingEventCompliance
#COPY requirements.txt /StreamingEventCompliance
RUN pip install -r requirements.txt

EXPOSE 5000

#COPY server.py /StreamingEventCompliance
CMD python server.py

