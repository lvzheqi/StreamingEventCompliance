from streaming_event_compliance.database import dbtools
from streaming_event_compliance.services.build_automata import build_automata


# Below are operations of autos and auto's status
autos = {}
status = 0
alert_logs = {}


def init():
    global autos, status
    autos, status = dbtools.init_automata_from_database()


def change_autos(key, value):
    autos[key] = value


def get_autos():
    return autos


def get_autos_status():
    return status


def call_buildautos():
    build_automata.build_automata()


def set_auto_status():
    global status
    status = 1


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


# Below are definitions and operations of various kinds of Memorizer of Compliance checking
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


client_alert_logs = {}

def get_client_alert_logs():
    client_alert_logs = {'client1':{'windowsize1':{},'windowsize2':{}},
                         'client2':{'windowsize1':{}, 'windowsize2':{}}}
    return client_alert_logs