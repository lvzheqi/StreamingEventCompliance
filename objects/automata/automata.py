from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Node(db.Model):
    __tablename__ = 'Node'
    node = db.Column('node', db.String(10), primary_key=True)
    degree = db.Column('degree', db.Integer)

    def __init__(self, node):
        self.node = node


class Automata(db.Model):
    __tablename__ = 'Automata'
    source_node = db.Column('source_node', db.String(10), db.ForeignKey('Node.node'), primary_key=True)
    sink_node = db.Column('sink_node', db.String(10), db.ForeignKey('Node.node'), primary_key=True)
    connection = db.Column('connection', db.Integer)
    probability = db.Column('probability', db.Float)
    db.ForeignKeyConstraint(
        ['source_node', 'sink_node'],
        ['Node.node', 'Node.node'], ondelete='CASCADE', onupdate='CASCADE')

    def __init__(self, source_node, sink_node):
        self.source_node = source_node
        self.sink_node = sink_node

    # TODO: write the function to create automata
    # TODO: instantiate the sourceNode and sinkNode





