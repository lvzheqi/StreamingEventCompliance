from pm4py.objects.log.importer.xes import factory as xes_importer
from pm4py.objects.log import transform
from . import eventthread
from .client_logging import ClientLogging
from .exception import ReadFileException, ConnectionException, ThreadException
import sys
from console_logging.console import Console
console = Console()
console.setVerbosity(5)

threads = []
T = eventthread.ThreadMemorizer()
index = 0


def read_log(client_uuid, path):
    '''
    Description:
        This function reads the log file provided by the user. It reads it, converts to event log file and then sorts it.
    :param client_uuid::str: It is the username of the user that has initiated the client
    :param path::str: It is the trace log path provided by user while running the client
    :return: event_log::list: It is sorted event logs
    '''
    func_name = sys._getframe().f_code.co_name
    try:
        ClientLogging().log_info(func_name, client_uuid, 'Creating a trace logger file: ')
        trace_log = xes_importer.import_log(path)
        ClientLogging().log_info(func_name, client_uuid, 'Transforming trace logger to event logger')
        event_log = transform.transform_trace_log_to_event_log(trace_log)
        ClientLogging().log_info(func_name, client_uuid, 'Sorting event logger')
        event_log.sort()
    except Exception:
        raise ReadFileException(path)
    return event_log


def simulate_stream_event(client_uuid, event_log):
    '''
    Description:
        This function uses the event log converts each event into a dict with keys as 'activity' and 'case_id'
        and calls the invoke_event_thread function for each event dict.
    :param client_uuid::str: It is the username of the user that has initiated the client
    :param event_log::list: It is a list of all the events in the sorted form
    '''
    func_name = sys._getframe().f_code.co_name
    for event in event_log:
        dic = {}
        for item in event.keys():
            if item == 'concept:name':
                dic['activity'] = event.get(item)
            elif item == 'case:concept:name':
                dic['case_id'] = event.get(item)
        ClientLogging().log_info(func_name, client_uuid, dic['case_id'], dic['activity'],
                                 'Calling invoke_event_thread()')
        event_thread = invoke_event_thread(dic, client_uuid)
        try:
            event_thread.join_with_exception()
        except ConnectionException:
            raise ConnectionException
        except ThreadException as ec:
            raise ThreadException(str(ec))

    end_message = {'case_id': 'NONE', 'activity': 'END'}
    ClientLogging().log_info(func_name, client_uuid, end_message['case_id'], end_message['activity'],
                             'Calling invoke_event_thread()')
    invoke_event_thread(end_message, client_uuid)


def invoke_event_thread(event, client_uuid):
    '''
    Description:
        This function starts a thread for each event.
        Index indicates a thread_id. Everytime a thread is created the index is
        incremented by 1 to get new thread_id for the next event.
    :param event: :`dict`={'case_id': `string`, 'activity': `string`}
    :param client_uuid::str: It is the username of the user that has initiated the client
    :return: event_thread::class client.simulate_stream_event.eventlog.EventThread : It is the class for the thread
    '''
    global index
    func_name = sys._getframe().f_code.co_name
    ClientLogging().log_info(func_name, client_uuid, event['case_id'], event['activity'], 'Initialising thread')
    event_thread = eventthread.EventThread(event, index, T,  client_uuid)
    ClientLogging().log_info(func_name, client_uuid, event['case_id'], event['activity'], 'Starting thread for event ')
    event_thread.start()
    threads.append(event_thread)
    index = index + 1
    return event_thread


