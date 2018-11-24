from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'User'
    user_name = db.Column('user_name', db.String(20), primary_key=True, unique=True)
    status = db.Column('status', db.Boolean)

    def __init__(self, user_name):
        self.user_name = user_name


class AlertLog(db.Model):
    __tablename__ = 'AlertLog'

    user_id = db.Column('user_id', db.String(20), db.ForeignKey('User.user_name'),
                        primary_key=True)
    window_size = db.Column('window_size', db.Integer, primary_key=True)
    source_node = db.Column('source_node', db.String(10), primary_key=True)
    sink_node = db.Column('sink_node', db.String(10), primary_key=True)
    alert_cause = db.Column('alert_cause', db.String(1))
    alert_count = db.Column('alert_count', db.Float)

    def __init__(self, user_id, window_size, source_node, sink_node):
        self.user_id = user_id
        self.window_size = window_size
        self.source_node = source_node
        self.sink_node = sink_node
