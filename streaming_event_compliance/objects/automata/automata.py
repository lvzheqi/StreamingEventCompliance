from streaming_event_compliance.database import db


class Automata:
    """
    Description:
        This class describes the basic elements of an automata.

    Private Instance Variables:
    _node: :`dict`={`string`: int}: {nodename: the number of this nodes appear}.
    _connections: :`dict`={`string`: class `streaming_event_compliance.object.automata.automata.Connection`}:
                    {hash value: one connection object}.
    _total_number: :int: the number of cases, calculated by taking count of node named 'None'
                    (using 'None' to indicate the beginning of one case in our setting).
    """
    def __init__(self):
        self._nodes = {}
        self._connections = {}
        self._total_number = 0

    def update_node(self, node, count):
        """
        Description:
            This function is for adding node into automata, and taking count of it.

        :param node: :`string` The node name.
        :param count: :int the number of occurrences of a node
        """
        if node == 'NONE':
            self._total_number += 1
            return
        if node in self._nodes:
            self._nodes[node] += count
        else:
            self._nodes[node] = count

    def add_connection_from_database(self, connection):
        """
        Description:
            Adding connection directly from database into the automata.

        :param connection: :class `streaming_event_compliance.object.automata.automata.Connection` connection object.
        """
        self._connections[hash(connection)] = connection

    def update_automata(self, connection):
        """
        Description:
            Adding the connection to the automata, try to accumulate the connection, if there are some same connections
            in the memory.

        :param connection: :class `streaming_event_compliance.object.automata.automata.Connection` connection object.
        """
        if self.contains_connection(connection):
            conn = self._connections[hash(connection)]
            conn.count += connection.count
        else:
            self._connections[hash(connection)] = connection
        self.update_node(connection.source_node, connection.count)

    def set_probability(self):
        """
        Description:
            This function is for computing the probabilities of each connection.
        """
        for conn in self.get_connections():
            if conn.source_node == 'NONE':
                conn.probability = conn.count / self._total_number
            else:
                degree = self._nodes[conn.source_node]
                if degree == 0:
                    conn.probability = 0
                else:
                    conn.probability = conn.count / degree

    def contains_source_node(self, source_node):
        """
        Description:
            Check, whether the given source_node is in the automata.

        :param source_node: :`string`
        :return: boolean
        """
        return source_node in self._nodes

    def contains_connection(self, connection):
        """
        Description:
            Checking, whether the given connection is in the automata.

        :param connection: :class `streaming_event_compliance.object.automata.automata.Connection` connection object.
        :return: boolean
        """
        return hash(connection) in self._connections

    def get_connection_probability(self, connection):
        """
        Description:
            Return the probability of the given connection; If the connection is not found, return -1.

        :param connection: :class `streaming_event_compliance.object.automata.automata.Connection` connection object.
        :return: probability or -1
        """
        if self.contains_connection(connection):
            conn = self._connections[hash(connection)]
            return conn.probability
        else:
            return -1

    def get_sink_nodes(self, source_node):
        """
        Description:
            This function will give all the successors(sink_nodes) of the given source_node along with
            their probabilities.

        :param source_node: :`string`
        :return: sink_nodes: :`dict`={`string`: `float`}: {sink_node name: the probability of this connection
        (from source_node to this particular sink_bode)}
        """
        sink_nodes = {}
        for conn in self.get_connections():
            if conn.source_node == source_node and conn.probability > 0:
                sink_nodes[conn.sink_node] = conn.probability
        return sink_nodes

    def get_connections(self):
        """
        Description:
            This function gives a list of the hash values of all connections.

        :return: :`list`
        """
        return list(self._connections.values())

    def get_nodes(self):
        return self._nodes

    def __repr__(self):
        return '\nNodes: %s' % self.get_nodes() + \
               '\nConnections: \n %s' % self.get_connections() + '\n'

#
# class ConnectionL:
#
#     def __init__(self, source_node, sink_node, count=1, probability=0):
#         self.source_node = source_node
#         self.sink_node = sink_node
#         self.count = count
#         self.probability = probability
#
#     def __eq__(self, other):
#         return self.source_node == other.source_node and \
#                                   self.sink_node == other.sink_node
#
#     def __hash__(self):
#         return hash((self.source_node, self.sink_node))
#
#     def __repr__(self):
#         return "<Source node: %s, sink node: %s, probability: %s>" % \
#                (self.source_node, self.sink_node, self.probability)


class Node(db.Model):
    """
    Description:
        This class describes the attributes of the Node(corresponding the column of the table 'Node' in database).

    Class Variables:
    node: :`string` node name.
    degree: :`integer` the outdegree of the node.
    """
    __tablename__ = 'Node'
    node = db.Column('node', db.String(350), primary_key=True)
    degree = db.Column('degree', db.Integer)

    def __init__(self, node, degree):
        self.node = node
        self.degree = degree


class Connection(db.Model):
    """
    Description:
        This class describes the attributes of the Connection(corresponding the column of the table 'Connection' in database).

    Class Variables:
    source_node: :`string` the source_node name.
    sink_node: :`string` the sink_node name.
    count: :`integer` the number of occurrences of the connection.
    probability: :`float` the probability of the connection.
    """
    __tablename__ = 'Connection'
    source_node = db.Column('source_node', db.String(350), primary_key=True)
    sink_node = db.Column('sink_node', db.String(350), primary_key=True)
    count = db.Column('count', db.Integer)
    probability = db.Column('probability', db.Float)

    def __init__(self, source_node, sink_node, count=1, probability=0):
        self.source_node = source_node
        self.sink_node = sink_node
        self.count = count
        self.probability = probability
