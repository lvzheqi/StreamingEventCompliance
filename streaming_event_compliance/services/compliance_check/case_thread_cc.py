from threading import Thread
from streaming_event_compliance import app
from streaming_event_compliance.objects.variable.globalvar import gVars, CCM, CAL
from streaming_event_compliance.objects.exceptions.exception import ThreadException
from streaming_event_compliance.objects.automata import automata, alertlog
from streaming_event_compliance.objects.logging.server_logging import ServerLogging
import queue, sys
import traceback
import threading
from console_logging.console import Console
console = Console()
console.setVerbosity(5)

WINDOW_SIZE = app.config['WINDOW_SIZE']
MAXIMUN_WINDOW_SIZE = app.config['MAXIMUN_WINDOW_SIZE']
THRESHOLD = app.config['THRESHOLD']
CHECKING_TYPE = app.config['CHECKING_TYPE']
ALERT_TYPE = app.config['ALERT_TYPE']


class CaseThreadForCC(Thread):
    def __init__(self, event, index, client_uuid):
        self.event = event
        self.CCM = CCM
        self.client_uuid = client_uuid
        self._status_queue = queue.Queue()
        self._message = queue.Queue()
        self.index = index
        Thread.__init__(self)

    def wait_for_exc_info(self):
        return self._status_queue.get()

    def join_with_exception(self):
        ex_info = self.wait_for_exc_info()
        if ex_info is None:
            return
        elif isinstance(ex_info, ZeroDivisionError):
            raise ThreadException(str(ex_info))
        else:
            raise Exception

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
        func_name = sys._getframe().f_code.co_name
        client_cases = self.CCM.dictionary_cases.get(self.client_uuid)
        client_locks = self.CCM.lock_List.get(self.client_uuid)
        try:
            if client_locks.get(self.event['case_id']).acquire():
                ServerLogging().log_info(func_name, self.client_uuid, self.index, self.event['case_id'],
                                         self.event['activity'], "Acquiring lock")
                windows_memory = client_cases.get(self.event['case_id'])[0: MAXIMUN_WINDOW_SIZE + 1]
                response = create_source_sink_node(windows_memory, self.client_uuid, self.event, self.index)
                ServerLogging().log_info(func_name, self.client_uuid, self.index, self.event['case_id'],
                                         self.event['activity'],
                                         "Calculating response")
                flag = True
                for ws, res in response.items():
                    if ws == min(WINDOW_SIZE) and res.get('body') == 'M' and CHECKING_TYPE == 'DELETE_M_EVENT':
                        flag = False
                        client_cases.get(self.event['case_id']).pop(MAXIMUN_WINDOW_SIZE)
                if flag:
                    client_cases.get(self.event['case_id']).pop(0)
                client_locks.get(self.event['case_id']).release()
                ServerLogging().log_info(func_name, self.client_uuid, self.index, self.event['case_id'],
                                         self.event['activity'], "Released lock")
                self._message.put(response)
                self._status_queue.put(None)
        except Exception as ec:
            console.error('run - ComplianceCaselock ' + traceback.format_exc())
            ServerLogging().log_error(func_name, self.client_uuid, self.index, self.event['case_id'], self.event['activity'],
                                      "Error with Caselock")
            self._status_queue.put(ec)


def create_source_sink_node(windowsMemory, client_uuid, event, thread_id):
    '''
    Create sink node and source node based on prefix sizes and call function to check compliance with automata in db
    :param windowsMemory: a list of activities from the same case_id of current event(another event),
                         size is maximum_window_size,
                         and the current event is at the last position of the windowsMemory
                         (i.e. event == windowsMemory[maximum_window_size])
    :param client_uuid: user name
    :param event: the event for which the compliance is being checked
    :param thread_id: the id of the thread that is running the compliance check
    :return:
    '''
    response = {}
    func_name = sys._getframe().f_code.co_name
    try:
        for ws in WINDOW_SIZE:
            source_node = ','.join(windowsMemory[MAXIMUN_WINDOW_SIZE - ws: MAXIMUN_WINDOW_SIZE])
            sink_node = ','.join(windowsMemory[MAXIMUN_WINDOW_SIZE - ws + 1: MAXIMUN_WINDOW_SIZE+1])
            if source_node.find('*') != -1 and sink_node.find('*') != -1:
                response[ws] = {'body': 'OK'}
                break
            elif source_node.find('*') != -1:
                source_node = 'NONE'
            matches = check_alert(ws, source_node, sink_node, client_uuid, event, thread_id)
            if matches == 2:
                response[ws] = {
                    'case_id': event['case_id'],
                    'source_node': source_node,
                    'sink_node': sink_node,
                    'expect': gVars.autos[ws].get_sink_nodes(source_node),
                    'body': 'M'
                }
                if ALERT_TYPE == 'RETURN_ONE':
                    return response
            elif matches == 1:
                response[ws] = {
                    'case_id': event['case_id'],
                    'source_node': source_node,
                    'sink_node': sink_node,
                    'cause': gVars.autos[ws].get_connection_probability(automata.Connection(source_node, sink_node)),
                    'expect': THRESHOLD,
                    'body': 'T'
                }
            else:
                response[ws] = {'body': 'OK'}
        return response
    except Exception as ec:
        ServerLogging().log_error(func_name, client_uuid, thread_id, event['case_id'], event['activity'], "Exception raised while creating sink_node and source_node")
        console.error('Exception from create_source_sink_node:' + traceback.format_exc())
        raise ec


