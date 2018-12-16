from threading import Thread
from streaming_event_compliance.utils.config import WINDOW_SIZE, MAXIMUN_WINDOW_SIZE
from . import compare_automata
from streaming_event_compliance.services import globalvar
from streaming_event_compliance.objects.exceptions.exception import ThreadException
import sys
import queue

class CaseThreadForCC(Thread):
    def __init__(self, event, client_uuid):
        self.event = event
        self.CCM = globalvar.get_client_case_memory()
        self.client_uuid = client_uuid
        self._status_queue = queue.Queue()
        self._message = queue.Queue()
        Thread.__init__(self)

    def wait_for_exc_info(self):
        return self._status_queue.get()

    def join_with_exception(self):
        ex_info = self.wait_for_exc_info()
        if ex_info is None:
            return
        else:
            raise ThreadException(ex_info[1])

    def get_message(self):
        return self._message

    def run(self):
        """
        in caseMemorizer every case we will memory the last 4 events that have been processed,
        so, the current processing event will be in the 5th  position. So after processing
        one event, we delete the first one in the list. And if in the 5th position we don't
        have any event, that means currently all the events from this case has been processed.
        This function acquires lock on caseMemorizer and releases lock when processing of the
        event is done
        """
        client_cases = self.CCM.dictionary_cases.get(self.client_uuid)
        client_locks = self.CCM.lock_List.get(self.client_uuid)
        try:
            if client_locks.get(self.event['case_id']).acquire():
                if len(client_cases.get(self.event['case_id'])) < MAXIMUN_WINDOW_SIZE + 1:
                    windows_memory = client_cases.get(self.event['case_id'])
                else:
                    windows_memory = client_cases.get(self.event['case_id'])[0: MAXIMUN_WINDOW_SIZE + 1]
                message = create_source_sink_node(windows_memory, self.client_uuid)
                if len(client_cases.get(self.event['case_id'])) > MAXIMUN_WINDOW_SIZE:
                    client_cases.get(self.event['case_id']).pop(0)
                client_locks.get(self.event['case_id']).release()
                self._message.put(message)
                self._status_queue.put(None)
        except Exception:
            self._status_queue.put(sys.exc_info())


def create_source_sink_node(windowsMemory, client_uuid):
    """
    Create sink node and source node based on prefix sizes and call function to check compliance with automata in db
    :param windowsMemory: a list of activities from the same case_id of current event(another event),
                         size is maximum_window_size,
                         and the current event is at the last position of the windowsMemory
                         (i.e. event == windowsMemory[maximum_window_size])
    :return:
    """
    for ws in WINDOW_SIZE:# [1, 2, 3, 4]
        # print(windowsMemory)
        source_node = ','.join(windowsMemory[MAXIMUN_WINDOW_SIZE - ws: MAXIMUN_WINDOW_SIZE])
        sink_node = ','.join(windowsMemory[MAXIMUN_WINDOW_SIZE - ws + 1: MAXIMUN_WINDOW_SIZE+1])
        if source_node.find('*') == -1:
            # print('WS: ' + str(ws) + ' Source: ' + source_node + ' Sink: ' + sink_node)
            matches = compare_automata.check_automata_with_source_sink(ws, source_node, sink_node, client_uuid)
            if matches == 0:
                print("Alert !!!  No connection from " + source_node + " to " + sink_node)
                return "Alert !!!  No connection from " + source_node + " to " + sink_node
            else:
                return "OK"
        elif source_node.find('*') != -1 and sink_node.find('*') == -1:
            # print('WS: ' + str(ws) + ' Source: ' + source_node + ' Sink: ' + sink_node)
            matches = compare_automata.check_automata_only_sourcenode(ws, sink_node, client_uuid)
            if matches == 0:
                print("Alert !!!  No connection from " + source_node + " to " + sink_node)
                return "Alert !!!  No connection from " + source_node + " to " + sink_node
            else:
                return "OK"

    # TODO: Implement returning to main function ALERT, Threading comments to be removed ,
    # TODO: When and where to save alert into db
    # TODO: if an event detected as alert what to do given option at start to keep or remove it from windows memory
