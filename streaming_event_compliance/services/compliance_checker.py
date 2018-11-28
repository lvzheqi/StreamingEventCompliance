from streaming_event_compliance.services import deviation_pdf
from streaming_event_compliance.services.build_automata import case_thread
from streaming_event_compliance.services.globalvar import ThreadMemorizer,CaseMemorizer

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

    print('case_id: ', event['case_id'])
    print('activity: ', event['activity'])
    if event['case_id'] != 'NONE' and event['activity'] != 'END':
        for key in C.dictionary_cases:
            if key == event['case_id']:
                # if we have already found the case, just add this event to this case, But should
                #we search in caseMemory or theathMemory??
                C.dictionary_cases.get(event['case_id']).append(event['activity'])
                # Do we need restart the thread for this case?
            else:
                #1. Add it to the caseMemory
                #2. Create a new thread for this case
                #3. Start it
                C.dictionary_cases[event['case_id']] = [event['activity']]
                thread = case_thread.CaseThread(event, T, C, threads_index, client_uuid)
                #TODO: what does caseThread do?
                T.dictionary_threads[threads_index] = case_thread
                # this is just for remember the threads information that we have ceated.
                thread.start()
                threads.append(case_thread) # this is for limiting the number of the threads that are runing???
                threads_index = threads_index + 1

        while len(threads) > 3:
            threads[0].join()  #TODO: Jingjing: why we need to join these threads?
            del threads[0]     # why we delete?

        # TODO: analyse and write non-compliance event to the database AlertLog with client_uuid
    else:
        deviation_pdf.build_deviation_pdf(client_uuid)
    # deviation information should be returned here, or we return it form thread.start()
    return 'deviation'


def error_handle():
    return "error"

