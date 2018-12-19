from streaming_event_compliance.objects.variable.globalvar import gVars, T, C, CL, CCM, CTM, CAL
from streaming_event_compliance.database import dbtools
from streaming_event_compliance.objects.automata import alertlog


def init_automata():
    gVars.autos, gVars.auto_status = dbtools.init_automata_from_database()


def clear_build_automata_memorizer():
    T.clear_memorizer()
    C.clear_memorizer()
    CL.clear_memorizer()


def init_compliance_checking(client_uuid):
    gVars.alert_logs[client_uuid] = {1: alertlog.AlertLog(),
                                     2: alertlog.AlertLog(),
                                     3: alertlog.AlertLog(),
                                     4: alertlog.AlertLog()}
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
