from threading import Thread
import requests
import sys
import json
from .client_logging import ClientLogging
from .exception import ConnectionException


class ThreadMemorizer(object):
    '''
    This object is for storing the threads detail that client creates for each case;
    '''
    def __init__(self):
        self.dictionary_threads = {}


class EventThread(Thread):
    def __init__(self, event, index, threadmemorizer, client_uuid):
        self.event = event
        self.client_uuid = client_uuid
        self.index = index
        self.threadmemorizer = threadmemorizer
        Thread.__init__(self)

    def run(self):
        func_name = sys._getframe().f_code.co_name
        try:
            ClientLogging().log_info(func_name, self.client_uuid, self.index, self.event['case_id'], self.event['activity'],
                                          "Posting event to server:http://127.0.0.1:5000/compliance-checker")
            r = requests.post('http://127.0.0.1:5000/compliance-checker?uuid=' + self.client_uuid,
                              json=json.dumps(self.event))
        except requests.exceptions.RequestException:
            ClientLogging().log_error(func_name, self.client_uuid, self.index, self.event['case_id'], self.event['activity'],
                                     "The server got disconnected, please try again later ")
            print(ConnectionException.message)
        # TODO: jingjinghuo: i want to raise this exception, and break it in for-loop, but i cannot do it, why?
        # We need this because when the server break down, after a while the server is ran, if the threads for
        # requests are still running, then the comformance checking for that event log will continue,
        # but we lost some events.

        else: # request is successful
            if r.status_code != 200:
                # TODO: jingjinghuo: Problem: What time this belowing code will be executed?
                ClientLogging().log_error(func_name, self.client_uuid, self.index, self.event['case_id'], self.event['activity'],
                                              "Error by compliance checking")
                print('Error: error by compliance checking')
            else:
                ClientLogging().log_info(func_name, self.client_uuid, self.index, self.event['case_id'], self.event['activity'],
                                              "The server response is: "+r.text)
                print("Info:", r.text)

        # TODO: jingjinghuo: there is a problem here. if a client have already done the 1.compliance checking,
        #  and click 1 again, will do it again.

