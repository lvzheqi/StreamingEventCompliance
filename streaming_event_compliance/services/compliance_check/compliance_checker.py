from streaming_event_compliance.services import visualization_deviation_automata
from streaming_event_compliance.services.compliance_check import case_thread_cc
from streaming_event_compliance.services import globalvar
from streaming_event_compliance.utils.config import MAXIMUN_WINDOW_SIZE
import threading
from streaming_event_compliance.database import dbtools
from streaming_event_compliance.objects.exceptions.exception import ThreadException
from streaming_event_compliance.objects.automata import alertlog
import traceback
import json


def compliance_checker(client_uuid, event):
    """
    This function will do compliance checking for each event from the streaming data provided from client_uuid.

    It will first check the global variable 'autos', to check if tt's status is true,
    if it's false, that means the automata has not built, return this information into user;
    if it's true, then it will get initialed CCM(Case memory for 'client_uuid') and CTM(Thread memory for
        'client_uuid'), and check firstly if this particular client_uuid is already in them,
        if yes, add the current event into CCM(corresponding key 'client_uuid'),
                create a thread for this event,
                add this thread into CTM(corresponding key 'client_uuid')
                start this thread
        if no, add this client_uuid into CCM and CTM, do the same thing as above.

    if the current event is endEvent, then it will join all threads for the streaming event provided from
    client_uuid, and insert this client_uuid and all alerts into database, after doing this, it will generate
    the visualization of deviation automata, return the url getting this pdf into user.

    :param client_uuid:
    :param event:
    :return:
    """
    if globalvar.get_autos_status():
        alert_logs = globalvar.get_alert_logs()
        alert_logs[client_uuid] = {1: alertlog.AlertLog(client_uuid, 1),
                                   2: alertlog.AlertLog(client_uuid, 2),
                                   3: alertlog.AlertLog(client_uuid, 3),
                                   4: alertlog.AlertLog(client_uuid, 4)}

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
                thread.start()
                message = thread.get_message().get()
                return json.dumps(message)
            except Exception:
                raise ThreadException(traceback.format_exc())
        else:
            client_cases = CCM.dictionary_cases.get(client_uuid)
            client_threads = CTM.dictionary_threads.get(client_uuid)
            client_locks = CCM.lock_List.get(client_uuid)
            if event['case_id'] != 'NONE' and event['activity'] != 'END':
                if event['case_id'] in client_cases:
                    client_cases.get(event['case_id']).append(event['activity'])
                    thread = case_thread_cc.CaseThreadForCC(event, client_uuid)
                    try:
                        thread.start()
                        client_threads.get(client_uuid).append(thread)
                        message = thread.get_message().get()
                        print(message, 'message')
                        return json.dumps(message)
                    except Exception:
                        raise ThreadException(traceback.format_exc())
                else:
                    client_cases[event['case_id']] = ['*' for i in range(0, MAXIMUN_WINDOW_SIZE)]
                    client_cases[event['case_id']].append(event['activity'])
                    thread = case_thread_cc.CaseThreadForCC(event, client_uuid)
                    lock = threading.Lock()
                    client_locks[event['case_id']] = lock
                    try:
                        thread.start()
                        client_threads[client_uuid] = [thread]
                        message = thread.get_message().get()
                        print(message)
                        return json.dumps(message)
                    except Exception:
                        raise ThreadException(traceback.format_exc())
            elif event['case_id'] == 'NONE' and event['activity'] == 'END':
                try:
                    for th in client_threads.get(client_uuid):
                        th.join_with_exception()
                except Exception:
                    raise ThreadException(traceback.format_exc())
                else:
                    alert_logs = globalvar.get_alert_logs()
                    dbtools.create_user(client_uuid)
                    dbtools.insert_alert_log(alert_logs.get(client_uuid))
                    visualization_deviation_automata.build_deviation_pdf(client_uuid)
                    dbtools.update_user_status(client_uuid, True)
                    response = 'The compliance checking is over, you can get the deviation pdf!'
                    return response
    else:
        response = 'Sorry, automata has not built, please wait for a while!'
        return response
