from objects.automata import alertLog, automata
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def init():

    from objects.automata.alertLog import db as alter_log_db
    # alter_log_db.drop_all()
    # alter_log_db.session.commit()
    alter_log_db.create_all()
    alter_log_db.session.commit()
    from objects.automata.automata import db as automata_db
    # # alter_log_db.drop_all()
    #
    # db.session.query(alertLog.AlertLog).delete()
    # db.session.query(alertLog.User).delete()
    # db.session.query(automata.Node).delete()
    # db.session.query(automata.Automata).delete()
    # automata_db.session.commit()

    automata_db.create_all()
    automata_db.session.commit()

    # empty table
    # db.session.query(alertLog.AlertLog).delete()
    # db.session.query(alertLog.User).delete()
    # db.session.query(automata.SourceNode).delete()
    # db.session.commit()
    #
    test_automata_create()
    test_user_create()
    test_alert_log_create()


def test_automata_create():
    source_node = automata.Node('EF')
    sink_node = automata.Node('SV')
    db.session.add(source_node)
    db.session.add(sink_node)
    db.session.commit()

    event = automata.Automata('EF', 'SV')
    db.session.add(event)
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
