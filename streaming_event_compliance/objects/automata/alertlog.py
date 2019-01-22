from streaming_event_compliance.database import db


class AlertLog:

    def __init__(self):
        self._alert_log = {}

    def update_alert_record(self, alert_record):
        key = hash(alert_record)
        if key in self._alert_log:
            alert = self._alert_log[key]
            alert.set_alert_count(alert.get_alert_count() + alert_record.get_alert_count())
        else:
            self._alert_log[key] = alert_record

    def add_alert_record_from_database(self, alert_record):
        self._alert_log[hash(alert_record)] = alert_record

    def get_max_count(self):
        count = 0
        for record in self._alert_log.values():
            if record.get_alert_count() > count:
                count = record.get_alert_count()
        return count

    def get_alert_log(self):
        return list(self._alert_log.values())

    def __repr__(self):
        return 'alert logger:\n %s' % self.get_alert_log() + '\n'


class Client(db.Model):
    """
    Description:
        This class describes the attributes of the Client(corresponding the column of the table 'Client' in database).

    Class Variables:
    client_name: :`string` the client_id.
    status: :`boolean`
    """
    __tablename__ = 'Client'
    client_name = db.Column('client_name', db.String(350), primary_key=True, unique=True)
    status = db.Column('status', db.Boolean)

    def __init__(self, client_name, status=False):
        self.client_name = client_name
        self.status = status


class AlertRecord(db.Model):
    """
    Description:
        This class describes the attributes of the AlertRecord(corresponding the column of the table 'AlertRecord'
        in database).

    Class Variables:
    client_id: :`string` the client_id.
    source_node: :`string` the source_node name.
    sink_node: :`string` the sink_node name.
    alert_cause: :`string` alert type {T, M}.
    alert_count: :`float` the number of occurrences of the alert.
    """
    __tablename__ = 'AlertRecord'
    client_id = db.Column('client_id', db.String(250), db.ForeignKey('Client.client_name'),
                        primary_key=True)
    source_node = db.Column('source_node', db.String(250), primary_key=True)
    sink_node = db.Column('sink_node', db.String(250), primary_key=True)
    alert_cause = db.Column('alert_cause', db.String(1))
    alert_count = db.Column('alert_count', db.Float)

    def __init__(self, client_id, source_node, sink_node, alert_count=1, alert_cause='M'):
        self.client_id = client_id
        self.source_node = source_node
        self.sink_node = sink_node
        self.l_client_id = client_id
        self.l_source_node = source_node
        self.l_sink_node = sink_node
        self.l_alert_count = alert_count
        self.l_alert_cause = alert_cause

    def is_equal(self, other):
        return self.l_client_id == other.l_client_id and \
               self.l_source_node == other.l_source_node and \
               self.l_sink_node == other.l_sink_node

    def __hash__(self):
        return hash((self.l_client_id, self.l_source_node, self.l_sink_node))

    def __repr__(self):
        return "<Source node: %s, sink node: %s, alert_cause: %s, alert_count: %s>" \
               % (self.l_source_node, self.l_sink_node, self.l_alert_cause, self.l_alert_count)

    def get_client_id(self):
        return self.l_client_id

    def get_source_node(self):
        return self.l_source_node

    def get_sink_node(self):
        return self.l_sink_node

    def get_alert_cause(self):
        return self.l_alert_cause

    def get_alert_count(self):
        return self.l_alert_count

    def set_alert_count(self, alert_count):
        self.l_alert_count = alert_count

    def set_alert_cause(self, alert_cause):
        self.l_alert_cause = alert_cause
