import unittest

from streaming_event_compliance.services.build_automata import build_automata
from streaming_event_compliance.services import case_thread
from streaming_event_compliance.services.case_thread import calcuate_connection_for_different_prefix_automata
from streaming_event_compliance.services.build_automata import check_order_list


class BuildingAutomataTestCase(unittest.TestCase):
    """
    Test function build_automata() in streaming_event_compliance/services/build_automata.py
    1.Generate EventLog2 in which each case is sorted from EventLog1
    2.Run buildAutomata.build_automata(EventLog1)
    3.Store the processing sequence of events of each case
    4.Compare these sequence with EventLog2 to see if all the events are processed in sequential
    """
    def setUp(self):
        '''do something before every test method'''
        print(self)

    def multi_threading_for_building_automata_test_case(self):
    # 做不到，因为用到全局变量呀？？？？
        check_order_list = []
        prima_list = build_automata()
        self.assertEqual(prima_list, check_order_list)

    # def calcuate_connection_for_different_prefix_automata(self):
    #     """
    #     """
    #     # Instantiate an object Connection
    #     Connection = calcuate_connection_for_different_prefix_automata()
    #     self.assertEqual(Connection, 'b')
    #
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

    def test(self):
        WINDOW_SIZE = [1, 2, 3, 4]
        windowsMemory = ['a', 'b', 'c', 'd', 'e']
        MAXIMUN_WINDOW_SIZE = 4


suite = unittest.TestLoader().loadTestsFromTestCase(BuildingAutomataTestCase)
unittest.TextTestRunner(verbosity=2).run(suite)