import unittest
from streaming_event_compliance.services.visualization import probability_automata
from streaming_event_compliance.services.build_automata import build_automata
from streaming_event_compliance.database import dbtools
from streaming_event_compliance.services import globalvar


class CreateProbabilityAutomataTest(unittest.TestCase):
    def setUp(self):
        dbtools.empty_tables()
        globalvar.init()
        build_automata.build_automata()

    def test_create_automata(self):
        probability_automata.apply(globalvar.autos)


if __name__ == '__main__':
    unittest.main()