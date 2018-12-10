from graphviz import Digraph
from streaming_event_compliance.utils.config import WINDOW_SIZE, BASE_DIR, MAXIMUN_WINDOW_SIZE, THRESHOLD


def apply(autos, alogs):
    viz = Digraph(comment='probability_automata', format='pdf', engine='dot')
    viz.format = 'pdf'
    viz.graph_attr['rankdir'] = 'LR'
    viz.attr('node', shape='circle', fixedsize='true', width='0.7')

    for i in range(MAXIMUN_WINDOW_SIZE - 1, -1, -1):
        auto = autos[WINDOW_SIZE[i]]
        alog = alogs[WINDOW_SIZE[i]]
        with viz.subgraph(name='cluster' + str(auto.window_size)) as sub:
            sub.attr(color='black', label='Probability Graph With Prefix Size ' + str(auto.window_size))
            for node in auto.nodes.keys():
                sub.node(node, node)
            for conn in auto.connections:
                if conn.count > 0 and conn.probability > THRESHOLD:
                    sub.edge(conn.source_node, conn.sink_node, penwidth='0.5')
                             # label=str(conn.probability), penwidth=str(conn.probability*2))

            max_count = alog.get_max_count()
            for record in alog.alert_log:
                sub.node(record.source_node, record.source_node, fillcolor='red', style='filled')
                sub.node(record.sink_node, record.sink_node, fillcolor='red', style='filled')
                if record.alert_cause == 'M':
                    sub.edge(record.source_node, record.sink_node, color='red', label='count = ' + str(record.alert_count),
                             penwidth=str(record.alert_count / max_count * 3))
                else:
                    sub.edge(record.source_node, record.sink_node, color='green', label='count = ' + str(record.alert_count),
                             penwidth=str(record.alert_count / max_count * 3))

    viz.render(filename='probability_automata', directory=BASE_DIR, view=False, cleanup=True)

    # viz_alogs = Digraph(comment='alert_probability_automata', format='pdf', engine='dot')
    # viz_alogs.format = 'pdf'
    # viz_alogs.graph_attr['rankdir'] = 'LR'
    # viz_alogs.attr('node', shape='circle', fixedsize='true', width='1')
    # for i in range(MAXIMUN_WINDOW_SIZE - 1, -1, -1):




    # return viz

