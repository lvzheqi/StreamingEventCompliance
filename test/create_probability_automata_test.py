import unittest
# from streaming_event_compliance.services. import probability_automata
from streaming_event_compliance.services import globalvar, visualization_deviation_automata
from streaming_event_compliance.objects.automata import alertlog


class CreateProbabilityAutomataTest(unittest.TestCase):

    def setUp(self):
        globalvar.init()

        self.uuid = 'u1'
        alog1 = alertlog.AlertLog(self.uuid, 1)
        alog2 = alertlog.AlertLog(self.uuid, 2)
        alog3 = alertlog.AlertLog(self.uuid, 3)
        alog4 = alertlog.AlertLog(self.uuid, 4)
        alog1.update_alert_record(alertlog.AlertRecord(self.uuid, 'a', 'd', 4, 'M'))
        alog1.update_alert_record(alertlog.AlertRecord(self.uuid, 'a', 'f', 2, 'M'))
        alog1.update_alert_record(alertlog.AlertRecord(self.uuid, 'd', 'b', 1, 'M'))
        alog1.update_alert_record(alertlog.AlertRecord(self.uuid, 'a', 'e', 1, 'T'))
        alog2.update_alert_record(alertlog.AlertRecord(self.uuid, 'a,d', 'd,b', 1, 'M'))
        alog2.update_alert_record(alertlog.AlertRecord(self.uuid, 'd,b', 'b,c', 1, 'M'))
        alog3.update_alert_record(alertlog.AlertRecord(self.uuid, 'a,d,b', 'd,b,c', 1, 'M'))
        alog3.update_alert_record(alertlog.AlertRecord(self.uuid, 'd,b,c', 'b,c,d', 1, 'M'))
        alog4.update_alert_record(alertlog.AlertRecord(self.uuid, 'a,d,b,c', 'd,b,c,d', 1, 'M'))
        alogs = {1: alog1, 2: alog2, 3: alog3, 4: alog4}
        self.u_alogs = {'u1': alogs}

    def test_create_automata(self):
        visualization_deviation_automata.visualization_automata(globalvar.autos, self.u_alogs[self.uuid], self.uuid)


if __name__ == '__main__':
    unittest.main()