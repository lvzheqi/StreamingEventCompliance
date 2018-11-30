import unittest
from client.simulate_stream_event import eventlog
from client.simulate_stream_event import exception

class BadAssError(TypeError):
    pass


class TestClient(unittest.TestCase):

    def test_read_log(self):
        client_uuid = 'test_client_uuid'
        path = 'asdfa'
        self.assertRaises(exception.ReadFileException, eventlog.read_log(client_uuid, path))
        # self.assertRaises(TypeError, eventlog.read_log(client_uuid, path))
        # self.assertRaises(Exception, eventlog.read_log(client_uuid, path))


suite = unittest.TestLoader().loadTestsFromTestCase(TestClient)
unittest.TextTestRunner(verbosity=2).run(suite)
