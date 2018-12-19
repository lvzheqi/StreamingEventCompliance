from streaming_event_compliance.objects.variable.globalvar import gVars, CAL
from streaming_event_compliance.utils.config import THRESHOLD
from streaming_event_compliance.objects.automata import alertlog, automata
import traceback, threading
from console_logging.console import Console
console = Console()
console.setVerbosity(5)

def check_alert(windowsize, source_node, sink_node, client_uuid):
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
        :return: alert message
    '''
    lock_list = CAL.c_alerts_lock_list.get(client_uuid)
    try:
        alert_log = gVars.get_client_alert_logs(client_uuid)[windowsize]
        auto = gVars.autos[windowsize]
        # console.info(auto)
        conn = automata.Connection(source_node, sink_node)
        if auto.contains_connection(conn):
            if auto.get_connection_probability(conn) >= THRESHOLD:
                return 0
            else:
                if lock_list.get((source_node, sink_node)):
                    if lock_list.get((source_node, sink_node)).acquire():
                        alert_log.update_alert_record(alertlog.AlertRecord(client_uuid, source_node, sink_node, 1, 'T'))
                        lock_list.get((source_node, sink_node)).release()
                        return 1
                else:
                    lock = threading.RLock()
                    lock_list[source_node, sink_node] = lock
                    if lock_list.get((source_node, sink_node)).acquire():
                        alert_log.update_alert_record(alertlog.AlertRecord(client_uuid, source_node, sink_node, 1, 'T'))
                        lock_list.get((source_node, sink_node)).release()
                        return 1
        elif source_node == 'NONE' and auto.contains_source_node(sink_node):
            return 0
        else:
            if lock_list.get((source_node, sink_node)):
                if lock_list.get((source_node, sink_node)).acquire():
                    alert_log.update_alert_record(alertlog.AlertRecord(client_uuid, source_node, sink_node, 1, 'M'))
                    lock_list.get((source_node, sink_node)).release()
                    return 2
            else:
                lock = threading.RLock()
                lock_list[source_node, sink_node] = lock
                if lock_list.get((source_node, sink_node)).acquire():
                    alert_log.update_alert_record(alertlog.AlertRecord(client_uuid, source_node, sink_node, 1, 'M'))
                    lock_list.get((source_node, sink_node)).release()
                    return 2
    except Exception as ec:
        raise ec
