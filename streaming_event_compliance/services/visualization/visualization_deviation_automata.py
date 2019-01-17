from streaming_event_compliance.objects.variable.globalvar import gVars
from streaming_event_compliance import app
from streaming_event_compliance.services import setup
from graphviz import Digraph
import os
import sys
from streaming_event_compliance.objects.logging.server_logging import ServerLogging


CLEINT_DATA_PATH = app.config['CLEINT_DATA_PATH']
AUTOMATA_FILE = app.config['AUTOMATA_FILE']
FILE_TYPE = app.config['FILE_TYPE']
WINDOW_SIZE = app.config['WINDOW_SIZE']
THRESHOLD = app.config['THRESHOLD']
CHECKING_TYPE = app.config['CHECKING_TYPE']
ALERT_TYPE = app.config['ALERT_TYPE']


def visualization_automata(autos, alogs, uuid):
    """
    Description:
        This function takes the automata and alertlog information to create a corresponding deviation pdf
        <client_uuid>_automata.pdf and save in p_automata file.

    :param autos: :`dict`={int: class `streaming_event_compliance.object.automata.Automata`}: {window size: the automata
    used to do compliance checking}
    :param alogs: :`dict`={int: class `streaming_event_compliance.object.automata.Alertlog`}: {window size: the alertlog
    used to stored the alert-information}
    :param uuid: :`string` client-id
    """
    func_name = sys._getframe().f_code.co_name
    ServerLogging().log_info(func_name, uuid, "Start to render pdf....")
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
                sub.node(node, node, color='black')
            for conn in auto.get_connections():
                if conn.source_node != 'NONE' and conn.count > 0 and conn.probability > THRESHOLD:
                    sub.edge(conn.source_node, conn.sink_node,  color='black',
                             label=str(round(conn.probability*100, 2))+'%',
                             penwidth=str(conn.probability*2))  # penwidth = '0.5'
            max_count = alog.get_max_count()
            for record in alog.get_alert_log():
                if record.source_node not in auto.get_nodes().keys() and record.source_node != 'NONE':
                    sub.node(record.source_node, record.source_node, fillcolor='red', style='filled')
                elif record.sink_node not in auto.get_nodes().keys():
                    sub.node(record.sink_node, record.sink_node, fillcolor='red', style='filled')
                if record.alert_cause == 'M' and record.source_node != 'NONE':
                    sub.edge(record.source_node, record.sink_node, color='red', label='count = ' + str(record.alert_count),
                             penwidth=str(record.alert_count / max_count * 3))
                elif record.alert_cause == 'T':
                    sub.edge(record.source_node, record.sink_node, color='green', label='count = ' + str(record.alert_count),
                             penwidth=str(record.alert_count / max_count * 3))

    ServerLogging().log_info(func_name, uuid, "Start to render pdf legend....")
    with viz.subgraph(name='cluster0') as sub:
        legend(sub)
    ServerLogging().log_info(func_name, uuid, "Finish rendering pdf")
    viz.render(filename=uuid + '_' + AUTOMATA_FILE, directory=CLEINT_DATA_PATH, view=False, cleanup=True)


def legend(sub):
    # sub.attr(rankdir='TB')
    # sub1 = Digraph('sub1')
    sub.attr(color='black', label='Legend')
    with sub.subgraph(name='cluster_sub1') as sub1:
        sub1.attr(color='white', label='', style='filled')
        sub1.node('activity', 'activity', fillcolor='red', style='filled')
        sub1.node('text0', shape='plaintext', style='solid', label='node, which exists not\\r',
                 penwidth='2', width='3.5')

        sub1.node('s_node1', 's_node1')
        sub1.node('ss_node1', 'ss_node1')
        sub1.edge('s_node1', 'ss_node1', color='black', label='', penwidth='1.5', len='2f')
        sub1.node('text1', shape='plaintext', style='solid', label='connections, when such exists \\r in primal automata \\r',
                 penwidth='2', width='3.5')

        sub1.node('s_node2', 's_node2')
        sub1.node('ss_node2', 'ss_node2')
        sub1.edge('s_node2', 'ss_node2', color='red', label='', penwidth='1.5')
        sub1.node('text2', shape='plaintext', style='solid', label='alerts, when no such connections \\r in primal automata \\r', width='3.5')

        sub1.node('s_node3', 's_node3')
        sub1.node('ss_node3', 'ss_node3')
        sub1.edge('s_node3', 'ss_node3', color='green', label='', penwidth='1.5')
        # sub.graph_attr['rank'] = 'source; text0 text1 text2 text3'
        sub1.node('text3', shape='plaintext', style='solid', label='alerts, when the probability is \\r below Threshold \\r', width='3.5')

        c1 = Digraph('child1')
        c1.attr(rank='source')
        c1.node('text0')
        c1.node('text1')
        c1.node('text2')
        c1.node('text3')

        sub1.subgraph(c1)

    with sub.subgraph(name='cluster_sub2') as sub2:
        sub2.attr(color='white', label='', style='filled')
        sub2.node('text5', shape='plaintext', style='solid', label=str(THRESHOLD), width='3.5')
        sub2.node('text4', shape='plaintext', style='solid', label='The threshold of the alert\\r', width='3.5')

        sub2.node('text7', shape='plaintext', style='solid', label=CHECKING_TYPE, width='3.5')
        sub2.node('text6', shape='plaintext', style='solid', label='The typ of compliance checking\\r', width='3.5')

        sub2.node('text9', shape='plaintext', style='solid', label=ALERT_TYPE, width='3.5')
        sub2.node('text8', shape='plaintext', style='solid', label='The typ of alert\\r', width='3.5')
        c2 = Digraph('child2')
        c2.attr(rank='source')
        c2.node('text4')
        c2.node('text6')
        c2.node('text8')

        sub2.subgraph(c2)


def show_deviation_pdf(uuid):
    """
    Description:
        This function checks if deviation_pdf exists. If the pdf exists, then return 1.
        If not, init alert-information from database and use function `visualization_automata`
        to create pdf. Return 0, if there are no information about this client in database.
        Otherwise, return 1.

    :param uuid: :`string`: client-id

    :return: :int: {0: not created, 1: created successfully}
    """
    func_name = sys._getframe().f_code.co_name
    path = CLEINT_DATA_PATH + uuid + '_' + AUTOMATA_FILE + FILE_TYPE
    ServerLogging().log_info(func_name, uuid, "Check, whether PDF Path exists")
    if not os.path.exists(path):
        ServerLogging().log_info(func_name, uuid, "PDF exists not, init alertlog if not exist")
        alogs, status = setup.init_client_alert_automata(uuid)
        if status == 1:
            ServerLogging().log_info(func_name, uuid, "PDF exists not, create again using alertlog")
            visualization_automata(gVars.autos, alogs, uuid)
            ServerLogging().log_info(func_name, uuid, "PDF is created successfully")
        else:
            ServerLogging().log_info(func_name, uuid, "Alertlog exists not, can't create PDF")
        return status
    else:
        ServerLogging().log_info(func_name, uuid, "PDF exists, don't need to create again")
        return 1
