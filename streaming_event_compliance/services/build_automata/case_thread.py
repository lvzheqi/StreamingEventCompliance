from threading import Thread
import time
from streaming_event_compliance.utils import config
from streaming_event_compliance.utils.config import WINDOW_SIZE, MAXIMUN_WINDOW_SIZE
from streaming_event_compliance.services import set_globalvar
from streaming_event_compliance.objects.automata import automata
from streaming_event_compliance.utils import dbtools

maximum_window_size = int(config.MAXIMUN_WINDOW_SIZE)


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

        # thread lock
        self.C.lock_List.get(self.event['case_id']).acquire()
        print('case ', self.event['case_id'], 'is locked, because ', self.event['activity'],
              'of this case is being processed.')
        print("we are checking the status of lock for this event:",
              self.C.lock_List.get(self.event['case_id']))
        if len(self.C.dictionary_cases.get(self.event['case_id'])) < MAXIMUN_WINDOW_SIZE:
            windows_memory = self.C.dictionary_cases.get(self.event['case_id'])
            print("windowsMemory of case ", self.event['case_id'], ':', windows_memory)

        else:
            windows_memory = self.C.dictionary_cases.get(self.event['case_id'])[0: MAXIMUN_WINDOW_SIZE]
            print("windowsMemory of case ", self.event['case_id'], ':', windows_memory)
            if self.C.dictionary_cases.get(self.event['case_id'])[MAXIMUN_WINDOW_SIZE-1] == self.event['activity']:
                print("\n*******current event is in the last of the memory*********\n")
            else:
                print("\n****somthing wrong!!***current event is not in the 5.positon of the memory*********\n")

        calcuate_connection_for_different_prefix_automata(windows_memory, self.event, self.T, self.C)

        self.C.lock_List.get(self.event['case_id']).release()
        print('case ', self.event['case_id'], 'is released', self.event['activity'],
              'of this case have been processed.')

        # TODO: Connect to the database
        # TODO: Store information of automata in database
        print(self, "until now ", time.time(), "the event ", self.event['activity'], "of case ",
              self.event['case_id'], "is done.")
        del self.T.dictionary_threads[self.index]







def calcuate_connection_for_different_prefix_automata(windowsMemory, event, T, C):
    """
    "autos" is a list of automata (global variable)
    :param windowsMemory: a list of activities from the same case_id of current event(another event),
                         size is maximum_window_size,
                         and the current event is in the last position of the windowsMemory
                         (i.e. event == windowsMemory[maximum_window_size-1])

    :param event:
    :return:
    """
    print('calcuateConnectionForDifferentPrefixAutomata for:','case:', event['case_id'], "activity:", event['activity'], 'with windowsMemory:', windowsMemory)
    # TODO: Calculating for one event in order to train automata
    time.sleep(1)
    autos = set_globalvar.get_autos()
    for ws in WINDOW_SIZE: # [1, 2, 3, 4]
        source_node = ''.join(windowsMemory[MAXIMUN_WINDOW_SIZE - ws - 1: MAXIMUN_WINDOW_SIZE-1])
        sink_node = ''.join(windowsMemory[MAXIMUN_WINDOW_SIZE - ws : MAXIMUN_WINDOW_SIZE])
        print("windowsize:",ws, "source_node:", source_node, "sink_node:", sink_node)
        print('test: ',automata.Connection(source_node, sink_node, 1))
        autos.get(ws).update_automata(automata.Connection(source_node, sink_node, 1))
    dbtools.insert_node_and_connection(autos)

    if len(C.dictionary_cases.get(event['case_id'])) > MAXIMUN_WINDOW_SIZE:
        C.dictionary_cases.get(event['case_id']).pop(0)
    print('case:', event['case_id'], "activity:", event['activity'], 'need to be deleted. after'
                                                                     'that caseMomory', C.dictionary_cases.get(event['case_id']))
