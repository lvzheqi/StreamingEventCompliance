from streaming_event_compliance.objects.automata import alert_log, automata
from flask_sqlalchemy import SQLAlchemy



class DatabaseTest:

    db = SQLAlchemy()

    def init(self):

        from streaming_event_compliance.objects.automata.alert_log import db as alter_log_db
        # alter_log_db.drop_all()
        # alter_log_db.session.commit()
        alter_log_db.create_all()
        alter_log_db.session.commit()
        from streaming_event_compliance.objects.automata.automata import db as automata_db
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
        self.test_automata_create()
        self.test_user_create()
        self.test_alert_log_create()


    def test_automata_create(self):
        source_node = automata.Node('EF')
        sink_node = automata.Node('SV')
        self.db.session.add(source_node)
        self.db.session.add(sink_node)
        self.db.session.commit()

        event = automata.Automata('EF', 'SV')
        self.db.session.add(event)
        self.db.session.commit()


    def test_user_create(self):
        user1 = alert_log.User('1')
        user2 = alert_log.User('2')
        self.db.session.add(user1)
        self.db.session.add(user2)
        self.db.session.commit()


    def test_alert_log_create(self):
        alert1 = alert_log.AlertLog('1', 2, 'EF', 'AB')
        self.db.session.add(alert1)
        self.db.session.commit()


