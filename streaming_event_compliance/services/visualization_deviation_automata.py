from streaming_event_compliance.services import globalvar
from streaming_event_compliance.utils.config import CLEINT_DATA_PATH, AUTOMATA_FILE, FILE_TYPE, WINDOW_SIZE, \
    MAXIMUN_WINDOW_SIZE, THRESHOLD
from graphviz import Digraph
import os


def visualization_automata(autos, alogs, uuid):
    viz = Digraph(comment='probability_automata', format='pdf', engine='dot')
    viz.format = 'pdf'
    viz.graph_attr['rankdir'] = 'LR'
    viz.attr('node', shape='circle', fixedsize='true', width='0.7')

    for i in range(MAXIMUN_WINDOW_SIZE - 1, -1, -1):
        auto = autos[WINDOW_SIZE[i]]
        alog = alogs[WINDOW_SIZE[i]]
        with viz.subgraph(name='cluster' + str(WINDOW_SIZE[i])) as sub:
            sub.attr(color='black', label='Probability Graph With Prefix Size ' + str(WINDOW_SIZE[i]))
            for node in auto.get_nodes().keys():
                sub.node(node, node)
            for conn in auto.get_connections():
                try:
                    if conn.source_node != 'NONE' and conn.count > 0 and conn.probability > THRESHOLD:
                        sub.edge(conn.source_node, conn.sink_node, penwidth='0.5')
                             # label=str(conn.probability), penwidth=str(conn.probability*2))
                except Exception as e:
                    print(e)

            max_count = alog.get_max_count()
            for record in alog.get_alert_log():
                if record.source_node != 'NONE':
                    sub.node(record.source_node, record.source_node, fillcolor='red', style='filled')
                sub.node(record.sink_node, record.sink_node, fillcolor='red', style='filled')
                if record.alert_cause == 'M' and record.source_node != 'NONE':
                    sub.edge(record.source_node, record.sink_node, color='red', label='count = ' + str(record.alert_count),
                             penwidth=str(record.alert_count / max_count * 3))
                elif record.alert_cause == 'T':
                    sub.edge(record.source_node, record.sink_node, color='green', label='count = ' + str(record.alert_count),
                             penwidth=str(record.alert_count / max_count * 3))

    with viz.subgraph(name='cluster00') as sub:
        sub.graph_attr['rankdir'] = 'RL'
        sub.node('text0', shape='plaintext', style='solid', label='node, where causes alert',
                 penwidth='2', width='3.5')
        sub.node('activity', 'activity', fillcolor='red', style='filled')

        sub.node('text1', shape='plaintext', style='solid', label='connections, when such exists\r in primal automata',
                 penwidth='2', width='3.5')
        sub.node('s_node1', 's_node1')
        sub.node('ss_node1', 'ss_node1')
        sub.edge('s_node1', 'ss_node1', color='black', label='', penwidth='1.5')

        sub.node('text2', shape='plaintext', style='solid', label='alerts, when no such connections in primal automata ', width='3.5')
        sub.node('s_node2', 's_node2', fillcolor='red', style='filled')
        sub.node('ss_node2', 'ss_node2', fillcolor='red', style='filled')
        sub.edge('s_node2', 'ss_node2', color='red', label='', penwidth='1.5')

        sub.node('text3', shape='plaintext', style='solid', label='alerts, when the probability is below Threshold ', width='3.5')
        sub.node('s_node3', 's_node3', fillcolor='red', style='filled')
        sub.node('ss_node3', 'ss_node3', fillcolor='red', style='filled')
        sub.edge('s_node3', 'ss_node3', color='green', label='', penwidth='1.5')
        sub.graph_attr['rank'] = 'source; text1; text2; text3'

    viz.render(filename=uuid + '_' + AUTOMATA_FILE, directory=CLEINT_DATA_PATH, view=False, cleanup=True)
    return viz


def build_deviation_pdf(client_uuid):
    '''
    Creates a deviation PDF for the given client_uuid, based on the deviations history
    stored in AlertLog entity in database. This pdf is stored in local as “<client_uuid>_deviations.pdf”.
    :param client_uuid: user name
    '''
    visualization_automata(globalvar.autos, globalvar.get_user_alert_logs(client_uuid), client_uuid)


def show_deviation_pdf(client_uuid):
    '''
    Returns the file “<client_uuid>_deviations.pdf”  if present in the local.
    Else if no file present with that name then, this function calls the build_deviation_pdf(client_uuid) to create a pdf
    :param client_uuid: user name
    '''
    path = CLEINT_DATA_PATH + client_uuid + '_' + AUTOMATA_FILE + FILE_TYPE
    if not os.path.exists(path):
        build_deviation_pdf(client_uuid)



