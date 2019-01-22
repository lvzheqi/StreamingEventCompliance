import unittest
from streaming_event_compliance.services.visualization import visualization_deviation_automata
from streaming_event_compliance.objects.variable.globalvar import gVars
from streaming_event_compliance.objects.automata import alertlog
from streaming_event_compliance.services import setup


class CreateProbabilityAutomataTest(unittest.TestCase):

    def setUp(self):
        setup.init_automata()

        self.uuid = 'client1'
        alog1 = alertlog.AlertLog()
        alog2 = alertlog.AlertLog()
        alog3 = alertlog.AlertLog()
        alog4 = alertlog.AlertLog()
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
        self.u_alogs = {'client1': alogs}

    def test_create_automata(self):
        visualization_deviation_automata.visualization_automata(gVars.autos, self.u_alogs[self.uuid], self.uuid)
        # visualization_deviation_automata.legend()

    # def test_create_legend(self):
    #     src = Source.from_file('Digraph.gv')
    #     src.render()


if __name__ == '__main__':
    unittest.main()
