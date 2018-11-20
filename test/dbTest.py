from objects.automata import automata, alertLog
from flask_sqlalchemy import SQLAlchemy
from utils import defaultConfig
# from sqlalchemy import *

db = SQLAlchemy()


def init():
    # engine = create_engine(defaultConfig.DATABASE_PATH)
    # metadata = MetaData()
    db.session.query(alertLog.AlertLog).delete()
    db.session.query(alertLog.User).delete()
    db.session.query(automata.SourceNode).delete()
    db.session.commit()
    test_source_node_create()
    test_user_create()
    test_alert_log_create()


def test_source_node_create():
    source1 = automata.SourceNode(2, 'EF')
    source2 = automata.SourceNode(3, 'EFG')
    db.session.add(source1)
    db.session.add(source2)
    db.session.commit()


def test_user_create():
    user1 = alertLog.User('1')
    user2 = alertLog.User('2')
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()


def test_alert_log_create():
    alert1 = alertLog.AlertLog('1', 2, 'EF', 'AB')
    db.session.add(alert1)
    db.session.commit()
