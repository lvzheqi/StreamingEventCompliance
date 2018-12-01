import unittest
from streaming_event_compliance import config
from streaming_event_compliance.services.build_automata import build_automata
from streaming_event_compliance.services.build_automata.case_thread import check_executing_order
from streaming_event_compliance.services import globalvar
from streaming_event_compliance.utils import dbtools
from pm4py.objects.log.importer.xes import factory as xes_importer
from pm4py.objects.log import transform

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
        self.assertEqual(expected_log, check_executing_order)


    # def test_calcuate_connection_for_different_prefix_automata(self):
    #     """
    #     """
    #     # Instantiate an object Connection
    #     Connection = calcuate_connection_for_different_prefix_automata()
    #     self.assertEqual(Connection, 'b')



    def tearUp(self):
        # do something after every test method
        print(self)


suite = unittest.TestLoader().loadTestsFromTestCase(BuildingAutomataTestCase)
unittest.TextTestRunner(verbosity=2).run(suite)