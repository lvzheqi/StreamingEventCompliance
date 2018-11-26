from streaming_event_compliance.objects.automata import automata, alertlog


def test_automata():
    auto1 = automata.Automata(1)
    auto2 = automata.Automata(2)
    auto3 = automata.Automata(3)
    auto4 = automata.Automata(4)
    auto1.update_automata(automata.Connection('A', 'B', 1))
    auto1.update_automata(automata.Connection('A', 'B', 1))
    auto1.update_automata(automata.Connection('A', 'C', 1))
    auto2.update_automata(automata.Connection('AB', 'BC', 1))
    auto2.update_automata(automata.Connection('BD', 'DB', 1))
    auto3.update_automata(automata.Connection('ASA', 'FVB', 1))
    auto3.update_automata(automata.Connection('ADF', 'DFB', 1))
    auto3.update_automata(automata.Connection('ASA', 'BDS', 1))
    auto4.update_automata(automata.Connection('ARTG', 'BKKL', 1))
    auto1.set_probability()
    auto2.set_probability()
    auto3.set_probability()
    auto4.set_probability()
    autos = {1: auto1, 2: auto2, 3: auto3, 4: auto4}
    return autos


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
