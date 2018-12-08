import unittest
from streaming_event_compliance.objects.automata import alertlog


class AlertlogTest(unittest.TestCase):

    def setUp(self):
        self.uuid = 'u1'
        self.alog1 = alertlog.AlertLog(self.uuid, 1)
        self.alog2 = alertlog.AlertLog(self.uuid, 2)
        self.alog1.update_alert_record(alertlog.AlertRecord(self.uuid, 'A', 'B', 1))
        self.alog1.update_alert_record(alertlog.AlertRecord(self.uuid, 'B', 'C', 1))
        self.alog2.update_alert_record(alertlog.AlertRecord(self.uuid, 'A,C', 'B,D', 1))
        self.alog2.update_alert_record(alertlog.AlertRecord(self.uuid, 'A,C', 'B,D', 1))
        self.alog2.update_alert_record(alertlog.AlertRecord(self.uuid, 'A,C', 'B,W', 1))

    def test_alertlog(self):
        for alog in self.alog1.alert_log:
            if alog.sink_node is 'B':
                self.assertAlmostEqual(alog.alert_count, 1)
            elif alog.sink_node is 'C':
                self.assertAlmostEqual(alog.alert_count, 1)
            elif alog.sink_node is '$':
                self.assertAlmostEqual(alog.alert_count, 0)
        for alog in self.alog2.alert_log:
            if alog.sink_node is 'B,D':
                self.assertAlmostEqual(alog.alert_count, 2)
            elif alog.sink_node is 'B,W':
                self.assertAlmostEqual(alog.alert_count, 1)


if __name__ == '__main__':
    unittest.main()
