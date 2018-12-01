from threading import Thread
import requests
import sys
import json
from . import client_logging
from .exception import ConnectionException


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
        except requests.exceptions.RequestException:
            client_logging.client_logging(message_type
                                      ="ERROR", level="DEBUG", func_name=func_name,
                                      username=self.client_uuid,
                                      thread_id="1",
                                      case_id=self.event['case_id'],
                                      activity=self.event['activity'],
                                      message="The server got disconnected, please try again later ")
            print(ConnectionException.message)
        # TODO: jingjinghuo: i want to raise this exception, and break it in for-loop, but i cannot do it, why?
        # We need this because when the server break down, after a while the server is ran, if the threads for
        # requests are still running, then the comformance checking for that event log will continue,
        # but we lost some events.

        else: # request is successful
            if r.status_code != 200:
                # TODO: jingjinghuo: Problem: What time this belowing code will be executed?
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
                                              message="The server response is: " + r.text)
                print("Info:", r.text)

        # TODO: jingjinghuo: there is a problem here. if a client have already done the 1.compliance checking,
        #  and click 1 again, will do it again.

