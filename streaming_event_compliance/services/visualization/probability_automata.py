from graphviz import Digraph
from streaming_event_compliance.utils.config import WINDOWS, BASE_DIR, MAXIMUN_WINDOW_SIZE


def apply(autos):
    viz = Digraph(comment='probability_automata', format='pdf', engine='dot')
    viz.format = 'pdf'
    viz.graph_attr['rankdir'] = 'LR'
    viz.attr('node', shape='circle', fixedsize='true', width='1')

    for i in range(MAXIMUN_WINDOW_SIZE - 1, -1, -1):
        auto = autos[WINDOWS[i]]
        with viz.subgraph(name='cluster' + str(auto.window_size)) as sub:
            sub.attr(color='black', label='Probability Graph With Prefix Size ' + str(auto.window_size))
            for node in auto.nodes.keys():
                sub.node(node, node)
            for conn in auto.connections:
                sub.edge(conn.source_node, conn.sink_node, label=str(conn.probability),
                         penwidth=str(conn.probability*2))
    viz.render(filename='probability_automata', directory=BASE_DIR, view=False, cleanup=True)

    # return viz

