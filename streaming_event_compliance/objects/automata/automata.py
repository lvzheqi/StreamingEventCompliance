from streaming_event_compliance.database import db
# TODO: needs to consider, whether the attribute is private


class Automata:
    def __init__(self):
        self._nodes = {}
        self._connections = {}

    def update_node(self, node, count):
        if node == 'NONE':
            return
        if node in self._nodes:
            self._nodes[node] += count
        else:
            self._nodes[node] = count

    def add_connection_from_database(self, connection):
        '''
        add connection directly from database into the automata
        :param connection: Connection object
        '''
        self._connections[hash(connection)] = connection

    def update_automata(self, connection):
        '''
        add the connection to the automata, try to accumulate the connection,
        if there are some same connections in the memory
        :param connection:
        :return:
        '''
        if self.contains_connection(connection):
            conn = self._connections[hash(connection)]
            conn.count += connection.count
        else:
            self._connections[hash(connection)] = connection
        self.update_node(connection.source_node, connection.count)

    def set_probability(self):
        for conn in self.get_connections():
            if conn.source_node != 'NONE':
                degree = self._nodes[conn.source_node]
                try:
                    conn.probability = conn.count / degree
                except ZeroDivisionError:
                    conn.probability = 0

    def contains_source_node(self, source_node):
        '''
        check, whether the given source_node is in the automata
        :param source_node: string
        :return: boolean
        '''
        return source_node in self._nodes

    def contains_connection(self, connection):
        '''
        check, whether the given connection is in the automata
        :param connection: Connection object
        :return: boolean
        '''
        return hash(connection) in self._connections

    def get_connection_probability(self, connection):
        '''
        return the probability of the given connection; if the connection is not found, return -1
        :param connection: Connection
        :return: probability or -1
        '''
        if self.contains_connection(connection):
            conn = self._connections[hash(connection)]
            return conn.probability
        else:
            return -1

    def get_connections(self):
        return list(self._connections.values())

    def get_sink_nodes(self, source_node):
        if source_node == 'NONE':
            return {}
        sink_nodes = {}
        for conn in self._connections.values():
            if conn.source_node == source_node and conn.probability > 0:
                sink_nodes[conn.sink_node] = conn.probability
        return sink_nodes

    def get_nodes(self):
        return self._nodes

    def __repr__(self):
        return '\nNodes: %s' % self.get_nodes() + \
               '\nConnections: \n %s' % self.get_connections() + '\n'


class Node(db.Model):
    __tablename__ = 'Node'
    node = db.Column('node', db.String(350), primary_key=True)
    degree = db.Column('degree', db.Integer)

    def __init__(self, node, degree):
        self.node = node
        self.degree = degree

    def __repr__(self):
        return "<Node: %s, degree: %s>" % (self.node, self.degree)


class Connection(db.Model):
    __tablename__ = 'Connection'
    # source_node = db.Column('source_node', db.String(10), db.ForeignKey('Node.node'), primary_key=True)
    # sink_node = db.Column('sink_node', db.String(10), db.ForeignKey('Node.node'), primary_key=True)
    source_node = db.Column('source_node', db.String(350), primary_key=True)
    sink_node = db.Column('sink_node', db.String(350), primary_key=True)
    count = db.Column('count', db.Integer)
    probability = db.Column('probability', db.Float)
    # db.ForeignKeyConstraint(
    #     ['source_node', 'sink_node'],
    #     ['Node.node', 'Node.node'], ondelete='CASCADE', onupdate='CASCADE')

    def __init__(self, source_node, sink_node, count=1):
        self.source_node = source_node
        self.sink_node = sink_node
        self.count = count

    def __eq__(self, other):
        return self.source_node == other.source_node and \
                                  self.sink_node == other.sink_node

    def __hash__(self):
        return hash((self.source_node, self.sink_node))

    def __repr__(self):
        return "<Source node: %s, sink node: %s, probability: %s>" % \
               (self.source_node, self.sink_node, self.probability)





