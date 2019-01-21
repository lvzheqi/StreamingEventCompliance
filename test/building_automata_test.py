import unittest
from streaming_event_compliance import app
from streaming_event_compliance.services.build_automata import build_automata, case_thread
from streaming_event_compliance.services import setup
from streaming_event_compliance.database import dbtools
from streaming_event_compliance.objects.variable.globalvar import gVars
from pm4py.objects.log.importer.xes import factory as xes_importer
from pm4py.objects.log import transform
from streaming_event_compliance.objects.automata import automata
import os


class BuildingAutomataTestCase(unittest.TestCase):
    """
    Test function build_automata() in streaming_event_compliance/services/build_automata.py
    3.Store the processing sequence of events of each case
    4.Compare these sequence with EventLog2 to see if all the events are processed in sequential
    """

    def setUp(self):
        '''do something before every test method'''

        dbtools.empty_tables()
        setup.init_automata()
        app.config['TRAINING_EVENT_LOG_PATH'] = app.config['BASE_DIR'] + 'data' + os.sep + \
                                                'Simple_Training2.xes'

    def test_multi_threading_for_building_automata(self):
        '''
        This test should pass, but because the bulid_automata() execuated twice
        the expected_log and check_executing_order are not same
        :return:
        '''
        # read file
        trace_log = xes_importer.import_log(app.config['TRAINING_EVENT_LOG_PATH'])
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
        self.assertEqual(expected_log, case_thread.check_executing_order)

    # def test_calcuate_connection_for_different_prefix_automata(self):
    #     ws = app.config['WINDOW_SIZE']
    #     if ws == [1, 2, 3, 4]:
    #         windowsMemory = ['a', 'b', 'c', 'd', 'e']
    #
    #         autos_manual1 = automata.Automata()
    #         autos_manual1.update_automata(automata.Connection('d', 'e', 1))
    #         autos_manual2 = automata.Automata()
    #         autos_manual2.update_automata(automata.Connection('c,d', 'd,e', 1))
    #         autos_manual3 = automata.Automata()
    #         autos_manual3.update_automata(automata.Connection('b,c,d', 'c,d,e', 1))
    #         autos_manual4 = automata.Automata()
    #         autos_manual4.update_automata(automata.Connection('a,b,c,d', 'b,c,d,e', 1))
    #         autos_manuals = {1: autos_manual1, 2: autos_manual2, 3: autos_manual3, 4: autos_manual4}
    #         case_thread.calculate_connection_for_different_prefix_automata(windowsMemory)
    #         for ws in app.config['WINDOW_SIZE']:
    #             self.assertEqual(autos_manuals[ws].get_connections(), gVars.autos[ws].get_connections())
    #             self.assertEqual(autos_manuals[ws].get_nodes(), gVars.autos[ws].get_nodes())

    # def test_calcuate_connection_for_different_prefix_automata_with_endevent(self):
    #     ws = app.config['WINDOW_SIZE']
    #     if ws == [1, 2, 3, 4]:
    #         windowsMemory = ['a', 'b', 'c', 'd', '~!@#$%']
    #         autos_manual1 = automata.Automata()
    #         autos_manual1.update_automata(automata.Connection('d', '~!@#$%', 0))
    #         autos_manual2 = automata.Automata()
    #         autos_manual2.update_automata(automata.Connection('c,d', '~!@#$%', 0))
    #         autos_manual3 = automata.Automata()
    #         autos_manual3.update_automata(automata.Connection('b,c,d', '~!@#$%', 0))
    #         autos_manual4 = automata.Automata()
    #         autos_manual4.update_automata(automata.Connection('a,b,c,d', '~!@#$%', 0))
    #         autos_manuals = {1: autos_manual1, 2: autos_manual2, 3: autos_manual3, 4: autos_manual4}
    #         case_thread.calculate_connection_for_different_prefix_automata(windowsMemory)
    #         for ws in app.config['WINDOW_SIZE']:
    #             self.assertEqual(autos_manuals[ws].get_connections(), gVars.autos[ws].get_connections())
    #             self.assertEqual(autos_manuals[ws].get_nodes(), gVars.autos[ws].get_nodes())
    #

if __name__ == '__main__':
    unittest.main()
