from .client_logging import ClientLogging
from .exception import ServerRequestException, ThreadException
from threading import Thread
import requests
import sys
import json
import queue


class ThreadMemorizer(object):
    '''
    This object is for storing the threads detail that client creates for each case;
    '''
    def __init__(self):
        self.dictionary_threads = {}


class EventThread(Thread):
    def __init__(self, event, index, threadmemorizer, client_uuid):
        Thread.__init__(self)
        self.event = event
        self.client_uuid = client_uuid
        self.index = index
        self.threadmemorizer = threadmemorizer
        self._status_queue = queue.Queue()

    def wait_for_exc_info(self):
        return self._status_queue.get()

    def join_with_exception(self):
        ex_info = self.wait_for_exc_info()
        if ex_info is None:
            return
        else:
            raise ThreadException(ex_info[1])

    def run(self):
        func_name = sys._getframe().f_code.co_name
        try:
            ClientLogging().log_info(func_name, self.client_uuid, self.index, self.event['case_id'],
                                     self.event['activity'],
                                     'Posting event to server:http://127.0.0.1:5000/compliance-checker')
            r = requests.post('http://127.0.0.1:5000/compliance-checker?uuid=' + self.client_uuid,
                              json=json.dumps(self.event))
            self._status_queue.put(None)
            if r.status_code != 200:
                # TODO: jingjinghuo: Problem: What time this belowing code will be executed?
                ClientLogging().log_error(func_name, self.client_uuid, self.index, self.event['case_id'],
                                          self.event['activity'],
                                          'Error by compliance checking')

                ServerRequestException('Failure by compliance checking').get_message()
            else:
                ClientLogging().log_info(func_name, self.client_uuid, self.index, self.event['case_id'],
                                         self.event['activity'],
                                         'The server response is: ' + r.text)
                print('Info:', r.text)

        except Exception:
            ClientLogging().log_error(func_name, self.client_uuid, self.index, self.event['case_id'],
                                      self.event['activity'],
                                      'The server got disconnected, please try again later ')
            self._status_queue.put(sys.exc_info())


