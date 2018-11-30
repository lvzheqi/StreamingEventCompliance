from threading import Thread
import requests
import sys
import json
from . import client_logging


class EventThread(Thread):
    def __init__(self, event, client_uuid):
        self.event = event
        self.client_uuid = client_uuid
        Thread.__init__(self)

    def run(self):
        func_name = sys._getframe().f_code.co_name
        try:
            client_logging.client_logging(message_type="INFO", level="DEBUG", func_name=func_name, username=self.client_uuid,
                                          thread_id="1",
                                          case_id=self.event['case_id'],
                                          activity=self.event['activity'],
                                          message="Posting event to server:http://127.0.0.1:5000/compliance-checker")
            r = requests.post('http://127.0.0.1:5000/compliance-checker?uuid=' + self.client_uuid,
                              json=json.dumps(self.event))
            if r.status_code != 200:
                client_logging.client_logging(message_type="ERROR", level="DEBUG", func_name=func_name,
                                              username=self.client_uuid,
                                              thread_id="1",
                                              case_id=self.event['case_id'],
                                              activity=self.event['activity'],
                                              message="Error by compliance checking")
                print('Error: error by compliance checking')
            else:
                client_logging.client_logging(message_type="INFO", level="DEBUG", func_name=func_name,
                                              username=self.client_uuid,
                                              thread_id="1",
                                              case_id=self.event['case_id'],
                                              activity=self.event['activity'],
                                              message="The server response is: "+r.text)
                print("Info:", r.text)
        except Exception:
            client_logging.client_logging(message_type="ERROR", level="DEBUG", func_name=func_name,
                                          username=self.client_uuid,
                                          thread_id="1",
                                          case_id=self.event['case_id'],
                                          activity=self.event['activity'],
                                          message="The server got disconnected, please try again later ")
            print('The server got disconnected, please try again later')
