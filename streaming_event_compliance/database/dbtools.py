from streaming_event_compliance.objects.automata import automata
from streaming_event_compliance.objects.automata import alertlog
from streaming_event_compliance import app

from streaming_event_compliance.database import db

WINDOW_SIZE = app.config['WINDOW_SIZE']


def empty_tables():
    db.session.query(automata.Connection).delete()
    db.session.query(automata.Node).delete()
    db.session.query(alertlog.AlertRecord).delete()
    db.session.query(alertlog.Client).delete()
    db.session.commit()


def insert_node_and_connection(autos):
    for auto in autos.values():
        for node, degree in auto.get_nodes().items():
            source_node = automata.Node(node, degree)
            db.session.add(source_node)
        for conn in auto.get_connections():
            pass
            db.session.add(automata.Connection(conn.source_node, conn.sink_node, conn.count, conn.probability))
            # db.session.add(conn)
    db.session.commit()


def insert_alert_log(alogs):
    for alog in alogs.values():
        for alert in alog.get_alert_log():
            db.session.add(alertlog.AlertRecord(alert.client_id, alert.source_node, alert.sink_node, alert.alert_count, alert.alert_cause))
            # db.session.add(alert)
    db.session.commit()


def create_client(uuid):
    client = alertlog.Client.query.filter_by(client_name=uuid).first()
    if client is None:
        client = alertlog.Client(uuid)
        db.session.add(client)
        db.session.commit()


def check_client_status(uuid):
    client = alertlog.Client.query.filter_by(client_name=uuid).first()
    db.session.commit()
    if client is not None:
        return client.status
    else:
        return None


def update_client_status(uuid, status):
    client = alertlog.Client.query.filter_by(client_name=uuid).first()
    db.session.commit()
    if client is not None:
        client.status = status

    else:
        client = alertlog.Client(uuid, status)
        db.session.add(client)
    db.session.commit()


def init_automata_from_database():
    conns = automata.Connection.query.all()
    db.session.commit()
    autos = {}
    for ws in WINDOW_SIZE:
        auto = automata.Automata()
        autos[ws] = auto
    if len(conns) != 0:
        for conn in conns:
            ws1 = conn.source_node.count(',') + 1
            ws2 = conn.sink_node.count(',') + 1
            auto = autos[max(ws1, ws2)]
            auto.add_connection_from_database(automata.ConnectionL(conn.source_node, conn.sink_node,
                                                                   conn.count, conn.probability))
            # auto.add_connection_from_database(conn)
            auto.update_node(conn.source_node, conn.count)
        return autos, 1
    return autos, 0


def init_alert_log_from_database(uuid):
    records = alertlog.AlertRecord.query.filter_by(client_id=uuid).all()
    db.session.commit()
    alogs = {}
    for ws in WINDOW_SIZE:
        alog = alertlog.AlertLog()
        alogs[ws] = alog
    if len(records) != 0:
        for record in records:
            ws1 = record.source_node.count(',') + 1
            ws2 = record.sink_node.count(',') + 1
            alog = alogs[max(ws1, ws2)]
            alog.add_alert_record_from_database(alertlog.AlertRecordL(record.sink_node, record.source_node,
                                                                      record.alert_count, record.alert_cause))
            # alog.add_alert_record_from_database(record)
        return alogs, 1
    return alogs, 0


def delete_alert(uuid):
    records = alertlog.AlertRecord.query.filter_by(client_id=uuid).all()
    for record in records:
        db.session.delete(record)
    db.session.commit()
