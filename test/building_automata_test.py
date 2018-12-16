import unittest
from streaming_event_compliance.utils import config
from streaming_event_compliance.services.build_automata import build_automata
from streaming_event_compliance.services.build_automata import case_thread
from streaming_event_compliance.database import dbtools
from streaming_event_compliance.services import globalvar
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

        end_message = {}
        for case in expected_log:
            end_message['case_id'] = item
            end_message['activity'] = '!@#$%^'
            expected_log.get(case).append(end_message['activity'])
        build_automata.build_automata()
        self.assertEqual(expected_log, case_thread.check_executing_order)

    def test_calcuate_connection_for_different_prefix_automata(self):
        windowsMemory = ['a', 'b', 'c', 'd', 'e']
        autos_manual1 = automata.Automata(1)
        autos_manual1.update_automata(automata.Connection('d', 'e', 1))
        autos_manual2 = automata.Automata(2)
        autos_manual2.update_automata(automata.Connection('c,d', 'd,e', 1))
        autos_manual3 = automata.Automata(3)
        autos_manual3.update_automata(automata.Connection('b,c,d', 'c,d,e', 1))
        autos_manual4 = automata.Automata(4)
        autos_manual4.update_automata(automata.Connection('a,b,c,d', 'b,c,d,e', 1))
        autos_manuals = {1: autos_manual1, 2: autos_manual2, 3: autos_manual3, 4: autos_manual4}
        case_thread.calcuate_connection_for_different_prefix_automata(windowsMemory)
        autos = globalvar.get_autos()
        # self.assertEqual(autos_manuals, autos)
        for ws in config.WINDOW_SIZE:
            self.assertEqual(autos_manuals[ws].connections, autos[ws].connections)
            self.assertEqual(autos_manuals[ws].nodes, autos[ws].nodes)

    def test_calcuate_connection_for_different_prefix_automata_with_endevent(self):
        windowsMemory = ['a', 'b', 'c', 'd', '!@#$%^']
        autos_manual1 = automata.Automata(1)
        autos_manual1.update_automata(automata.Connection('d', '!@#$%^', 0))
        autos_manual2 = automata.Automata(2)
        autos_manual2.update_automata(automata.Connection('c,d', '!@#$%^', 0))
        autos_manual3 = automata.Automata(3)
        autos_manual3.update_automata(automata.Connection('b,c,d', '!@#$%^', 0))
        autos_manual4 = automata.Automata(4)
        autos_manual4.update_automata(automata.Connection('a,b,c,d', '!@#$%^', 0))
        autos_manuals = {1: autos_manual1, 2: autos_manual2, 3: autos_manual3, 4: autos_manual4}
        case_thread.calcuate_connection_for_different_prefix_automata(windowsMemory)
        autos = globalvar.get_autos()
        for ws in config.WINDOW_SIZE:
            self.assertEqual(autos_manuals[ws].connections, autos[ws].connections)
            self.assertEqual(autos_manuals[ws].nodes, autos[ws].nodes)
    #     autos_manuals = {}
    #     autos_manual1 = automata.Automata(1)
    #     autos_manual1.windowsize = 1
    #     autos_manual1.nodes = {'d': 0}
    #     autos_manual1.connections.append({'Source node': ' d', 'sink node': '!@#$%^', 'probability': None})
    #     autos_manuals[1] = autos_manual1
    #     autos_manual2 = automata.Automata(2)
    #     autos_manual2.windowsize = 2
    #     autos_manual2.nodes = {'c,d': 0}
    #     autos_manual2.connections.append({'Source node': ' c,d', 'sink node': '!@#$%^', 'probability': None})
    #     autos_manuals[2] = autos_manual2
    #     autos_manual3 = automata.Automata(3)
    #     autos_manual3.windowsize = 3
    #     autos_manual3.nodes = {'b,c,d': 0}
    #     autos_manual3.connections.append({'Source node': ' b,c,d', 'sink node': '!@#$%^', 'probability': None})
    #     autos_manuals[3] = autos_manual3
    #     autos_manual4 = automata.Automata(4)
    #     autos_manual4.windowsize = 4
    #     autos_manual4.nodes = {'a,b,c,d': 0}
    #     autos_manual4.connections.append({'Source node': ' a,b,c,d', 'sink node': '!@#$%^', 'probability': None})
    #     autos_manuals[4] = autos_manual4
    #     case_thread.calcuate_connection_for_different_prefix_automata(windowsMemory)
    #     autos = globalvar.get_autos()
    #     for ws in config.WINDOW_SIZE:
    #         autos_manual = str(autos_manuals[ws]).replace("'", "")
    #         autos_manual = autos_manual.replace(" ", "")
    #         autos_computed = str(autos[ws]).replace('<', '{')
    #         autos_computed = autos_computed.replace('>', '}')
    #         autos_computed = autos_computed.replace("'", "")
    #         autos_computed = autos_computed.replace(" ", "")
    #         self.assertEqual(autos_computed, autos_manual)


if __name__ == '__main__':
    unittest.main()

# autos_manual1.windowsize = 1
# autos_manual1.nodes = {'d': 1}
# autos_manual1.connections.append({'Source node': ' d', 'sink node': 'e', 'probability': None})
# autos_manuals[1] = autos_manual1
# autos_manual2 = automata.Automata(2)
# autos_manual2.windowsize = 2
# autos_manual2.nodes = {'c,d': 1}
# autos_manual2.connections.append({'Source node': ' c,d', 'sink node': 'd,e', 'probability': None})
# autos_manuals[2] = autos_manual2
# autos_manual3 = automata.Automata(3)
# autos_manual3.windowsize = 3
# autos_manual3.nodes = {'b,c,d': 1}
# autos_manual3.connections.append({'Source node': ' b,c,d', 'sink node': 'c,d,e', 'probability': None})
# autos_manuals[3] = autos_manual3
# autos_manual4 = automata.Automata(4)
# autos_manual4.windowsize = 4
# autos_manual4.nodes = {'a,b,c,d': 1}
# autos_manual4.connections.append({'Source node': ' a,b,c,d', 'sink node': 'b,c,d,e', 'probability': None})
# autos_manuals[4] = autos_manual4

# autos_manual = str(autos_manuals[ws]).replace("'", "")
# autos_manual = autos_manual.replace(" ", "")
# autos_computed = str(autos[ws]).replace('<', '{')
# autos_computed = autos_computed.replace('>', '}')
# autos_computed = autos_computed.replace("'", "")
# autos_computed = autos_computed.replace(" ", "")
# self.assertEqual(autos_computed, autos_manual)