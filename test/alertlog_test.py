import unittest
from streaming_event_compliance.objects.automata import alertlog


class AlertlogTest(unittest.TestCase):

    def test_alertlog(uuid, autos):
        alog1 = alertlog.AlertLog(uuid, 1, autos[1])
        alog2 = alertlog.AlertLog(uuid, 2, autos[2])
        alog3 = alertlog.AlertLog(uuid, 3, autos[3])
        alog4 = alertlog.AlertLog(uuid, 4, autos[4])
        alog1.add_alert_record(alertlog.AlertRecord(uuid, 'A', 'B', 1))
        alog1.add_alert_record(alertlog.AlertRecord(uuid, 'B', 'B', 1))
        alog2.add_alert_record(alertlog.AlertRecord(uuid, 'AC', 'BD', 1))
        alog2.add_alert_record(alertlog.AlertRecord(uuid, 'AC', 'BR', 1))
        alog2.add_alert_record(alertlog.AlertRecord(uuid, 'AW', 'BW', 1))
        alog3.add_alert_record(alertlog.AlertRecord(uuid, 'ADS', 'BWQ', 1))
        alog3.add_alert_record(alertlog.AlertRecord(uuid, 'AAW', 'BSS', 1))
        alog4.add_alert_record(alertlog.AlertRecord(uuid, 'ALKK', 'BSSD', 1))
        alog4.add_alert_record(alertlog.AlertRecord(uuid, 'ADDS', 'SDWB', 1))
        alogs = {1: alog1, 2: alog2, 3: alog3, 4: alog4}
        return alogs


if __name__ == '__main__':
    unittest.main()
