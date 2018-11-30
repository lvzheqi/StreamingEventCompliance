import unittest

if __name__ == '__main__':
    from test.database_test import DBToolsTest
    from test.automata_test import AutomataTest

    test_object1 = DBToolsTest()
    test_object2 = AutomataTest()

    unittest.main()
