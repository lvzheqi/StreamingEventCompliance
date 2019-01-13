from threading import Thread
import requests
import sys, traceback
import json
import queue
from .client_logging import ClientLogging
from .exception import ServerRequestException, ThreadException, ConnectionException
from console_logging.console import Console
console = Console()
console.setVerbosity(5)


class ThreadMemorizer(object):
    """
    Description:
        This class is used for storing the threads detail that client creates for each event;
    """
    def __init__(self):
        self.dictionary_threads = {}


class EventThread(Thread):
    """
     Description:
        This class is used for storing the threads details that client creates for each event;

     Instance Variables:
        event: :`dict`={'case_id': `string`, 'activity': `string`} Event the thread is processing
        index: :int, It is the thread id that is incremented everytime a new thread created, starting from 0
        threadmemorizer: class `ThreadMemorizer` It is the dictionary to store some extra details of thread
        client_uuid: :`string` It is the username of the user that has initiated the client
        _status_queue: `Queue` It stores the status of the thread. For example - in case of exception the thread was cancelled.
    """
    def __init__(self, event, index, threadmemorizer, client_uuid):
        Thread.__init__(self)
        self.event = event
        self.client_uuid = client_uuid
        self.index = index
        self.threadmemorizer = threadmemorizer
        self._status_queue = queue.Queue()

    def wait_for_exc_info(self):
        """
        Description:
            It returns the data available in _status_queue
        :return: :`string` status
        """
        return self._status_queue.get()

    def join_with_exception(self):
        """
        Description:
            This function checks if there where any exceptions by checking the _status_queue.
            If there are exceptions in queue it raises an exception based on type of error.
        """
        ex_info = self.wait_for_exc_info()
        if ex_info is None:
            return
        elif isinstance(ex_info, ZeroDivisionError):
            console.error(traceback.format_exc())
            raise ThreadException(str(ex_info))
        else:
            raise ConnectionException

    def run(self):
        """
        Description:
            This function runs when the thread  starts.
            It requests the server by sending client_uuid and event
            The response returned from server is checked. If response status is not OK then it raises exception
            Else the response type is checked. The response message can be of type M,T, Error, OK
            M indicates that the event cannot happen. There is an event missing before it
            T indicates that the event can happen but the probability of it happening is very less(lesser than threshold)
            Error- indicates there was error in while checking alert
            OK- indicates there was no alert generated.
            Based on the message type mentioned above, the alerts are displayed on the screen for user
        """
        func_name = sys._getframe().f_code.co_name
        try:
            ClientLogging().log_info(func_name, self.client_uuid, self.index, self.event['case_id'],
                                     self.event['activity'],
                                     'Posting event to server:http://0.0.0.0:5000/compliance-checker')
            response = requests.post('http://0.0.0.0:5000/compliance-checker?uuid=' + self.client_uuid,
                              json=json.dumps(self.event))
            if response.status_code != 200:
                ClientLogging().log_error(func_name, self.client_uuid, self.index, self.event['case_id'],
                                          self.event['activity'],
                                          'Error by compliance checking')
                ServerRequestException('Failure by compliance checking').get_message()
            else:
                ClientLogging().log_info(func_name, self.client_uuid, self.index, self.event['case_id'],
                                         self.event['activity'],
                                         'The server response is: ' + response.text)
                response = response.json()
                for ws, message in response.items():
                    if message['body'] == 'M':
                        if message['source_node'] == 'NONE':
                            console.secure("[ Alert M  ]", " no such start node' " + message['sink_node'] + " 'in case ' " +
                                  message['case_id'] + "'")
                            if len(message['expect']) != 0:
                                print('    The expected start node:')
                                for s_node in message['expect']:
                                    print("\t'", s_node, "' with probability: ", message['expect'][s_node])
                        else:
                            console.secure('[ Alert M  ]', " no such connection in case '" + message['case_id'] + "'")
                            print('    The connection:', message['source_node'], '-->', message['sink_node'])
                            if len(message['expect']) != 0:
                                print('    The expected connection:')
                                for s_node in message['expect']:
                                    print('\t', message['source_node'], '-->', s_node, ': ', message['expect'][s_node])
                    elif message['body'] == 'T':
                        console.secure('[ Alert T  ]', " The threshold of the connection in case '" + message['case_id']
                                       + "' is too low.")
                        print('   The minimal expected probability from ', message['source_node'], '-->',
                              message['sink_node'], ': ', message['expect'])
                        print('               The true probability from ', message['source_node'], '-->',
                              message['sink_node'], ': ', message['cause'])
                    elif 'Error' in message['body']:
                        console.error(message['body'])
                    elif message['body'] != 'OK':
                        console.info(message['body'])
                    self._status_queue.put(None)
        except Exception as ec:
            console.error('Exception - in thread' + traceback.format_exc())
            ClientLogging().log_error(func_name, self.client_uuid, self.index, self.event['case_id'],
                                      self.event['activity'],
                                      'The server got disconnected, please try again later ')
            self._status_queue.put(ec)


