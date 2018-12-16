from threading import Thread
import time
from streaming_event_compliance.utils.config import WINDOW_SIZE, MAXIMUN_WINDOW_SIZE
from . import compare_automata


class CaseThreadForCC(Thread):
    def __init__(self, event, index, T, C, client_uuid):
        self.event = event
        self.index = index
        self.T = T
        self.C = C
        self.client_uuid = client_uuid
        Thread.__init__(self)

    def run(self):
        """
        in caseMemorizer every case we will memory the last 4 events that have been processed,
        so, the current processing event will be in the 5th  position. So after processing
        one event, we delete the first one in the list. And if in the 5th position we don't
        have any event, that means currently all the events from this case has been processed.
        This function acquires lock on caseMemorizer and releases lock when processing of the
        event is done
        """
        # Acquire the thread lock for current event
        if self.C.lock_List.get(self.event['case_id']).acquire():
            # Calculate windows_memory for each event
            if len(self.C.dictionary_cases.get(self.event['case_id'])) < MAXIMUN_WINDOW_SIZE+1:
                windows_memory = self.C.dictionary_cases.get(self.event['case_id'])
            else:
                windows_memory = self.C.dictionary_cases.get(self.event['case_id'])[0: MAXIMUN_WINDOW_SIZE+1]
            create_source_sink_node(windows_memory, self.client_uuid, self.event)
            if len(self.C.dictionary_cases.get(self.event['case_id'])) > MAXIMUN_WINDOW_SIZE:
                self.C.dictionary_cases.get(self.event['case_id']).pop(0)
            self.C.lock_List.get(self.event['case_id']).release()

    def thread_run(self, thread_queue):
        # Acquire the thread lock for current event
        if self.C.lock_List.get(self.event['case_id']).acquire():
            # Calculate windows_memory for each event
            if len(self.C.dictionary_cases.get(self.event['case_id'])) < MAXIMUN_WINDOW_SIZE + 1:
                windows_memory = self.C.dictionary_cases.get(self.event['case_id'])
            else:
                windows_memory = self.C.dictionary_cases.get(self.event['case_id'])[0: MAXIMUN_WINDOW_SIZE + 1]
            message = create_source_sink_node(windows_memory, self.client_uuid, self.event)
            if len(self.C.dictionary_cases.get(self.event['case_id'])) > MAXIMUN_WINDOW_SIZE:
                self.C.dictionary_cases.get(self.event['case_id']).pop(0)
            self.C.lock_List.get(self.event['case_id']).release()
            thread_queue.put(message)


def create_source_sink_node(windowsMemory, client_uuid, event):
    """
    Create sink node and source node based on prefix sizes and call function to check compliance with automata in db
    :param windowsMemory: a list of activities from the same case_id of current event(another event),
                         size is maximum_window_size,
                         and the current event is at the last position of the windowsMemory
                         (i.e. event == windowsMemory[maximum_window_size])
    :return:
    """
    for ws in WINDOW_SIZE:# [1, 2, 3, 4]
        print(windowsMemory)
        source_node = ','.join(windowsMemory[MAXIMUN_WINDOW_SIZE - ws: MAXIMUN_WINDOW_SIZE])
        sink_node = ','.join(windowsMemory[MAXIMUN_WINDOW_SIZE - ws + 1: MAXIMUN_WINDOW_SIZE+1])
        if source_node.find('*') == -1:
            print('WS: ' + str(ws) + ' Source: ' + source_node + ' Sink: ' + sink_node)
            matches = compare_automata.check_automata_with_source_sink(ws, source_node, sink_node, client_uuid)
            if matches == 0:
                print("Alert !!!  No connection from " + source_node + " to " + sink_node + " due to missing node")
                response = {
                    'case_id': event['case_id'],
                    'source_node': sink_node,
                    'sink_node': None,
                    'cause': 'No such source node',
                    'message': 'Alert'
                }
                return response
            elif matches == 1:
                print("Alert !!!  No connection from " + source_node + " to " + sink_node + " due to less probability")
                response = {
                    'case_id': event['case_id'],
                    'source_node': sink_node,
                    'sink_node': None,
                    'cause': 'Probability less than threshold',
                    'message': 'Alert'
                }
                return response
        elif source_node.find('*') != -1 and sink_node.find('*') == -1:
            print('WS: ' + str(ws) + ' Source: ' + source_node + ' Sink: ' + sink_node)
            matches = compare_automata.check_automata_only_sourcenode(ws, sink_node, client_uuid)
            if matches == 0:
                print("Alert !!!  No connection from " + source_node + " to " + sink_node + " due to missing node")
                response = {
                    'case_id': event['case_id'],
                    'source_node': source_node,
                    'sink_node': sink_node,
                    'cause': 'No such connection',
                    'message': 'Alert'
                }
                return response
            elif matches == 1:
                print("Alert !!!  No connection from " + source_node + " to " + sink_node + " due to less probability")
                response = {
                    'case_id': event['case_id'],
                    'source_node': source_node,
                    'sink_node': sink_node,
                    'cause': 'Probability less than threshold',
                    'message': 'Alert'
                }
                return response
    response = {
        'case_id': event['case_id'],
        'source_node': source_node,
        'sink_node': sink_node,
        'cause': '',
        'message': 'OK'
    }
    return response

    # TODO: Implement returning to main function ALERT, Threading comments to be removed ,
    # TODO: When and where to save alert into db
    # TODO: if an event detected as alert what to do given option at start to keep or remove it from windows memory




    # TODO: JingjingHuo: run() and thread_run() keep one is enough;
    # TODO: JingjingHuo: thread_queue should be the attribute of this threadclass?
