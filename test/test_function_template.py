import unittest

from test.function_template_for_test import get_formatted_name
"""单元测试"""
class NamesTestCase(unittest.TestCase):
    #的测试name_function.py"""
    def setUp(self):
        '''do something before every test method'''
        print(self)

    def test_first_last_name(self):
        """能够正确的处理像Janis Joplin这样的姓名吗？"""
        formatted_name = get_formatted_name('janis', 'joplin')
        self.assertEqual(formatted_name, 'Janis Joplin')

    def test_first_middle_last_name(self):
        """能够正确的处理像Wolfgang Amadeus Mozart这样的姓名吗？"""
        formatted_name = get_formatted_name('wolfgang', 'amadeus', 'mozart')
        self.assertEqual(formatted_name, 'Wolfgang Mozart Amadeus')

    def tearUp(self):
        # do something after every test method
        print(self)

suite = unittest.TestLoader().loadTestsFromTestCase(NamesTestCase)
unittest.TextTestRunner(verbosity=2).run(suite)