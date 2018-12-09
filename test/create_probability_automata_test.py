import unittest
from streaming_event_compliance.services.visualization import probability_automata
from streaming_event_compliance.services import globalvar


class CreateProbabilityAutomataTest(unittest.TestCase):
    def setUp(self):
        globalvar.init()

    def test_create_automata(self):
        probability_automata.apply(globalvar.autos)


if __name__ == '__main__':
    unittest.main()
