import unittest
from streaming_event_compliance.objects.automata import automata, alertlog


class AutomataTest(unittest.TestCase):
    def setUp(self):
        self.auto1 = automata.Automata(1)
        self.auto2 = automata.Automata(2)
        self.auto1.update_automata(automata.Connection('A', 'B', 1))
        self.auto1.update_automata(automata.Connection('A', 'B', 1))
        self.auto1.update_automata(automata.Connection('A', 'C', 1))
        self.auto2.update_automata(automata.Connection('AB', 'BC', 1))
        self.auto2.update_automata(automata.Connection('BD', 'DB', 1))
        self.auto1.set_probability()
        self.auto2.set_probability()

    def test_update_automata(self):
        for conn in self.auto1.connections:
            if conn.sink_node is 'B':
                self.assertAlmostEqual(conn.probability, 2/3)
            elif conn.sink_node is 'C':
                self.assertAlmostEqual(conn.probability, 1/3)
        for conn in self.auto2.connections:
            if conn.sink_node is 'BC':
                self.assertAlmostEqual(conn.probability, 1)
            elif conn.sink_node is 'DB':
                self.assertAlmostEqual(conn.probability, 1)
        self.assertEqual(self.auto1.nodes, {'A': 3})
        self.assertEqual(self.auto2.nodes, {'AB': 1, 'BD': 1})


if __name__ == '__main__':
    unittest.main()

