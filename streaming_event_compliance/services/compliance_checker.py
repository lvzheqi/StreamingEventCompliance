from streaming_event_compliance.services import visualization_deviation_automata
from streaming_event_compliance.services.compliance_check import case_thread_cc
from streaming_event_compliance.services import globalvar
from streaming_event_compliance.utils.config import MAXIMUN_WINDOW_SIZE
import threading
import queue
from streaming_event_compliance.database import dbtools


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
        CCM = globalvar.get_client_case_memory()
        CTM = globalvar.get_client_thread_memory()
        if client_uuid not in CCM.dictionary_cases:
            CCM.dictionary_cases[client_uuid] = {}
            CTM.dictionary_threads[client_uuid] = {}
            CCM.lock_List[client_uuid] = {}
            client_cases = CCM.dictionary_cases.get(client_uuid)
            client_threads = CTM.dictionary_threads.get(client_uuid)
            client_locks = CCM.lock_List.get(client_uuid)

            client_cases[event['case_id']] = ['*' for i in range(0, MAXIMUN_WINDOW_SIZE)]
            client_cases[event['case_id']].append(event['activity'])
            thread = case_thread_cc.CaseThreadForCC(event, client_uuid)
            client_threads[client_uuid] = [thread]
            lock = threading.Lock()
            client_locks[event['case_id']] = lock
            try:
                thread_queue = queue.Queue()
                thread = threading.Thread(target=thread.thread_run, args=[thread_queue])
                thread.start()
                response = thread_queue.get()
                print(response)
                return response
            except KeyboardInterrupt:
                print('Error: Thread is interrupt!')
                return "Server Error!"

        else:
            client_cases = CCM.dictionary_cases.get(client_uuid)
            client_threads = CTM.dictionary_threads.get(client_uuid)
            client_locks = CCM.lock_List.get(client_uuid)
            if event['case_id'] != 'NONE' and event['activity'] != 'END':
                if event['case_id'] in client_cases:
                    client_cases.get(event['case_id']).append(event['activity'])
                    thread = case_thread_cc.CaseThreadForCC(event, client_uuid)
                    try:
                        thread_queue = queue.Queue()
                        thread = threading.Thread(target=thread.thread_run, args=[thread_queue])
                        thread.start()
                        client_threads.get(client_uuid).append(thread)
                        response = thread_queue.get()
                        return response
                    except KeyboardInterrupt:
                        print('Error: Thread is interrupt!')
                        return "Server Error!"
                else:
                    client_cases[event['case_id']] = ['*' for i in range(0, MAXIMUN_WINDOW_SIZE)]
                    client_cases[event['case_id']].append(event['activity'])
                    thread = case_thread_cc.CaseThreadForCC(event, client_uuid)
                    lock = threading.Lock()
                    client_locks[event['case_id']] = lock
                    try:
                        thread_queue = queue.Queue()
                        thread = threading.Thread(target=thread.thread_run, args=[thread_queue])
                        thread.start()
                        client_threads[client_uuid] = [thread]
                        response = thread_queue.get()
                        print(response)
                        return response
                    except KeyboardInterrupt:
                        print('Error: Thread is interrupt!')
                        return "Server Error!"

             # TODO: analyse and write non-compliance event to the database AlertLog with client_uuid
             # TODO: Sabya Remove the below elif... This portion is only for now to show the content of alert logs...
             # TODO: After inserting Alert_logs into table remove this below elif part
            elif event['case_id'] == 'NONE' and event['activity'] == 'END':
                alert_logs = globalvar.get_alert_logs()
                print(alert_logs)
                for th in client_threads.get(client_uuid):
                    try:
                        th.join_with_exception()
                    except Exception as ec:
                        print(ec.__class__)
                        print(th, "---is not join due to exception")
                    else:
                        # update the alert log for particular client into database
                        dbtools.create_user(client_uuid)
                        dbtools.insert_alert_log(alert_logs.get(client_uuid))
                        visualization_deviation_automata.build_deviation_pdf(client_uuid)
                        dbtools.update_user_status()
                    finally:
                        pass
                        # if dbtools.check_user_status(client_uuid):
                        #     return "OK, deviation_pdf is also build!"
                        # else:
                        #     return "something wrong"
    else:
        return "automata is not build"


def error_handle():
    return "error"

