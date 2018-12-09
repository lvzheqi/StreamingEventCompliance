import unittest
from streaming_event_compliance.database import dbtools
from streaming_event_compliance.objects.automata import automata, alertlog


class DBToolsTest(unittest.TestCase):
    def setUp(self):
        dbtools.empty_tables()

    def create_automata(self):
        auto1 = automata.Automata(1)
        auto2 = automata.Automata(2)
        auto3 = automata.Automata(3)
        auto4 = automata.Automata(4)
        auto1.update_automata(automata.Connection('A', 'B,', 1))
        auto1.update_automata(automata.Connection('A', 'B,', 1))
        auto1.update_automata(automata.Connection('A', 'C', 1))
        auto2.update_automata(automata.Connection('A,B', 'B,C', 1))
        auto2.update_automata(automata.Connection('B,D', 'D,B', 1))
        auto3.update_automata(automata.Connection('A,D,D', 'C,D,D', 1))
        auto4.update_automata(automata.Connection('A,B,A,W', 'B,C,S,S', 1))
        auto1.set_probability()
        auto2.set_probability()
        auto3.set_probability()
        auto4.set_probability()
        return {1: auto1, 2: auto2, 3: auto3, 4: auto4}

    def test_node_and_connection(self):
        autos = self.create_automata()
        dbtools.insert_node_and_connection(autos)
        autos2, status = dbtools.init_automata_from_database()
        self.assertEqual(status, 1)
        self.assertEqual(repr(autos), repr(autos2))

    def test_user(self):
        dbtools.create_user('1')
        dbtools.create_user('2')
        dbtools.update_user_status('1', True)
        dbtools.update_user_status('2', False)
        self.assertEqual(dbtools.check_user_status('1'), True)
        self.assertEqual(dbtools.check_user_status('2'), False)

    def test_alert_log(self):
        uuid = '1'
        dbtools.create_user('1')
        alog1 = alertlog.AlertLog(uuid, 1)
        alog2 = alertlog.AlertLog(uuid, 2)
        alog3 = alertlog.AlertLog(uuid, 3)
        alog4 = alertlog.AlertLog(uuid, 4)
        alog1.update_alert_record(alertlog.AlertRecord(uuid, 'A', 'B', 1))
        alog1.update_alert_record(alertlog.AlertRecord(uuid, 'A', 'B', 1))
        alog1.update_alert_record(alertlog.AlertRecord(uuid, 'B', 'B', 1))
        alog2.update_alert_record(alertlog.AlertRecord(uuid, 'A,C', 'B,D', 1))
        alog2.update_alert_record(alertlog.AlertRecord(uuid, 'A,C', 'B,R', 1))
        alog2.update_alert_record(alertlog.AlertRecord(uuid, 'A,W', 'B,W', 1))
        alog3.update_alert_record(alertlog.AlertRecord(uuid, 'A,A,W', 'B,S,S', 1))
        alog4.update_alert_record(alertlog.AlertRecord(uuid, 'A,L,K,K', 'B,S,S,D', 1))
        alogs = {1: alog1, 2: alog2, 3: alog3, 4: alog4}
        dbtools.insert_alert_log(alogs)
        alogs2 = dbtools.init_alert_log_from_database(uuid)
        self.assertEqual(repr(alogs), repr(alogs2))


if __name__ == '__main__':
    unittest.main()
