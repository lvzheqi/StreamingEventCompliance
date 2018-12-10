from streaming_event_compliance.database import db
# TODO: needs to consider, whether the attribute is private
# TODO: change map methods


class Automata:
    def __init__(self, window_size):
        self.window_size = window_size
        self.nodes = {}
        self.connections = []

    def update_node(self, node, count):
        if node in self.nodes:
            self.nodes[node] += count
        else:
            self.nodes[node] = count

    def add_connection_from_database(self, connection):
        '''
        add connection directly from database into the automata
        :param connection: Connection object
        '''
        self.connections.append(connection)

    def update_automata(self, connection):
        '''
        add the connection to the automata, try to accumulate the connection,
        if there are some same connections in the memory
        :param connection:
        :return:
        '''
        if self.contains_connection(connection):
            index = self.connections.index(connection)
            conn = self.connections[index]
            conn.count += connection.count
        else:
            self.connections.append(connection)
        self.update_node(connection.source_node, connection.count)

    def set_probability(self):
        for conn in self.connections:
            degree = self.nodes[conn.source_node]
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
        return source_node in self.nodes

    def contains_connection(self, connection):
        '''
        check, whether the given connection is in the automata
        :param connection: Connection object
        :return: boolean
        '''
        return connection in self.connections

    def get_connection_probability(self, connection):
        '''
        return the probability of the given connection; if the connection is not found, return -1
        :param connection: Connection
        :return: probability or -1
        '''
        if self.contains_connection(connection):
            index = self.connections.index(connection)
            conn = self.connections[index]
            return conn.probability
        else:
            return -1

    def __repr__(self):
        return "Window size :%s" % self.window_size + \
               '\nNodes: %s' % self.nodes + \
               '\nConnections: \n %s' % self.connections + '\n'


class Node(db.Model):
    __tablename__ = 'Node'
    node = db.Column('node', db.String(100), primary_key=True)
    degree = db.Column('degree', db.Integer)

    def __init__(self, node, degree):
        self.node = node
        self.degree = degree

    def __repr__(self):
        return "<Node :%s, degree:%s>" % (self.node, self.degree)


class Connection(db.Model):
    __tablename__ = 'Connection'
    # source_node = db.Column('source_node', db.String(10), db.ForeignKey('Node.node'), primary_key=True)
    # sink_node = db.Column('sink_node', db.String(10), db.ForeignKey('Node.node'), primary_key=True)
    source_node = db.Column('source_node', db.String(100), primary_key=True)
    sink_node = db.Column('sink_node', db.String(100), primary_key=True)
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

    def __repr__(self):
        return "<Source node :%s, sink node:%s, probability: %s>" % \
               (self.source_node, self.sink_node, self.probability)





