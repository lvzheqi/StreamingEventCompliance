import unittest
from streaming_event_compliance.utils import config
from streaming_event_compliance.services.build_automata import build_automata
from streaming_event_compliance.services.build_automata import case_thread
from streaming_event_compliance.database import dbtools
from streaming_event_compliance.services import globalvar, set_globalvar
from pm4py.objects.log.importer.xes import factory as xes_importer
from pm4py.objects.log import transform
from streaming_event_compliance.objects.automata import automata


class BuildingAutomataTestCase(unittest.TestCase):
    """
    Test function build_automata() in streaming_event_compliance/services/build_automata.py
    3.Store the processing sequence of events of each case
    4.Compare these sequence with EventLog2 to see if all the events are processed in sequential
    """

    def setUp(self):
        '''do something before every test method'''
        dbtools.empty_tables()
        # init automata
        globalvar.init()

    def test_multi_threading_for_building_automata(self):
        '''
        This test should pass, but because the bulid_automata() execuated twice
        the expected_log and check_executing_order are not same
        :return:
        '''
        # read file
        trace_log = xes_importer.import_log(config.TRAINING_EVENT_LOG_PATH)
        event_log = transform.transform_trace_log_to_event_log(trace_log)
        event_log.sort()
        expected_log = {}
        for one_event in event_log:
            event = {}
            for item in one_event.keys():
                if item == 'concept:name':
                    event['activity'] = one_event.get(item)
                elif item == 'case:concept:name':
                    event['case_id'] = one_event.get(item)
            if expected_log.get(event['case_id']):
                expected_log.get(event['case_id']).append(event['activity'])
            else:
                expected_log[event['case_id']] = []
                expected_log[event['case_id']].append(event['activity'])
        build_automata.build_automata()
        print("expected_order:")
        for item in expected_log:
            print(item, ":", expected_log.get(item))
        print("check_executing_order:")
        for item in case_thread.check_executing_order:
            print(item, ":", case_thread.check_executing_order.get(item))
        self.assertEqual(expected_log, case_thread.check_executing_order)

    def test_calcuate_connection_for_different_prefix_automata(self):
        windowsMemory = ['a', 'b', 'c', 'd', 'e']
        autos_manuals = {}
        autos_manual1 = automata.Automata(1)
        autos_manual1.windowsize = 1
        autos_manual1.nodes = {'d': 1}
        autos_manual1.connections.append({'Source node': ' d', 'sink node': 'e', 'probability': None})
        autos_manuals[1] = autos_manual1
        autos_manual2 = automata.Automata(2)
        autos_manual2.windowsize = 2
        autos_manual2.nodes = {'c,d': 1}
        autos_manual2.connections.append({'Source node': ' c,d', 'sink node': 'd,e', 'probability': None})
        autos_manuals[2] = autos_manual2
        autos_manual3 = automata.Automata(3)
        autos_manual3.windowsize = 3
        autos_manual3.nodes = {'b,c,d': 1}
        autos_manual3.connections.append({'Source node': ' b,c,d', 'sink node': 'c,d,e', 'probability': None})
        autos_manuals[3] = autos_manual3
        autos_manual4 = automata.Automata(4)
        autos_manual4.windowsize = 4
        autos_manual4.nodes = {'a,b,c,d': 1}
        autos_manual4.connections.append({'Source node': ' a,b,c,d', 'sink node': 'b,c,d,e', 'probability': None})
        autos_manuals[4] = autos_manual4
        case_thread.calcuate_connection_for_different_prefix_automata(windowsMemory)
        autos, status = set_globalvar.get_autos()
        for ws in config.WINDOW_SIZE:
            autos_manual = str(autos_manuals[ws]).replace("'", "")
            autos_manual = autos_manual.replace(" ", "")
            autos_computed = str(autos[ws]).replace('<', '{')
            autos_computed = autos_computed.replace('>', '}')
            autos_computed = autos_computed.replace("'", "")
            autos_computed = autos_computed.replace(" ", "")
            print(autos_computed)
            print(autos_manual)
            self.assertEqual(autos_computed, autos_manual)

    def tearUp(self):
        # do something after every test method
        # print(self)
        pass


if __name__ == '__main__':
    unittest.main()
