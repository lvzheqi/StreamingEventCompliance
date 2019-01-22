import unittest

if __name__ == '__main__':
    from test.database_test import DBToolsTest
    from test.automata_test import AutomataTest
    from test.alertlog_test import AlertlogTest
    from test.server_logging_tests import TestServerLogging
    from test.building_automata_test import BuildingAutomataTestCase
    from test.create_probability_automata_test import CreateProbabilityAutomataTest

    test_object1 = DBToolsTest()
    test_object2 = AutomataTest()
    test_object3 = AlertlogTest()
    test_object4 = BuildingAutomataTestCase()
    test_object5 = CreateProbabilityAutomataTest()
    test_object6 = TestServerLogging()

    unittest.main()
