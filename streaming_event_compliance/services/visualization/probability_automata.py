from graphviz import Digraph
from streaming_event_compliance.utils import config
import shutil

import os

def apply(autos, alert=None):
    '''
    create
    :return:
    '''
    viz = Digraph(name='automata', format='pdf', engine='dot')
    viz.format = 'pdf'
    viz.graph_attr['rankdir'] = 'LR'
    for auto in autos.values():
        with viz.subgraph(name='cluster' + str(auto.window_size)) as sub:
            sub.graph_attr['rankdir'] = 'BT'
            sub.attr(color='black', label='Probability Graph With Prefix Size ' + str(auto.window_size))
            for node in auto.nodes.keys():
                sub.node(node, node)
            for conn in auto.connections:
                sub.edge(conn.source_node, conn.sink_node, label=str(conn.probability),
                         penwidth=str(conn.probability*2))

        # render = viz.render(view=False)
        # with open(render, "rb") as f:
        #     return base64.b64encode(f.read())
    render = viz.render('probability_automata')
    shutil.copyfile(render, config.BASE_DIR + 'test.pdf')
