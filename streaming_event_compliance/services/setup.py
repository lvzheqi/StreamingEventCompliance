from streaming_event_compliance.objects.variable.globalvar import gVars, T, C, CL, CCM, CTM, CAL
from streaming_event_compliance.database import dbtools
from streaming_event_compliance.objects.automata import alertlog
from streaming_event_compliance.utils.config import WINDOW_SIZE

# from streaming_event_compliance import app
# WINDOW_SIZE = app.config['WINDOW_SIZE']


def init_automata():
    gVars.autos, gVars.auto_status = dbtools.init_automata_from_database()


def init_client_alert_automata(uuid):
    alogs = gVars.get_client_alert_logs(uuid)
    if alogs is None:
        return dbtools.init_alert_log_from_database(uuid)
    else:
        return alogs, 1


def clear_build_automata_memorizer():
    T.clear_memorizer()
    C.clear_memorizer()
    CL.clear_memorizer()


def init_compliance_checking(client_uuid):
    gVars.alert_logs[client_uuid] = {}
    for ws in WINDOW_SIZE:
        gVars.alert_logs[client_uuid][ws] = alertlog.AlertLog()
    CCM.init_client_memorizer(client_uuid)
    CTM.init_client_memorizer(client_uuid)
    CAL.init_client_memorizer(client_uuid)


def clear_cc_memorizer(client_uuid):
    gVars.alert_logs.pop(client_uuid)
    CCM.dictionary_cases.pop(client_uuid)
    CTM.dictionary_threads.pop(client_uuid)
    CCM.lock_List.pop(client_uuid)
    CAL.c_alerts_lock_list.pop(client_uuid)
    gVars.clients_cc_status.pop(client_uuid)
