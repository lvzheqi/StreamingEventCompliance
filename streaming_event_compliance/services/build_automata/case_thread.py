from streaming_event_compliance import app
from streaming_event_compliance.objects.variable.globalvar import gVars, CL
from streaming_event_compliance.objects.automata import automata
from streaming_event_compliance.objects.exceptions.exception import ThreadException
from threading import Thread
import threading
import queue
import traceback
import sys

check_executing_order = {}
WINDOW_SIZE = app.config['WINDOW_SIZE']
MAXIMUN_WINDOW_SIZE = app.config['MAXIMUN_WINDOW_SIZE']

class CaseThreadForTraining(Thread):
    def __init__(self, event, index, T, C):
        self.event = event
        self.index = index
        self.T = T
        self.C = C
        Thread.__init__(self)
        self._status_queue = queue.Queue()

    def wait_for_exc_info(self):
        return self._status_queue.get()

    def join_with_exception(self):
        ex_info = self.wait_for_exc_info()
        if ex_info is None:
            return
        else:
            print('join exception')
            raise ThreadException(traceback.format_exc())

    def run(self):
        """
            In caseMemorier for every case we will store the last 4 events that have been processed,
            so for the current event processing event should in the 5. position. So after we processed
            one event, we should remove the first one from the list. And if in the 5. position we don't
            have event, that means currently all the events from this case has been processed.
            This thread can do noting excepting waiting.
            But during the processing the list will change, some events will be added into it,
        """
        global index
        try:
            if self.event['activity'] != '~!@#$%':
                if self.C.lock_List.get(self.event['case_id']).acquire():
                    windows_memory = self.C.dictionary_cases.get(self.event['case_id'])[0: MAXIMUN_WINDOW_SIZE + 1]

                    '''--------for checking threads error--------'''
                    if len(windows_memory) != 5:
                        print('----len(windows_memory) is not 5')
                    if self.event['activity'] != windows_memory[MAXIMUN_WINDOW_SIZE]:
                        pass
                    '''---------for checking threads error--------'''

                    calcuate_connection_for_different_prefix_automata(windows_memory)
                    if len(self.C.dictionary_cases.get(self.event['case_id'])) > MAXIMUN_WINDOW_SIZE:
                        self.C.dictionary_cases.get(self.event['case_id']).pop(0)

                    global check_executing_order
                    '''--------For Testing: Before releasing lock, which thread used it will be stored-------'''
                    if check_executing_order.get(self.event['case_id']):
                        check_executing_order.get(self.event['case_id']).append(self.event['activity'])
                    else:
                        check_executing_order[self.event['case_id']] = []
                        check_executing_order[self.event['case_id']].append(self.event['activity'])
                    '''--------For Testing: Before releasing lock, which thread used it will be stored-------'''
                    self.C.lock_List.get(self.event['case_id']).release()
                    self._status_queue.put(None)
            elif self.event['activity'] == '~!@#$%':
                if self.C.lock_List.get(self.event['case_id']).acquire():
                    windows_memory = self.C.dictionary_cases.get(self.event['case_id'])[0: MAXIMUN_WINDOW_SIZE + 1]

                    '''---------for checking threads error--------'''
                    if self.event['activity'] != windows_memory[MAXIMUN_WINDOW_SIZE]:
                        pass
                    '''---------for checking threads error--------'''

                    calcuate_connection_for_different_prefix_automata(windows_memory)
                    if len(self.C.dictionary_cases.get(self.event['case_id'])) > MAXIMUN_WINDOW_SIZE:
                        self.C.dictionary_cases.get(self.event['case_id']).pop(0)
                    self.C.lock_List.get(self.event['case_id']).release()
                    self._status_queue.put(None)
        except Exception:
                print('Caselock', traceback.format_exc())
                self._status_queue.put(sys.exc_info())


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
    :return：
    """
    for ws in WINDOW_SIZE:  # [1, 2, 3, 4]
        source_node = ','.join(windowsMemory[MAXIMUN_WINDOW_SIZE - ws: MAXIMUN_WINDOW_SIZE])
        sink_node = ','.join(windowsMemory[MAXIMUN_WINDOW_SIZE - ws + 1: MAXIMUN_WINDOW_SIZE + 1])
        if CL.lock_list.get((source_node, sink_node)):
            if CL.lock_list.get((source_node, sink_node)).acquire():
                try:
                    if windowsMemory[MAXIMUN_WINDOW_SIZE] == '~!@#$%' and source_node.find('*') == -1:
                        gVars.autos.get(ws).update_automata(automata.Connection(source_node, '~!@#$%', 0))
                    elif source_node.find('*') == -1:
                        gVars.autos.get(ws).update_automata(automata.Connection(source_node, sink_node, 1))
                    elif source_node.find('*') != -1 and sink_node.find('*') == -1:
                        gVars.autos.get(ws).update_automata(automata.Connection('NONE', sink_node, 1))
                    CL.lock_list.get((source_node, sink_node)).release()
                except Exception as ec:
                    raise ec
        else:
            lock = threading.RLock()
            CL.lock_list[source_node, sink_node] = lock
            if CL.lock_list.get((source_node, sink_node)).acquire():
                try:
                    if windowsMemory[MAXIMUN_WINDOW_SIZE] == '~!@#$%' and source_node.find('*') == -1:
                        gVars.autos.get(ws).update_automata(automata.Connection(source_node, '~!@#$%', 0))
                    elif source_node.find('*') == -1:
                        gVars.autos.get(ws).update_automata(automata.Connection(source_node, sink_node, 1))
                    CL.lock_list.get((source_node, sink_node)).release()
                except Exception as ec:
                    raise ec

