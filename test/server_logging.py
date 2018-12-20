import unittest
from streaming_event_compliance.server_logging import ServerLogging
from streaming_event_compliance import app
import sys

SERVER_LOG_PATH = app.config['SERVER_LOG_PATH']

class TestClientLogging(unittest.TestCase):

    def test_log_info_2(self):
        func_name = sys._getframe().f_code.co_name
        test_data_in_log_file = ''
        compare_test_data_in_log_file = "INFO Username:Unknown test_log_info_2 'Testing logging info with 2 arguments'"
        ServerLogging().log_info(func_name, "Testing logging info with 2 arguments")
        with open(SERVER_LOG_PATH, 'r') as f:
            lines = f.read().splitlines()
            test_data_in_log_file = lines[-1]
            test_data_in_log_file = ' '.join(test_data_in_log_file.split(' ')[3:])
            print(test_data_in_log_file)
            print(compare_test_data_in_log_file)
        self.assertEqual(test_data_in_log_file, compare_test_data_in_log_file)

    def test_log_info_3(self):
        func_name = sys._getframe().f_code.co_name
        uuid = 'test_user'
        test_data_in_log_file = ''
        compare_test_data_in_log_file = "INFO test_user test_log_info_3 'Testing logging info with 3 arguments'"
        ServerLogging().log_info(func_name, uuid, "Testing logging info with 3 arguments")
        with open(SERVER_LOG_PATH, 'r') as f:
            lines = f.read().splitlines()
            test_data_in_log_file = lines[-1]
            test_data_in_log_file = ' '.join(test_data_in_log_file.split(' ')[3:])
            print(test_data_in_log_file)
            print(compare_test_data_in_log_file)
        self.assertEqual(test_data_in_log_file, compare_test_data_in_log_file)

    def test_log_info_5(self):
        func_name = sys._getframe().f_code.co_name
        uuid = 'test_user'
        dic = {
            'case_id': 'test1',
            'activity': 'testing_log_info_5',
        }
        test_data_in_log_file = ''
        compare_test_data_in_log_file = "INFO test_user test_log_info_5 Case_id:test1 Activity:testing_log_info_5 " \
                                        "'Testing logging info with 5 arguments'"
        ServerLogging().log_info(func_name, uuid, dic['case_id'], dic['activity'], "Testing logging info with 5 "
                                                                                   "arguments")
        with open(SERVER_LOG_PATH, 'r') as f:
            lines = f.read().splitlines()
            test_data_in_log_file = lines[-1]
            test_data_in_log_file = ' '.join(test_data_in_log_file.split(' ')[3:])
            print(test_data_in_log_file)
            print(compare_test_data_in_log_file)
        self.assertEqual(test_data_in_log_file, compare_test_data_in_log_file)

    def test_log_info_6(self):
        func_name = sys._getframe().f_code.co_name
        uuid = 'test_user'
        dic = {
            'case_id': 'test1',
            'activity': 'testing_log_info_6',
        }
        thread_id = 1
        test_data_in_log_file = ''
        compare_test_data_in_log_file = "INFO test_user test_log_info_6 Thread:1 Case_id:test1 Activity:testing_" \
                                        "log_info_6 " \
                                        "'Testing logging info with 6 arguments'"
        ServerLogging().log_info(func_name, uuid, thread_id, dic['case_id'], dic['activity'], "Testing logging info with 6 "
                                                                                   "arguments")
        with open(SERVER_LOG_PATH, 'r') as f:
            lines = f.read().splitlines()
            test_data_in_log_file = lines[-1]
            test_data_in_log_file = ' '.join(test_data_in_log_file.split(' ')[3:])
            print(test_data_in_log_file)
            print(compare_test_data_in_log_file)
        self.assertEqual(test_data_in_log_file, compare_test_data_in_log_file)

    def test_log_error_2(self):
        func_name = sys._getframe().f_code.co_name
        test_data_in_log_file = ''
        compare_test_data_in_log_file = "ERROR Username:Unknown test_log_error_2 'Testing logging error with 2 arguments'"
        ServerLogging().log_error(func_name, "Testing logging error with 2 arguments")
        with open(SERVER_LOG_PATH, 'r') as f:
            lines = f.read().splitlines()
            test_data_in_log_file = lines[-1]
            test_data_in_log_file = ' '.join(test_data_in_log_file.split(' ')[3:])
            print(test_data_in_log_file)
            print(compare_test_data_in_log_file)
        self.assertEqual(test_data_in_log_file, compare_test_data_in_log_file)

    def test_log_error_3(self):
        func_name = sys._getframe().f_code.co_name
        uuid = 'test_user'
        test_data_in_log_file = ''
        compare_test_data_in_log_file = "ERROR test_user test_log_error_3 'Testing logging error with 3 arguments'"
        ServerLogging().log_error(func_name, uuid, "Testing logging error with 3 arguments")
        with open(SERVER_LOG_PATH, 'r') as f:
            lines = f.read().splitlines()
            test_data_in_log_file = lines[-1]
            test_data_in_log_file = ' '.join(test_data_in_log_file.split(' ')[3:])
            print(test_data_in_log_file)
            print(compare_test_data_in_log_file)
        self.assertEqual(test_data_in_log_file, compare_test_data_in_log_file)

    def test_log_error_5(self):
        func_name = sys._getframe().f_code.co_name
        uuid = 'test_user'
        dic = {
            'case_id': 'test1',
            'activity': 'testing_log_info_5',
        }
        test_data_in_log_file = ''
        compare_test_data_in_log_file = "ERROR test_user test_log_error_5 Case_id:test1 Activity:testing_log_info_5 " \
                                        "'Testing logging error with 5 arguments'"
        ServerLogging().log_error(func_name, uuid, dic['case_id'], dic['activity'], "Testing logging error with 5 "
                                                                                    "arguments")
        with open(SERVER_LOG_PATH, 'r') as f:
            lines = f.read().splitlines()
            test_data_in_log_file = lines[-1]
            test_data_in_log_file = ' '.join(test_data_in_log_file.split(' ')[3:])
            print(test_data_in_log_file)
            print(compare_test_data_in_log_file)
        self.assertEqual(test_data_in_log_file, compare_test_data_in_log_file)

    def test_log_error_6(self):
        func_name = sys._getframe().f_code.co_name
        uuid = 'test_user'
        dic = {
            'case_id': 'test1',
            'activity': 'testing_log_info_6',
        }
        thread_id = 1
        test_data_in_log_file = ''
        compare_test_data_in_log_file = "ERROR test_user test_log_error_6 Thread:1 Case_id:test1 Activity:testing_" \
                                        "log_info_6 " \
                                        "'Testing logging error with 6 arguments'"
        ServerLogging().log_error(func_name, uuid, thread_id, dic['case_id'], dic['activity'],
                                  "Testing logging error with 6 "
                                  "arguments")
        with open(SERVER_LOG_PATH, 'r') as f:
            lines = f.read().splitlines()
            test_data_in_log_file = lines[-1]
            test_data_in_log_file = ' '.join(test_data_in_log_file.split(' ')[3:])
            print(test_data_in_log_file)
            print(compare_test_data_in_log_file)
        self.assertEqual(test_data_in_log_file, compare_test_data_in_log_file)


if __name__ == '__main__':
    unittest.main()
