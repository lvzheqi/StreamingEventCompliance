from threading import Thread
from streaming_event_compliance import app
from streaming_event_compliance.objects.variable.globalvar import gVars, CCM, CAL
from streaming_event_compliance.objects.exceptions.exception import ThreadException
from streaming_event_compliance.objects.automata import automata, alertlog
from streaming_event_compliance.objects.logging.server_logging import ServerLogging
import queue, sys, traceback
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
        else:
            console.error(traceback.format_exc())
            raise ThreadException(str(ex_info))

    def get_message(self):
        return self._message

    def run(self):
        """
        Description:
            This function acquires lock on caseMemorizer and releases lock when processing of the
            event is done. The event, which has done the compliance checking, will be removed.
            This function provide 2 ways to do the compliance checking, respectively `DELETE_M_EVENT` and
            `KEEP_ALL_EVENTS`.
        """
        func_name = sys._getframe().f_code.co_name
        client_cases = self.CCM.dictionary_cases.get(self.client_uuid)
        client_locks = self.CCM.lock_List.get(self.client_uuid)
        try:
            if client_locks.get(self.event['case_id']).acquire():
                ServerLogging().log_info(func_name, self.client_uuid, self.index, self.event['case_id'],
                                         self.event['activity'], "Acquiring lock for event case: " + self.event['case_id'])
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
                                         self.event['activity'], "Released lock for event case: " + self.event['case_id'])
                self._message.put(response)
                self._status_queue.put(None)
        except Exception as ec:
            ServerLogging().log_info(func_name, self.client_uuid, self.index, self.event['case_id'],
                                     self.event['activity'],
                                     "in this thread's _status_queue ec is putted in: " + traceback.format_exc())
            self._status_queue.put(ec)


def create_source_sink_node(windows_memory, client_uuid, event, thread_id):
    """
    Description:
        This function creates sink node and source node based on prefix sizes and call function to
        check compliance with automata. Let the source node be NONE and sink node be the node,
        if it is the start node.

    :param windows_memory: :`list` a list of activities from the same case_id of current event(another event) with
                         size `maximum_window_size`, and the current event is at the last position of the windowsMemory
    :param client_uuid: :`string` client-id
    :param event: :`dict`={'case_id': `string`, 'activity': `string`}
    :param thread_id: :int, the id of the thread that is running the compliance check

    :return: `json` {
                        'body': other information (Mandatory)
                        'case_id':	case id (Option)
                        'source_node': source node of the current connection, with separator `,` (Option)
                        'sink_node': sink node of the current connection, with separator `,` (Option)
                        'cause': alert cause of the current connection
                                    {M: missing, T: lower than threshold}(Option)
                        'expect': expect connection (Option)
                    }
    """
    response = {}
    func_name = sys._getframe().f_code.co_name
    try:
        for ws in WINDOW_SIZE:
            source_node = ','.join(windows_memory[MAXIMUN_WINDOW_SIZE - ws: MAXIMUN_WINDOW_SIZE])
            sink_node = ','.join(windows_memory[MAXIMUN_WINDOW_SIZE - ws + 1: MAXIMUN_WINDOW_SIZE + 1])
            if source_node.find('*') != -1 and sink_node.find('*') != -1:
                response[str(ws)] = {'body': 'OK'}
                break
            elif source_node.find('*') != -1:
                source_node = 'NONE'

            lock_list = CAL.c_alerts_lock_list.get(client_uuid)
            if (source_node, sink_node) not in lock_list:
                lock = threading.Lock()
                lock_list[source_node, sink_node] = lock
                ServerLogging().log_info(func_name, client_uuid, thread_id, event['case_id'],
                                          event['activity'],
                                          "the lock has been created: " + source_node + " to " + sink_node)

            matches = check_alert(ws, source_node, sink_node, client_uuid, event, thread_id)
            if matches == 2:
                response[str(ws)] = {
                    'case_id': event['case_id'],
                    'source_node': source_node,
                    'sink_node': sink_node,
                    'expect': gVars.autos[ws].get_sink_nodes(source_node),
                    'body': 'M'
                }
                if ALERT_TYPE == 'RETURN_ONE':
                    return response
            elif matches == 1:
                response[str(ws)] = {
                    'case_id': event['case_id'],
                    'source_node': source_node,
                    'sink_node': sink_node,
                    'cause': gVars.autos[ws].get_connection_probability(automata.Connection(source_node, sink_node)),
                    'expect': THRESHOLD,
                    'body': 'T'
                }
            else:
                response[str(ws)] = {'body': 'OK'}
        return response
    except Exception as ec:
        console.error(traceback.format_exc())
        raise ec


