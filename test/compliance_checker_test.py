import unittest
from streaming_event_compliance.utils import config
from streaming_event_compliance.services.build_automata import build_automata
from streaming_event_compliance.services.build_automata import case_thread
from streaming_event_compliance.database import dbtools
from streaming_event_compliance.services import globalvar
from pm4py.objects.log.importer.xes import factory as xes_importer
from pm4py.objects.log import transform


class ComplianceCheckerTestCase(unittest.TestCase):
    def test_call_compliance_checker(self):
        pass

