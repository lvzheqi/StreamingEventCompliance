from streaming_event_compliance.services import deviation_pdf
from streaming_event_compliance.services.compliance_check import case_thread_cc
from streaming_event_compliance.services import globalvar
from streaming_event_compliance.utils.config import MAXIMUN_WINDOW_SIZE
from streaming_event_compliance.services.compliance_check.compare_automata import  client_alert_logs
import threading
import queue
import json

threads = []
threads_index = 0


def compliance_checker(client_uuid, event):
    '''
    This function creates a case_memorizer for each case_id and starts thread.
    The threads return "deviation" message at the end if there is any deviation
    for the event
    :param client_uuid: user name
    :param event: the event that we want to check the compliance
    :return:the deviation information or success information.
    '''
    if globalvar.get_autos_status():
        C = globalvar.get_case_memory()
        T = globalvar.get_thread_memory()
        print(event['case_id'] + " " + event['activity'])
        global threads_index
        if event['case_id'] != 'NONE' and event['activity'] != 'END':
            if event['case_id'] in C.dictionary_cases:
                    # 1. Append the incoming event to already existing caseMemory of the with same case_id
                    # 2. Create a new thread for this case
                    # 3. Start it
                    C.dictionary_cases.get(event['case_id']).append(event['activity'])
                    thread = case_thread_cc.CaseThreadForCC(event, threads_index, T, C, client_uuid)
                    T.dictionary_threads[threads_index] = case_thread_cc
                    try:
                        thread_queue = queue.Queue()
                        thread = threading.Thread(target=thread.thread_run, args=[thread_queue])
                        thread.start()
                        threads.append(case_thread_cc)
                        threads_index = threads_index + 1
                        response = thread_queue.get()
                        print(response)
                        return json.dumps(response)
                    except KeyboardInterrupt:
                        print('Error: Thread is interrupt!')
                        response = {
                            'case_id': None,
                            'source_node': None,
                            'sink_node': None,
                            'cause': None,
                            'message': 'Server Error'
                        }
                        return response
            else:
                    # 1. Add it to the caseMemory
                    # 2. Create a new thread for this case
                    # 3. Start it
                    C.dictionary_cases[event['case_id']] = ['*' for i in range(0, MAXIMUN_WINDOW_SIZE)]
                    C.dictionary_cases[event['case_id']].append(event['activity'])
                    thread = case_thread_cc.CaseThreadForCC(event, threads_index, T, C, client_uuid)
                    T.dictionary_threads[threads_index] = case_thread_cc
                    lock = threading.Lock()
                    # Create a lock for the new case
                    C.lock_List[event['case_id']] = lock
                    # this is just for remember the threads information that we have ceated.
                    try:
                        thread_queue = queue.Queue()
                        thread = threading.Thread(target=thread.thread_run, args=[thread_queue])
                        thread.start()
                        threads.append(case_thread_cc)
                        threads_index = threads_index + 1
                        response = thread_queue.get()
                        print(response)
                        return json.dumps(response)
                    except KeyboardInterrupt:
                        print('Error: Thread is interrupt!')
                        response = {
                            'case_id': None,
                            'source_node': None,
                            'sink_node': None,
                            'cause': None,
                            'message': 'Server Error'
                        }
                        return response
             # while len(threads) > 3:
             #   threads[0].join()  #TODO: Jingjing: why we need to join these threads?
             #  del threads[0]     # why we delete?

         # TODO: analyse and write non-compliance event to the database AlertLog with client_uuid
         # TODO: Sabya Remove the below elif... This portion is only for now to show the content of alert logs...
         # TODO: After inserting Alert_logs into table remove this below elif part
        elif event['case_id'] == 'NONE' and event['activity'] == 'END':
            print(client_alert_logs)
            response = {
                'case_id': None,
                'source_node': None,
                'sink_node': 'End',
                'cause': None,
                'message': 'OK'
            }
            return response
        else:
            deviation_pdf.build_deviation_pdf(client_uuid)
        # deviation information should be returned here, or we return it form thread.start()
            response = {
                'case_id': None,
                'source_node': None,
                'sink_node': None,
                'cause': None,
                'message': 'PDF'
            }
            return response
    # return event['case_id'] + "->" + event['activity']
    response = {
        'case_id': None,
        'source_node': None,
        'sink_node': None,
        'cause': None,
        'message': 'Automata not built!'
    }
    return response


def error_handle():
    return "error"

