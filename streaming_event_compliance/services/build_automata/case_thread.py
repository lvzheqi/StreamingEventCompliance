from threading import Thread
import time
from streaming_event_compliance.utils.config import WINDOW_SIZE, MAXIMUN_WINDOW_SIZE
from streaming_event_compliance.services import set_globalvar
from streaming_event_compliance.objects.automata import automata

check_executing_order = {}


class CaseThreadForTraining(Thread):
    def __init__(self, event, index,  T, C):
        self.event = event
        self.index = index
        self.T = T
        self.C = C
        Thread.__init__(self)

    def run(self):
        """
        in caseMemorier every case we will memory the last 5 events that have been processed,
        so for the current event processing event should in the 6. position? So after we processed
        one event, we should delete the first one in the list. And if in the 6. position we don't
        have event, that means currently all the events from this case has been processed.
        This thread can do noting excepting waiting.
        But during the processing the list will change, some events will be added into it,
        how do we let the thread know that?
        """
        print(self, "Now ", time.time(), "the event ", self.event['activity'], "of case ",
              self.event['case_id'], "is started.")

        print("we are checking the status of lock for this event:",
              self.C.lock_List.get(self.event['case_id']))
        # Acquire the thread lock for current event
        self.C.lock_List.get(self.event['case_id']).acquire()
        print('case ', self.event['case_id'], 'is locked, because ', self.event['activity'],
              'of this case is being processed.')

        # Calculate windows_memory for each event
        if len(self.C.dictionary_cases.get(self.event['case_id'])) < MAXIMUN_WINDOW_SIZE+1:
            windows_memory = self.C.dictionary_cases.get(self.event['case_id'])
        else:
            windows_memory = self.C.dictionary_cases.get(self.event['case_id'])[0: MAXIMUN_WINDOW_SIZE+1]

        calcuate_connection_for_different_prefix_automata(windows_memory)
        if len(self.C.dictionary_cases.get(self.event['case_id'])) > MAXIMUN_WINDOW_SIZE:
            self.C.dictionary_cases.get(self.event['case_id']).pop(0)

        '''--------For Testing: Before releasing lock, which thread used it will be stored-------'''
        if check_executing_order.get(self.event['case_id']):
            check_executing_order.get(self.event['case_id']).append(self.event['activity'])
        else:
            check_executing_order[self.event['case_id']] = []
            check_executing_order[self.event['case_id']].append(self.event['activity'])
        '''--------For Testing: Before releasing lock, which thread used it will be stored-------'''

        self.C.lock_List.get(self.event['case_id']).release()

        # Release the thread lock for current event
        print('case ', self.event['case_id'], 'is released', self.event['activity'],
              'of this case have been processed.')
        return "test return value"

def calcuate_connection_for_different_prefix_automata(windowsMemory):
    """
    "autos" is a list of automata (global variable)
    Connect to the database
    Store information of automata in database
    :param windowsMemory: a list of activities from the same case_id of current event(another event),
                         size is maximum_window_size,
                         and the current event is in the last position of the windowsMemory
                         (i.e. event == windowsMemory[maximum_window_size])

    :param event:
    :return:
    """
    autos, status = set_globalvar.get_autos()
    for ws in WINDOW_SIZE:# [1, 2, 3, 4]
        source_node = ','.join(windowsMemory[MAXIMUN_WINDOW_SIZE - ws: MAXIMUN_WINDOW_SIZE])
        sink_node = ','.join(windowsMemory[MAXIMUN_WINDOW_SIZE - ws + 1: MAXIMUN_WINDOW_SIZE+1])
        if source_node.find('*') == -1:
            autos.get(ws).update_automata(automata.Connection(source_node, sink_node, 1))


