from streaming_event_compliance.objects.variable.globalvar import gVars
from streaming_event_compliance import app
from streaming_event_compliance.services import setup
from graphviz import Digraph
import os

CLEINT_DATA_PATH = app.config['CLEINT_DATA_PATH']
AUTOMATA_FILE = app.config['AUTOMATA_FILE']
FILE_TYPE = app.config['FILE_TYPE']
WINDOW_SIZE = app.config['WINDOW_SIZE']
THRESHOLD = app.config['THRESHOLD']


def visualization_automata(autos, alogs, uuid):
    viz = Digraph(comment='probability_automata', format='pdf', engine='dot')
    viz.format = 'pdf'
    viz.attr('node', fixedsize='true', width='0.7')
    viz.attr(rankdir='LR')
    for i in range(len(WINDOW_SIZE) - 1, -1, -1):
        auto = autos[WINDOW_SIZE[i]]
        alog = alogs[WINDOW_SIZE[i]]
        with viz.subgraph(name='cluster' + str(WINDOW_SIZE[i])) as sub:
            sub.attr(color='black', label='Probability Graph With Prefix Size ' + str(WINDOW_SIZE[i]))
            for node in auto.get_nodes().keys():
                sub.node(node, node)
            for conn in auto.get_connections():
                if conn.source_node != 'NONE' and conn.count > 0 and conn.probability > THRESHOLD:
                    sub.edge(conn.source_node, conn.sink_node, penwidth='0.5')
                         # label=str(conn.probability), penwidth=str(conn.probability*2))

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

    with viz.subgraph(name='cluster0') as sub:
        # sub.attr(color='black', label='Legend')
        sub = legend()
        # [fixedsize = true, width = 0.75]

    # viz.subgraph(sub)
    viz.render(filename=uuid + '_' + AUTOMATA_FILE, directory=CLEINT_DATA_PATH, view=False, cleanup=False)
    return viz


def legend():
    sub = Digraph()
    # sub.attr(rankdir='LR')
    sub.attr(color='black', label='Legend')
    sub.attr(color='black', label='Legend')
    sub.node('activity', 'activity', fillcolor='red', style='filled')
    sub.node('text0', shape='plaintext', style='solid', label='node, where causes alert\\r',
             penwidth='2', width='3.5')

    sub.node('s_node1', 's_node1')
    sub.node('ss_node1', 'ss_node1')
    sub.edge('s_node1', 'ss_node1', color='black', label='', penwidth='1.5')
    sub.node('text1', shape='plaintext', style='solid', label='connections, when such exists \\r in primal automata \\r',
             penwidth='2', width='3.5')

    sub.node('s_node2', 's_node2', fillcolor='red', style='filled')
    sub.node('ss_node2', 'ss_node2', fillcolor='red', style='filled')
    sub.edge('s_node2', 'ss_node2', color='red', label='', penwidth='1.5')
    sub.node('text2', shape='plaintext', style='solid', label='alerts, when no such connections \\r in primal automata \\r', width='3.5')

    sub.node('s_node3', 's_node3', fillcolor='red', style='filled')
    sub.node('ss_node3', 'ss_node3', fillcolor='red', style='filled')
    sub.edge('s_node3', 'ss_node3', color='green', label='', penwidth='1.5')
    # sub.graph_attr['rank'] = 'source; text0 text1 text2 text3'
    sub.node('text3', shape='plaintext', style='solid', label='alerts, when the probability is \\r below Threshold \\r', width='3.5')

    #
    c1 = Digraph('child1')
    c1.attr(rank='source')
    c1.node('text0')
    c1.node('text1')
    c1.node('text2')
    c1.node('text3')
    sub.subgraph(c1)

    return sub


def show_deviation_pdf(uuid):
    '''
    Returns the file “<client_uuid>_deviations.pdf”  if present in the local.
    Else if no file present with that name then, this function calls the build_deviation_pdf(client_uuid) to create a pdf
    :param client_uuid: user name
    '''
    path = CLEINT_DATA_PATH + uuid + '_' + AUTOMATA_FILE + FILE_TYPE
    if not os.path.exists(path):
        alogs, status = setup.init_client_alert_automata(uuid)
        if status == 1:
            visualization_automata(gVars.autos, alogs, uuid)
        return status
    else:
        return 1
