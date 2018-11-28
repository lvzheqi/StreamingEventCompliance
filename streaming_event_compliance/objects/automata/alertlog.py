from streaming_event_compliance import db


class AlertLog:

    def __init__(self, uuid, window_size, auto):
        self.window_size = window_size
        self.uuid = uuid
        self.auto = auto
        self.alert_log = []

    def add_alert_record(self, alert_record):
        if alert_record in self.alert_log:
            index = self.alert_log.index(alert_record)
            alert = self.alert_log[index]
            alert.alert_count += 1
        else:
            self.alert_log.append(alert_record)

    def __repr__(self):
        return 'User name: %s' % self.uuid + '\n' + \
               'Window size: %s' % self.window_size + '\n' + \
               'alert logger:\n %s' % self.alert_log + '\n'


class User(db.Model):
    __tablename__ = 'User'

    user_name = db.Column('user_name', db.String(20), primary_key=True, unique=True)
    status = db.Column('status', db.Boolean)

    def __init__(self, user_name):
        self.user_name = user_name

    def __eq__(self, other):
        return self.user_name == other.user_name


class AlertRecord(db.Model):
    __tablename__ = 'AlertRecord'

    user_id = db.Column('user_id', db.String(20), db.ForeignKey('User.user_name'),
                        primary_key=True)
    source_node = db.Column('source_node', db.String(10), primary_key=True)
    sink_node = db.Column('sink_node', db.String(10), primary_key=True)
    alert_cause = db.Column('alert_cause', db.String(1))
    alert_count = db.Column('alert_count', db.Float)

    def __init__(self, user_id, source_node, sink_node, alert_count):
        self.user_id = user_id
        self.source_node = source_node
        self.sink_node = sink_node
        self.alert_count = alert_count

    def __eq__(self, other):
        return self.user_id == other.user_id and \
               self.source_node == other.source_node and \
               self.sink_node == other.sink_node

    def __repr__(self):
        return "<Source node: %s, sink node: %s, alert_cause: %s, alert_count: %s>" \
               % (self.source_node, self.sink_node, self.alert_cause, self.alert_count)

