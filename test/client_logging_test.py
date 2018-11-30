import unittest
from client.simulate_stream_event import client_logging


class TestClientLogging(unittest.TestCase):

    def test_client_logging(self):
        self.assertEqual(client_logging(message="All good", message_type="ERROR", level="INFO", func_name=func_name), True)
        self.assertEqual(client_logging(message="All good", message_type="ERROR", level="INFO", func_name=func_name,
         thread_id='1'), True)
        self.assertEqual(client_logging(message="All good", message_type="ERROR", level="INFO", func_name=func_name,
         case_id='1'), True)
        self.assertEqual(client_logging(message="All good", message_type="ERROR", level="INFO", func_name=func_name,
         case_id='1',activity="a"), True)


if __name__ == '__main__':
    unittest.main()
