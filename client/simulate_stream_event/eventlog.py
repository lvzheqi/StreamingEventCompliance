from pm4py.objects.log.importer.xes import factory as xes_importer
from pm4py.objects.log import transform
from . import eventthread, client_logging
from .exception import ReadFileException
import time
import sys

threads = []


def read_log(client_uuid, path):
    func_name = sys._getframe().f_code.co_name
    try:
        client_logging.client_logging(message_type="INFO", level="DEBUG", func_name=func_name, username=client_uuid,
                                      message="Creating a trace logger file: ")
        trace_log = xes_importer.import_log(path)
        client_logging.client_logging(message_type="INFO", level="DEBUG", func_name=func_name, username=client_uuid,
                                      message="Transforming trace logger to event logger")
        event_log = transform.transform_trace_log_to_event_log(trace_log)
        client_logging.client_logging(message_type="INFO", level="DEBUG", func_name=func_name, username=client_uuid,
                                      message="Sorting event logger")
        event_log.sort()
    except Exception:
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
        client_logging.client_logging(message_type="INFO", level="DEBUG", func_name=func_name, username=client_uuid,
                                      case_id=dic['case_id'],
                                      activity=dic['activity'],
                                      message="Calling invoke_event_thread()")
        invoke_event_thread(dic, client_uuid)
    end_message = {'case_id': 'NONE', 'activity': 'END'}
    client_logging.client_logging(message_type="INFO", level="DEBUG", func_name=func_name, username=client_uuid,
                                  case_id=end_message['case_id'],
                                  activity=end_message['activity'],
                                  message="Calling invoke_event_thread()")
    invoke_event_thread(end_message, client_uuid)


def invoke_event_thread(event, client_uuid):
    func_name = sys._getframe().f_code.co_name
    client_logging.client_logging(message_type="INFO", level="DEBUG", func_name=func_name, username=client_uuid,
                                  case_id=event['case_id'],
                                  activity=event['activity'],
                                  message="Initialising thread")
    event_thread = eventthread.EventThread(event, client_uuid)
    client_logging.client_logging(message_type="INFO", level="DEBUG", func_name=func_name, username=client_uuid,
                                  case_id=event['case_id'],
                                  activity=event['activity'],
                                  message="Starting thread for event ")
    event_thread.start()
    threads.append(event_thread)



