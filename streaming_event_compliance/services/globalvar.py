from streaming_event_compliance.database import dbtools
from streaming_event_compliance.services.build_automata import build_automata
from streaming_event_compliance.objects.automata import alertlog


# Below are operations of autos and auto's status
autos = {}
auto_status = 0
alert_logs = {}
users = {}

indexN = 0


def set_index():
    global indexN
    indexN += 1


def get_index():
    return indexN


def init():
    global autos, auto_status
    autos, auto_status = dbtools.init_automata_from_database()


def change_autos(key, value):
    global autos
    autos[key] = value


def get_autos():
    return autos


def set_auto_status():
    global auto_status
    auto_status = 1


def get_autos_status():
    return auto_status


def call_buildautos():
    build_automata.build_automata()


def get_alert_logs():
    test_alertlog()
    return alert_logs


def get_user_alert_logs(uuid):
    return alert_logs[uuid]


def set_user(uuid, status):
    global users
    users[uuid] = status


def get_users():
    return users


# Below are definitions and operations of various kinds of Memorizer of building automata
class ThreadMemorizer(object):
    '''
    This object is for storing the threads that server creates for each case;
    '''

    def __init__(self):
        self.dictionary_threads = {}


class CaseMemorizer(object):
    '''
    This object is for storing the cases that server receives;

    key:'case_id'
    value:[a,b,c,d...] events sorting by timestamp, but we don't need to sort these events, and it also doesn't contain any timestamp
                    but the events are sent by Client in the order of time, even they are sent by multi-threads, the server will get
                    these events in the order of time. So when server get a event, it can only check its case_id and add it into the
                    corresponding list.
    '''

    def __init__(self):
        self.dictionary_cases = {}
        self.lock_List = {}


class ConnectionsLocker(object):
    '''
    This object is for storing the threads that server creates for each case;
    '''

    def __init__(self):
        self.lock_List = {}


T = ThreadMemorizer()
C = CaseMemorizer()
CL = ConnectionsLocker()


def clear_memorizer():
    T.dictionary_threads = {}
    C.dictionary_cases = {}
    C.lock_List = {}


def get_connection_locks():
    return CL


def get_case_memory():
    return C


def get_thread_memory():
    return T


class ClientThreadMemorizer(object):
    def __init__(self):
        self.client_number = 0
        self.dictionary_threads = {}


class ClientCaseMemorizer(object):
    def __init__(self):
        self.client_number = 0
        self.dictionary_cases = {}
        self.lock_List = {}


CTM = ThreadMemorizer()
CCM = CaseMemorizer()


def get_client_case_memory():
    return CCM


def get_client_thread_memory():
    return CTM


def test_alertlog():
    global alert_logs
    uuid = 'client1'
    alog1 = alertlog.AlertLog(uuid, 1)
    alog2 = alertlog.AlertLog(uuid, 2)
    alog3 = alertlog.AlertLog(uuid, 3)
    alog4 = alertlog.AlertLog(uuid, 4)
    alog1.update_alert_record(alertlog.AlertRecord(uuid, 'a', 'd', 4, 'M'))
    alog1.update_alert_record(alertlog.AlertRecord(uuid, 'a', 'f', 2, 'M'))
    alog1.update_alert_record(alertlog.AlertRecord(uuid, 'd', 'b', 1, 'M'))
    alog1.update_alert_record(alertlog.AlertRecord(uuid, 'a', 'e', 1, 'T'))
    alog2.update_alert_record(alertlog.AlertRecord(uuid, 'a,d', 'd,b', 1, 'M'))
    alog2.update_alert_record(alertlog.AlertRecord(uuid, 'd,b', 'b,c', 1, 'M'))
    alog3.update_alert_record(alertlog.AlertRecord(uuid, 'a,d,b', 'd,b,c', 1, 'M'))
    alog3.update_alert_record(alertlog.AlertRecord(uuid, 'd,b,c', 'b,c,d', 1, 'M'))
    alog4.update_alert_record(alertlog.AlertRecord(uuid, 'a,d,b,c', 'd,b,c,d', 1, 'M'))
    alogs = {1: alog1, 2: alog2, 3: alog3, 4: alog4}
    alert_logs[uuid] = alogs
