from pm4py.objects.log.importer.xes import factory as xes_importer
from pm4py.objects.log import transform
from . import eventthread

from .client_logging import ClientLogging
from .exception import ReadFileException, ThreadException
import sys, time
from console_logging.console import Console
console = Console()
console.setVerbosity(5)

threads = []


def read_log(client_uuid, path):
    """
    Description:
        This function reads the log file provided by the user. It reads it, converts to event log file
        and then sorts it.
    :param client_uuid: :`string`  It is the username of the user that has initiated the client
    :param path: :`string` It is the trace log path provided by user while running the client
    :return: `list` It is sorted event logs
    """
    func_name = sys._getframe().f_code.co_name
    try:
        console.secure('Path:', str(path))
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
    """
    Description:
        This function uses the event log converts each event into a dict with keys as 'activity' and 'case_id'
        and calls the invoke_event_thread function for each event dict.

    :param client_uuid: :`string` It is the username of the user that has initiated the client
    :param event_log: :`list` It is a list of all the events in the sorted form
    """
    global threads
    func_name = sys._getframe().f_code.co_name
    sum = len(event_log)

    start = time.clock()
    for event in event_log:
        dic = {}
        for item in event.keys():
            if item == 'concept:name':
                dic['activity'] = event.get(item)
            elif item == 'case:concept:name':
                dic['case_id'] = event.get(item)
        ClientLogging().log_info(func_name, client_uuid, dic['case_id'], dic['activity'],
                                 'Calling invoke_event_thread()')
        if len(threads) > 1000:
            try:
                for th in threads:
                    th.join_with_exception()
            except ThreadException as ec:
                raise ThreadException(str(ec))
            threads = []

        invoke_event_thread(dic, client_uuid)

    end = time.clock()
    runtime = end - start
    results = sum / runtime
    console.secure('[ Events_number  ]', str(sum))
    console.secure('[ Running time  ]', str(runtime))
    console.secure('[ Average speed  ]', str(results) + ' per second!\n')

    end_message = {'case_id': 'NONE', 'activity': 'END'}
    ClientLogging().log_info(func_name, client_uuid, end_message['case_id'], end_message['activity'],
                             'Calling invoke_event_thread()')
    invoke_event_thread(end_message, client_uuid)

    try:
        for th in threads:
            th.join_with_exception()
    except ThreadException as ec:
        raise ThreadException(str(ec))


def invoke_event_thread(event, client_uuid):
    """
    Description:
        This function starts a thread for each event.
        Index indicates a thread_id. Everytime a thread is created the index is
        incremented by 1 to get new thread_id for the next event.

    :param event: :`dict`={'case_id': `string`, 'activity': `string`}
    :param client_uuid: :`string` It is the username of the user that has initiated the client
    """

    func_name = sys._getframe().f_code.co_name
    ClientLogging().log_info(func_name, client_uuid, event['case_id'], event['activity'], 'Initialising thread')
    event_thread = eventthread.EventThread(event, client_uuid)
    ClientLogging().log_info(func_name, client_uuid, event['case_id'], event['activity'], 'Starting thread for event ')
    event_thread.start()
    threads.append(event_thread)



