from pm4py.objects.log.importer.xes import factory as xes_importer
from pm4py.objects.log import transform
from simulationStreamEvent import eventThread
import json

T = eventThread.ThreadMemorizer()
threads = []
threads_index = 0


def read_log(path):
    trace_log = xes_importer.import_log(path)
    event_log = transform.transform_trace_log_to_event_log(trace_log)
    event_log.sort()
    return event_log


def simulate_stream_event(client_uuid, event_log):
    for event in event_log:
        dic = {}
        for item in event.keys():
            if item == 'concept:name':
                dic['activity'] = event.get(item)
            elif item == 'case:concept:name':
                dic['case_id'] = event.get(item)
        invoke_event_thread(json.dumps(dic), T, client_uuid)
    end_message = {'case_id': 'NONE', 'activity': 'END'}
    invoke_event_thread(json.dumps(end_message), T, client_uuid)


def invoke_event_thread(event, T, client_uuid):
    global threads_index
    while len(threads) > 3:
        threads[0].join()
        del threads[0]
    print('length of threads: ', len(threads))
    event_thread = eventThread.EventThread(event, T, threads_index, client_uuid)
    T.dictionary_threads[threads_index] = event_thread
    event_thread.start()
    threads.append(event_thread)
    threads_index = threads_index + 1
