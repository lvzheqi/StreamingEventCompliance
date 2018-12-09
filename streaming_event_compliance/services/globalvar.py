#TODO: This file needs to be moved out of build automata and inclued in some other folder as global -
#TODO: common to both train and test
from streaming_event_compliance.database import dbtools

autos = {}
status = 0


def init():
    global autos, status
    autos, status = dbtools.init_automata_from_database()


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


T = ThreadMemorizer()
C = CaseMemorizer()