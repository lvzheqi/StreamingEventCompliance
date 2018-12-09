from pm4py.objects.log.importer.xes import factory as xes_importer
from pm4py.objects.log import transform
from . import eventthread
from .client_logging import ClientLogging
from .exception import ReadFileException
import time
import sys

threads = []
T = eventthread.ThreadMemorizer()
index = 0


def read_log(client_uuid, path):
    func_name = sys._getframe().f_code.co_name
    try:
        ClientLogging().log_info(func_name, client_uuid, "Creating a trace logger file: ")
        trace_log = xes_importer.import_log(path)
        ClientLogging().log_info(func_name, client_uuid, "Transforming trace logger to event logger")
        event_log = transform.transform_trace_log_to_event_log(trace_log)
        ClientLogging().log_info(func_name, client_uuid, "Sorting event logger")
        event_log.sort()
    except Exception:
        ClientLogging().log_error(func_name, client_uuid, "Sorting event logger")
        raise ReadFileException(path)
    return event_log


def simulate_stream_event(client_uuid, event_log):
    func_name = sys._getframe().f_code.co_name
    for event in event_log:
        dic = {}
        for item in event.keys():
            time.sleep(.1)
            if item == 'concept:name':
                dic['activity'] = event.get(item)
            elif item == 'case:concept:name':
                dic['case_id'] = event.get(item)
        ClientLogging().log_info(func_name, client_uuid, dic['case_id'], dic['activity'], "Calling invoke_event_thread()")
        invoke_event_thread(dic, client_uuid)
    end_message = {'case_id': 'NONE', 'activity': 'END'}
    ClientLogging().log_info(func_name, client_uuid, end_message['case_id'], end_message['activity'], "Calling invoke_"
                                                                                                     "event_thread()")
    invoke_event_thread(end_message, client_uuid)


def invoke_event_thread(event, client_uuid):
    global index
    func_name = sys._getframe().f_code.co_name
    ClientLogging().log_info(func_name, client_uuid, event['case_id'], event['activity'], "Initialising thread")
    event_thread = eventthread.EventThread(event, index, T,  client_uuid)
    ClientLogging().log_info(func_name, client_uuid, event['case_id'], event['activity'], "Starting thread for event ")
    event_thread.start()
    threads.append(event_thread)
    index = index + 1



