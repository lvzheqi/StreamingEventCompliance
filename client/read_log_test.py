import unittest
from simulate_stream_event import eventlog
from simulate_stream_event import exception


class TestClient(unittest.TestCase):

    def test_read_log_exception(self):
        client_uuid = 'test_client_uuid'
        path = 'asdfa'
        self.assertRaises(exception.ReadFileException,
                          lambda: eventlog.read_log(client_uuid, path))
        print(exception.ReadFileException, exception.ReadFileException.message)


if __name__ == '__main__':
    unittest.main()

#TODO: jingjinghuo: This file path need to be changed. But if I move it to another filefolder, some modules can not been found.