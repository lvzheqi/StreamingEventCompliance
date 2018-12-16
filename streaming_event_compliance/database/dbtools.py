from streaming_event_compliance.objects.automata import automata
from streaming_event_compliance.objects.automata import alertlog
from streaming_event_compliance.utils.config import WINDOW_SIZE
from streaming_event_compliance.objects.exceptions.exception import NoUserException

from streaming_event_compliance.database import db


def empty_tables():
    db.session.query(automata.Connection).delete()
    db.session.query(automata.Node).delete()
    db.session.query(alertlog.AlertRecord).delete()
    db.session.query(alertlog.User).delete()
    db.session.commit()


def insert_node_and_connection(autos):
    for auto in autos.values():
        for node, degree in auto.nodes.items():
            source_node = automata.Node(node, degree)
            db.session.add(source_node)
        for conn in auto.get_connections():
            db.session.add(conn)
    db.session.commit()


def insert_alert_log(alogs):
    for alog in alogs.values():
        for alert in alog.get_alert_log():
            db.session.add(alert)
    db.session.commit()


def create_user(uuid):
    user = alertlog.User.query.filter_by(user_name=uuid).first()
    if user is None:
        user = alertlog.User(uuid)
        db.session.add(user)
        db.session.commit()


def check_user_status(uuid):
    user = alertlog.User.query.filter_by(user_name=uuid).first()
    if user is not None:
        return user.status
    else:
        raise NoUserException


def update_user_status(uuid, status):
    user = alertlog.User.query.filter_by(user_name=uuid).first()
    if user is not None:
        user.status = status
        db.session.commit()
    else:
        raise NoUserException


def init_automata_from_database():
    '''
    fetch the automata from database. If there is no data in database, then return None
    :return: automata with different window size, otherwise return None
    '''
    conns = automata.Connection.query.all()
    autos = {}
    for ws in WINDOW_SIZE:
        auto = automata.Automata(ws)
        autos[ws] = auto
    if len(conns) != 0:
        for conn in conns:
            ws = conn.source_node.count(",") + 1
            auto = autos[ws]
            auto.add_connection_from_database(conn)
            auto.update_node(conn.source_node, conn.count)
        return autos, 1
    return autos, 0


def init_alert_log_from_database(uuid):
    records = alertlog.AlertRecord.query.filter_by(user_id=uuid).all()
    alogs = {}
    for ws in WINDOW_SIZE:
        alog = alertlog.AlertLog(uuid, ws)
        alogs[ws] = alog
    for record in records:
        ws = record.source_node.count(',') + 1
        alog = alogs[ws]
        alog.add_alert_record_from_database(record)
    return alogs


def delete_alert(uuid):
    records = alertlog.AlertRecord.query.filter_by(user_id=uuid).all()
    for record in records:
        db.session.delete(record)
    db.session.commit()


