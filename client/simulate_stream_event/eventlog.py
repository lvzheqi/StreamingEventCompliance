from pm4py.objects.log.importer.xes import factory as xes_importer
from pm4py.objects.log import transform
from . import eventthread
import json
import time

threads = []


def read_log(path):
    trace_log = xes_importer.import_log(path)
    event_log = transform.transform_trace_log_to_event_log(trace_log)
    event_log.sort()
    return event_log


def simulate_stream_event(client_uuid, event_log):
    for event in event_log:
        dic = {}
        for item in event.keys():
            time.sleep(.1)
            if item == 'concept:name':
                dic['activity'] = event.get(item)
            elif item == 'case:concept:name':
                dic['case_id'] = event.get(item)
        invoke_event_thread(json.dumps(dic), client_uuid)
    end_message = {'case_id': 'NONE', 'activity': 'END'}
    invoke_event_thread(json.dumps(end_message), client_uuid)


def invoke_event_thread(event, client_uuid):
    event_thread = eventthread.EventThread(event, client_uuid)
    event_thread.start()
    threads.append(event_thread)