def check_alert(window_size, source_node, sink_node, client_uuid, event, thread_id):
    """
        Description:
            This function takes sink_node, source_node and checks if the automata of 'windowsize'
            has any source_node and sink_node that matches tbe source_node, sink_node. If
            there is a match then checks for its probability ,if probability below than threshold (Alert Typ: T) or
            no match found (Alert Typ: M) then it inserts data to Alertlog object and returns an alert messsage.

        :param window_size: :int, the length of the automata node
        :param source_node: :`string` source node combination in fixed size, with separator `,`
        :param sink_node: :`string` sink node combination in fixed size, with separator `,`
        :param client_uuid: :`string` client-id
        :param event: :dict`={'case_id': `string`, 'activity': `string`}
        :param thread_id: :int, the id of the thread that is running the compliance check

        :return: :int: {0: OK, 1: Alert, lower threshold, 2: Alert, no such connection}
    """
    lock_list = CAL.c_alerts_lock_list.get(client_uuid)
    func_name = sys._getframe().f_code.co_name
    ServerLogging().log_info(func_name, client_uuid, thread_id, event['case_id'],
                              event['activity'], "the lock is in the lock_list: " + source_node + " to " + sink_node)
    alert_log = gVars.get_client_alert_logs(client_uuid)[window_size]
    auto = gVars.autos[window_size]
    conn = automata.Connection(source_node, sink_node)
    if auto.contains_connection(conn):
        if auto.get_connection_probability(conn) >= THRESHOLD:
            return 0
        else:
            try:
                if lock_list.get((source_node, sink_node)).acquire():
                    ServerLogging().log_info(func_name, client_uuid, thread_id, event['case_id'],
                                             event['activity'],
                                             "Acquiring lock for alert: " + "(" + source_node + " to " + sink_node + ")")
                    alert_log.update_alert_record(
                        alertlog.AlertRecord (client_uuid, source_node, sink_node, 1, 'T'))
                    ServerLogging().log_info(func_name, client_uuid, thread_id, event['case_id'],
                                              event['activity'], "Alert raised as probability of "
                                                                 "connection between " +
                                              source_node + " and " + sink_node + " is lesser than threshold")
            except Exception as ec:
                ServerLogging().log_info(func_name, client_uuid, thread_id, event['case_id'], event['activity'],
                                          "Exception by check_alert between " + source_node
                                          + " and " + sink_node)
                console.error(traceback.format_exc())
                raise ec
            else:
                lock_list.get((source_node, sink_node)).release()
                ServerLogging().log_info(func_name, client_uuid, thread_id, event['case_id'],
                                         event['activity'],
                                         "Release lock for alert: " + "(" + source_node + " to " + sink_node + ")")
                return 1
    elif source_node == 'NONE' and auto.contains_source_node(sink_node):
        return 0
    else:
        try:
            if lock_list.get((source_node, sink_node)).acquire():
                ServerLogging().log_info(func_name, client_uuid, thread_id, event['case_id'],
                                         event['activity'],
                                         "Acquiring lock for alert: " + "(" + source_node + " to " + sink_node + ")")
                alert_log.update_alert_record(alertlog.AlertRecord(client_uuid, source_node, sink_node, 1, 'M'))
                ServerLogging().log_info(func_name, client_uuid, thread_id, event['case_id'], event['activity'],
                                         "Alert raised as there should not be connection between " + source_node
                                         + " and " + sink_node)
        except Exception:
            ServerLogging().log_info(func_name, client_uuid, thread_id, event['case_id'], event['activity'],
                                      "Exception by check_alert between " + source_node
                                      + " and " + sink_node)
            console.error(traceback.format_exc())
        else:
            lock_list.get((source_node, sink_node)).release()
            ServerLogging().log_info(func_name, client_uuid, thread_id, event['case_id'],
                                     event['activity'],
                                     "Release lock for alert: " + "(" + source_node + " to " + sink_node + ")")
            return 2
