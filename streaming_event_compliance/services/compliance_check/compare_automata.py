from streaming_event_compliance.services import globalvar
from streaming_event_compliance.utils.config import THRESHOLD
from streaming_event_compliance.objects.automata import alertlog, automata


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
    alert_log = globalvar.get_alert_logs()[client_uuid][windowsize]
    auto = globalvar.get_autos()[windowsize]
    conn = automata.Connection(sink_node, source_node)
    if not auto.contains_connection(conn):
        if auto.get_connection_probability(conn) >= THRESHOLD:
            return 0
        else:
            alert_log.update_alert_record(alert_log.AlertRecord(client_uuid, source_node, sink_node, 1, 'T'))
            return 1
    elif source_node is None and auto.contains_source_node(sink_node):
        return 0
    else:
        alert_log.update_alert_record(alertlog.AlertRecord(client_uuid, source_node, sink_node, 1, 'M'))
        return 2

#     for connection in autos[windowsize].get_connections():
#         if connection.source_node == source_node and connection.sink_node == sink_node:
#             if connection.probability >= THRESHOLD:
#                 return
#             else:
#                 alert_record = alertlog.AlertRecord(client_uuid, source_node, sink_node, 1, "T")
#                 # Create an alert_log object for windowsize(given) if it is not created previously
#                 if client_uuid not in alert_logs:
#                     alert_logs[client_uuid] = alertlog.AlertLog(client_uuid, windowsize)
#                 alert_logs[client_uuid].update_alert_record(alert_record)
#                 print(alert_logs)
#                 print("alert due to probability lesser than threshold")
#                 return 1
#     alert_record = alertlog.AlertRecord(client_uuid, source_node, sink_node, 1, "M")
#     # Create an alert_log object for windowsize(given) if it is not created previously
#     if client_uuid not in alert_logs:
#         alert_logs[client_uuid] = alertlog.AlertLog(client_uuid, windowsize)
#     alert_logs[client_uuid].update_alert_record(alert_record)
#     print(alert_logs)
#     print("alert due to missing node")
#     return 0
#
#     # TODO: Once server busy message is received at client side then processing must be stopped and next events must
#     # not be thrown to server. If this is not handled the server takes the incomplete data and fires alert
#     # TODO : Implement the deletion of all logs and other stuffs once processing done for one time for all events
#     # from file
#
# def check_automata_only_sourcenode(windowsize, sink_node, client_uuid):
#     '''
#         This function takes sink_node given and checks if the automata of 'windowsize'  has the
#         source_node matching the sink_node. If yes then checks for its probability, if
#         probability is below the threshold or no match found for sink_node then insert data to
#         Alertlog object and return alert message.
#         The automata is retrieved directly from 'autos' variable rather than db. This autos
#         variable was initialized when automata was built using training set
#         :param windowsize: The length of the automata node.
#         :param sink_node: the combination of event that we want to check the compliance for and
#                the additional events(based on window size)
#         :param client_uuid: user name
#         :return: alert message
#     '''
#     alert_log = globalvar.get_alert_logs()[client_uuid][windowsize]
#     auto = globalvar.get_autos()[windowsize]
#     if not auto.contains_source_node(sink_node):
#         alert_record = alertlog.AlertRecord(client_uuid, None, sink_node, 1, 'M')
#         alert_log.update_alert_record(alert_record)
#
#     # for connection in autos[windowsize].get_connections():
#     #     if connection.source_node == sink_node:
#     #         if connection.probability >= THRESHOLD:
#     #             return 2
#     #         else:
#     #             # Insert source_node as sink_node if the sink_node is an initial node
#     #             alert_record = alertlog.AlertRecord(client_uuid, sink_node, None, 1, "T")
#     #
#     #             # Create an alert_log object for windowsize(given) if it is not created previously
#     #             if client_uuid not in alert_logs:
#     #                 alert_logs[client_uuid] = alertlog.AlertLog(client_uuid, windowsize)
#     #             alert_logs[client_uuid].update_alert_record(alert_record)
#     #             print(alert_logs)
#     #             print("alert due to probability lesser than threshold")
#     #             return 1
#     # Insert source_node as sink_node if the sink_node is an initial node
#     # alert_record = alertlog.AlertRecord(client_uuid, sink_node, None, 1, "M")
#
#     # Create an alert_log object for windowsize(given) if it is not created previously
#     # TODO: create init alertlog
#
#     # if client_uuid not in alert_logs:
#     #     alert_logs[client_uuid] = alertlog.AlertLog(client_uuid, windowsize)
#     # alert_logs[client_uuid].update_alert_record(alert_record)
#     # print(alert_logs)
#     print("alert due to missing node")
#     return 0

