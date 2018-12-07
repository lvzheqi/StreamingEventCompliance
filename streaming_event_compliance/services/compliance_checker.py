from streaming_event_compliance.services import deviation_pdf
from streaming_event_compliance.services.compliance_check import case_thread_cc
from streaming_event_compliance.services.globalvar import ThreadMemorizer, CaseMemorizer
from streaming_event_compliance.utils.config import MAXIMUN_WINDOW_SIZE
import threading

T = ThreadMemorizer()
C = CaseMemorizer()
threads = []
threads_index = 0


def compliance_checker(client_uuid, event):
    '''
    Does the compliance checking of the particular event received from client by comparing
    the automata information in the database. Returns alerts, when some deviations occur.
    :param client_uuid: user name
    :param event: the event that we want to check the compliance
    :return:the deviation information or success information.
    '''
    global threads_index
    if event['case_id'] != 'NONE' and event['activity'] != 'END':
        if event['case_id'] in C.dictionary_cases:
                C.dictionary_cases.get(event['case_id']).append(event['activity'])
                thread = case_thread_cc.CaseThreadForCC(event, threads_index, T, C, client_uuid)
                T.dictionary_threads[threads_index] = case_thread_cc
                try:
                    thread.start()
                    threads.append(case_thread_cc)  # this is for limiting the number of the threads that are runing???
                    threads_index = threads_index + 1
                except KeyboardInterrupt:
                    print('Error: Thread is interrupt!')
                # Do we need restart the thread for this case?
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
                    thread.start()
                    threads.append(case_thread_cc)  # this is for limiting the number of the threads that are runing???
                    threads_index = threads_index + 1
                except KeyboardInterrupt:
                    print('Error: Thread is interrupt!')

         # while len(threads) > 3:
         #   threads[0].join()  #TODO: Jingjing: why we need to join these threads?
         #  del threads[0]     # why we delete?

        # TODO: analyse and write non-compliance event to the database AlertLog with client_uuid
    else:
        deviation_pdf.build_deviation_pdf(client_uuid)
    # deviation information should be returned here, or we return it form thread.start()
    return 'deviation'


def error_handle():
    return "error"

