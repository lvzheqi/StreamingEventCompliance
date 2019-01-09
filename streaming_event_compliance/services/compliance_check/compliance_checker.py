from streaming_event_compliance.services import setup
from streaming_event_compliance.services.visualization import visualization_deviation_automata
from streaming_event_compliance.services.compliance_check import case_thread_cc
from streaming_event_compliance.objects.variable.globalvar import gVars, CCM, CTM
from streaming_event_compliance import app
import threading
from streaming_event_compliance.database import dbtools
from streaming_event_compliance.objects.exceptions.exception import ThreadException
from streaming_event_compliance.objects.logging.server_logging import ServerLogging
import traceback
import json
import os, sys
from console_logging.console import Console

console = Console()
console.setVerbosity(5)
MAXIMUN_WINDOW_SIZE = app.config['MAXIMUN_WINDOW_SIZE']
THRESHOLD = app.config['THRESHOLD']
CLEINT_DATA_PATH = app.config['CLEINT_DATA_PATH']
AUTOMATA_FILE = app.config['AUTOMATA_FILE']
FILE_TYPE = app.config['FILE_TYPE']
threads = []
threads_index = 0

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
    func_name = sys._getframe().f_code.co_name
    global threads_index, threads
    if gVars.auto_status:
        client_cases = CCM.dictionary_cases.get(client_uuid)
        client_threads = CTM.dictionary_threads.get(client_uuid)
        client_locks = CCM.lock_List.get(client_uuid)
        if event['case_id'] != 'NONE' and event['activity'] != 'END':
            if event['case_id'] in client_cases:
                client_cases.get(event['case_id']).append(event['activity'])
                thread = case_thread_cc.CaseThreadForCC(event, threads_index, client_uuid)
                try:
                    thread.start()
                    client_threads.get(client_uuid).append(thread)
                    threads.append(thread)
                    threads_index = threads_index + 1
                    return json.dumps(thread.get_message().get())
                except Exception:
                    console.error('compliance_checker' + traceback.format_exc())
                    ServerLogging().log_error(func_name, client_uuid, "Exception raised while starting thread")
                    raise ThreadException(traceback.format_exc())
            else:
                client_cases[event['case_id']] = ['*' for i in range(0, MAXIMUN_WINDOW_SIZE)]
                client_cases[event['case_id']].append(event['activity'])
                thread = case_thread_cc.CaseThreadForCC(event, threads_index, client_uuid)
                lock = threading.Lock()
                client_locks[event['case_id']] = lock
                try:
                    thread.start()
                    client_threads[client_uuid] = [thread]
                    threads.append(thread)
                    threads_index = threads_index + 1
                    return json.dumps(thread.get_message().get())
                except Exception:
                    console.error('compliance_checker' + traceback.format_exc())
                    ServerLogging().log_error(func_name, client_uuid, "Exception raised while starting thread.")
                    raise ThreadException(traceback.format_exc())
        elif event['case_id'] == 'NONE' and event['activity'] == 'END':
            for th in client_threads.get(client_uuid):
                try:
                    th.join_with_exception()
                except ZeroDivisionError:
                    print(traceback.format_exc())
                    ServerLogging().log_error(func_name, client_uuid, "Exception raised while joining thread.")
                except ThreadException as ec:
                    console.error('compliance_checker' + traceback.format_exc())
                    ServerLogging().log_error(func_name, client_uuid, "Exception raised while joining thread.")
                    raise ThreadException(str(ec))
                except Exception:
                    ServerLogging().log_error(func_name, client_uuid, "Exception raised while joining thread.")
                    console.error(traceback.format_exc())
            alert_log = gVars.get_client_alert_logs(client_uuid)
            dbtools.create_client(client_uuid)
            dbtools.insert_alert_log(alert_log)
            path = CLEINT_DATA_PATH + client_uuid + '_' + AUTOMATA_FILE + FILE_TYPE
            if os.path.exists(path):
                os.remove(path)
            ServerLogging().log_info(func_name, client_uuid, "showing pdf")
            visualization_deviation_automata.show_deviation_pdf(client_uuid)
            ServerLogging().log_info(func_name, client_uuid, "Setting client status to true as compliance checking is completed for that client")
            dbtools.update_client_status(client_uuid, True)
            gVars.clients_status[client_uuid] = True
            ServerLogging().log_info(func_name, client_uuid, "Clearing memorizers for client- "+ client_uuid)
            setup.clear_cc_memorizer(client_uuid)
            ServerLogging().log_info(func_name, client_uuid, "Compliance checking is finished.")
            return json.dumps({'End': {'body': 'The compliance checking is over, you can get the deviation pdf!'}})
    else:
        ServerLogging().log_error(func_name, client_uuid, "Automata is not built!")
        return json.dumps({'End': {'body': 'Sorry, automata has not built, please wait for a while!'}})