def check_alert(windowsize, source_node, sink_node, client_uuid, event, thread_id):
    '''
        This function takes sink_node, source_node and checks if the automata of 'windowsize'
        has any source_node and sink_node that matches tbe source_node, sink_node  passed. If
        there is a match then checks for its probability ,if probability below than threshold or
        no match found then it inserts data to Alertlog object and returns an alert messsage
        The automata is retrieved directly from 'autos' variable rather than db. This autos
        variable was initialized when automata was built using training set
        :param windowsize: The length of the automata node.
        :param sink_node: the combination of event that we want to check the compliance for and
               the additional events(based on window size)
        :param client_uuid: user name
        :param event: the event for which the compliance is being checked
        :param thread_id: the id of the thread that is running the compliance check
        :return: alert message
    '''
    lock_list = CAL.c_alerts_lock_list.get(client_uuid)
    func_name = sys._getframe().f_code.co_name
    try:
        alert_log = gVars.get_client_alert_logs(client_uuid)[windowsize]
        auto = gVars.autos[windowsize]
        conn = automata.Connection(source_node, sink_node)
        if auto.contains_connection(conn):
            if auto.get_connection_probability(conn) >= THRESHOLD:
                return 0
            else:
                if lock_list.get((source_node, sink_node)):
                    if lock_list.get((source_node, sink_node)).acquire():
                        alert_log.update_alert_record(
                            alertlog.AlertRecord(client_uuid, source_node, sink_node, 1, 'T'))
                        ServerLogging().log_error(func_name, client_uuid, thread_id, event['case_id'], event['activity'],
                                                  "Alert raised as probability of connection between "+source_node +" and " + sink_node + " is lesser than threshold")
                        lock_list.get((source_node, sink_node)).release()
                        return 1
                else:
                    lock = threading.RLock()
                    lock_list[source_node, sink_node] = lock
                    if lock_list.get((source_node, sink_node)).acquire():
                        alert_log.update_alert_record(
                            alertlog.AlertRecord(client_uuid, source_node, sink_node, 1, 'T'))
                        ServerLogging().log_error(func_name, client_uuid, thread_id, event['case_id'], event['activity'],
                                                  "Alert raised as probability of connection between " + source_node + " and " + sink_node + " is lesser than threshold")
                        lock_list.get((source_node, sink_node)).release()
                        return 1
        elif source_node == 'NONE' and auto.contains_source_node(sink_node):
            return 0
        else:
            if lock_list.get((source_node, sink_node)):
                if lock_list.get((source_node, sink_node)).acquire():
                    alert_log.update_alert_record(alertlog.AlertRecord(client_uuid, source_node, sink_node, 1, 'M'))
                    ServerLogging().log_error(func_name, client_uuid, thread_id, event['case_id'], event['activity'],
                                              "Alert raised as there should not be connection between " + source_node + " and " + sink_node)
                    lock_list.get((source_node, sink_node)).release()
                    return 2
            else:
                lock = threading.RLock()
                lock_list[source_node, sink_node] = lock
                if lock_list.get((source_node, sink_node)).acquire():
                    alert_log.update_alert_record(alertlog.AlertRecord(client_uuid, source_node, sink_node, 1, 'M'))
                    ServerLogging().log_error(func_name, client_uuid, thread_id, event['case_id'], event['activity'],
                                              "Alert raised as there should not be connection between " + source_node + " and " + sink_node)
                    lock_list.get((source_node, sink_node)).release()
                    return 2
    except Exception as ec:
        ServerLogging().log_error(func_name, client_uuid, thread_id, event['case_id'], event['activity'], "Exception raised while checking alert")
        raise ec
