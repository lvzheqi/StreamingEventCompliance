import unittest
from streaming_event_compliance.objects.automata import automata


class AutomataTest(unittest.TestCase):
    def setUp(self):
        self.auto1 = automata.Automata(1)
        self.auto2 = automata.Automata(2)
        self.auto1.update_automata(automata.Connection('A', 'B', 1))
        self.auto1.update_automata(automata.Connection('A', 'B', 1))
        self.auto1.update_automata(automata.Connection('A', 'C', 1))
        self.auto1.update_automata(automata.Connection('C', '$', 0))
        self.auto2.update_automata(automata.Connection('A,B', 'B,C', 1))
        self.auto2.update_automata(automata.Connection('B,D', 'D,B', 1))
        self.auto1.set_probability()
        self.auto2.set_probability()

    def test_update_automata(self):
        for conn in self.auto1.connections:
            if conn.sink_node is 'B':
                self.assertAlmostEqual(conn.probability, 2/3)
            elif conn.sink_node is 'C':
                self.assertAlmostEqual(conn.probability, 1/3)
            elif conn.sink_node is '$':
                self.assertAlmostEqual(conn.probability, 0)
        for conn in self.auto2.connections:
            if conn.sink_node is 'B,C':
                self.assertAlmostEqual(conn.probability, 1)
            elif conn.sink_node is 'D,B':
                self.assertAlmostEqual(conn.probability, 1)
        self.assertEqual(self.auto1.nodes, {'A': 3, 'C': 0})
        self.assertEqual(self.auto2.nodes, {'A,B': 1, 'B,D': 1})

    def test_contains_source_node(self):
        self.assertEqual(self.auto1.contains_source_node('C'), True)
        self.assertEqual(self.auto1.contains_source_node('A'), True)
        self.assertEqual(self.auto1.contains_source_node('B'), False)
        self.assertEqual(self.auto1.contains_source_node('$'), False)

    def test_get_probability(self):
        self.assertAlmostEqual(self.auto1.get_connection_probability(automata.Connection('A', 'B')), 2/3)
        self.assertAlmostEqual(self.auto1.get_connection_probability(automata.Connection('A', 'C')), 1/3)
        self.assertAlmostEqual(self.auto1.get_connection_probability(automata.Connection('C', 'C')), -1)


if __name__ == '__main__':
    unittest.main()

