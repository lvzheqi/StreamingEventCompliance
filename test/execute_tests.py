import unittest

if __name__ == '__main__':
    from test.database_test import DBToolsTest
    from test.automata_test import AutomataTest
    from test.alertlog_test import AlertlogTest
    # from test.building_automata_test import BuildingAutomataTestCase

    test_object1 = DBToolsTest()
    test_object2 = AutomataTest()
    test_object3 = AlertlogTest()
    # test_object4 = BuildingAutomataTestCase()

    unittest.main()
