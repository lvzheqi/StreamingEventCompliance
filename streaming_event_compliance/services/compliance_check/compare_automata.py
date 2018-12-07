from streaming_event_compliance.services import set_globalvar
from streaming_event_compliance.utils.config import THRESHOLD
from streaming_event_compliance.objects.automata import alertlog


def check_automata_startswith(windowsize, sink_node, client_uuid):
    '''
        This function takes sink_node and checks if the automata of 'windowsize'  has any
        source_node that starts with this sink_node. If yes then checks for its probability,
        if probability below than threshold or no match found for source_node starting with
        sink_node then insert data to Alertlog object and return alert message
        The automata is retrieved directly from 'autos' variable rather than db. This autos
        variable was initialized when automata was built using training set
        :param windowsize: The length of the automata node.
        :param sink_node: the combination of event that we want to check the compliance for and
               the additional events(based on window size)
        :param client_uuid: user name
        :return: alert message
    '''
    autos, status = set_globalvar.get_autos()
    alert_log = alertlog.AlertLog(client_uuid, windowsize)
    for connection in autos[windowsize].connections:
        if connection.source_node.startswith(sink_node):
            if connection.probability >= THRESHOLD:
                return 1
            else:
                alert_record = alertlog.AlertRecord(client_uuid, None, sink_node, 1)# source_node=None in case its an initial node
                alert_log.add_alert_record(alert_record)
                print("alert due to probability lesser than threshold")
                print(alert_log)
                return 0
    alert_record = alertlog.AlertRecord(client_uuid, None, sink_node, 1)  # source_node=None in case its an initial node
    alert_log.add_alert_record(alert_record)
    print("alert due to missing node")
    print(alert_log)
    return 0


def check_automata_with_source_sink(windowsize, source_node, sink_node, client_uuid):
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
    autos, status = set_globalvar.get_autos()
    alert_log = alertlog.AlertLog(client_uuid, windowsize)
    for connection in autos[windowsize].connections:
        if connection.source_node == source_node and connection.sink_node == sink_node:
            if connection.probability >= THRESHOLD:
                return 1
            else:
                alert_record = alertlog.AlertRecord(client_uuid, None, sink_node, 1)  # source_node=None in case its an initial node
                alert_log.add_alert_record(alert_record)
                print(alert_log)
                print("alert due to probability lesser than threshold")
                return 0
    alert_record = alertlog.AlertRecord(client_uuid, None, sink_node, 1)  # source_node=None in case its an initial node
    alert_log.add_alert_record(alert_record)
    print("alert due to missing node")
    print(alert_log)
    return 0

    # TODO:  AlertLog doesnt need window size and uuid it already there in alert_record then why required to initialize with them
    # TODO:  alertlog needs to be inserted into table after finishing all threads
    # TODO:  when to insert in to User table and change status? Initial with first incoming event the status must be set to 'in-progress'
    # TODO: Once server busy message is received at client side then processing must be stopped and next events must not be thrown to server. If this is not handled the server takes the incomplete data and fires alert