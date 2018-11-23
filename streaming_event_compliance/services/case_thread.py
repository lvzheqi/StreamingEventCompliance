from threading import Thread


class ThreadMemorizer(object):
    '''
    This object is for storing the threads that server creates for each case;
    '''
    def __init__(self):
        self.dictionary_threads = {} # key should be the case id, so we can know if the thread still exists ??

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



class CaseThread(Thread):
    def __init__(self, event, threadMemorizer, caseMemorizer, index, client_uuid):
        self.event = event
        self.threadMemorizer = threadMemorizer
        self.caseMemorizer = caseMemorizer
        self.index = index
        self.client_uuid = client_uuid
        Thread.__init__(self)

    def run(self):
        '''run what??
           in caseMemorier every case we will memory the last 5 events that have been processed, so for the current event processing
           event should in the 6. position? So after we processed one event, we should delete the first one in the list. And if in the
           6. position we don't have event, that means currently all the events from this case has been processed.
           This thread can do noting excepting waiting.
           But during the processing the list will change, some events will be added into it, how do we let the thread know that?
        '''

        # thread condition
        len(self.caseMemorizer.dictionary_cases.get(self.event[id])) > 5

        print(self)
        # del self.threadMemorizer.dictionary_threads[self.index] # we can not delete it even this event processing is done,
        # we should waiting another event from the same case?

