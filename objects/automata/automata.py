from typing import Any
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Automata:
    # TODO: write the function to create automata
    # TODO: instantiate the sourceNode and sinkNode
    def __init__(self, ):
        return


class SourceNode(db.Model):
    __tablename__ = 'SourceNode'
    window_size = db.Column('window_size', db.Integer, primary_key=True)
    source_node = db.Column('source_node', db.String(10), primary_key=True)
    degree = db.Column('degree', db.Integer)
    sink_node = db.relationship('SinkNode', primaryjoin='or_(SourceNode.window_size==SinkNode.window_size, '
                                                        'SourceNode.source_node==SinkNode.source_node )',
                                backref='sourceNode', lazy='dynamic')

    def __init__(self, window_size, source_node):
        self.window_size = window_size
        self.source_node = source_node

    def __setattr__(self, name: str, value: Any) -> None:
            super().__setattr__(name, value)

    def __getattribute__(self, name: str) -> Any:
            return super().__getattribute__(name)


class SinkNode(db.Model):
    __tablename__ = 'SinkNode'
    window_size = db.Column('window_size', db.Integer, db.ForeignKey('SourceNode.window_size'), primary_key=True)
    source_node = db.Column('source_node', db.String(10), db.ForeignKey('SourceNode.source_node'), primary_key=True)
    sink_node = db.Column('sink_node', db.String(10), primary_key=True)
    connection = db.Column('connection', db.Integer)
    probability = db.Column('probability', db.Float)

    def __init__(self, window_size, source_node, sink_node):
        self.window_size = window_size
        self.source_node = source_node
        self.sink_node = sink_node

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)

    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name)



