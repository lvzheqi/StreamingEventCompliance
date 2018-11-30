import unittest
from streaming_event_compliance.services.build_automata import build_automata
from streaming_event_compliance.services.build_automata.build_automata import C
from streaming_event_compliance.services.build_automata.case_thread import check_executing_order
from streaming_event_compliance import db


class BuildingAutomataTestCase(unittest.TestCase):
    """
    Test function build_automata() in streaming_event_compliance/services/build_automata.py
    3.Store the processing sequence of events of each case
    4.Compare these sequence with EventLog2 to see if all the events are processed in sequential
    """
    def setUp(self):
        '''do something before every test method'''
        try:
            db.create_all()
        except Exception:
            print('Error: Database connection!')
            exit(1)
        from streaming_event_compliance.services import globalvar
        from streaming_event_compliance.utils import dbtools
        dbtools.empty_tables()
        globalvar.init()

    def test_multi_threading_for_building_automata(self):
        build_automata.build_automata()
        print("-++++++++++++++++++-")
        print('expected value:', C.dictionary_cases)
        print('executing value:', check_executing_order)
        self.assertEqual(C.dictionary_cases, check_executing_order)


    # def calcuate_connection_for_different_prefix_automata(self):
    #     """
    #     """
    #     # Instantiate an object Connection
    #     Connection = calcuate_connection_for_different_prefix_automata()
    #     self.assertEqual(Connection, 'b')

    # def correctness_of_automata(self):
    #     """
    #     test if the builded automata is correct.
    #     """
    #     # Instantiate an object Automata.
    #     automata = calcuate_connection_for_different_prefix_automata()
    #     correctAutomata = ' '
    #     self.assertEqual(automata, correctAutomata)

    def tearUp(self):
        # do something after every test method
        print(self)


suite = unittest.TestLoader().loadTestsFromTestCase(BuildingAutomataTestCase)
unittest.TextTestRunner(verbosity=2).run(suite)