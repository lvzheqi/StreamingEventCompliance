from streaming_event_compliance import app
from streaming_event_compliance.objects.variable.globalvar import gVars
from streaming_event_compliance.services.build_automata import build_automata
from streaming_event_compliance.services import setup
import pytest
import json
from streaming_event_compliance.utils import config
from pm4py.objects.log.importer.xes import factory as xes_importer
from pm4py.objects.log import transform
import time
import os


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['client_uuid'] = 'client_test'
    client = app.test_client()
    with app.app_context():
        setup.init_automata()
        if gVars.auto_status == 0:
            build_automata.build_automata()
    yield client


def test_index(client):
    """Start with a blank database."""
    rv = client.get('/')
    assert b'Welcome to Compliance Server! We will provide 2 services!' in rv.data


def test_call_login(client):
    rv = login(client, app.config['client_uuid'])
    assert b'False' in rv.data


def test_compliance_check(client):
    """
    Case1: No alerts
    :param client:
    :return:
    """
    login(client, app.config['client_uuid'])
    print(gVars.clients_status)
    # path = config.BASE_DIR + 'data' + os.sep + 'Abelow100M.xes'
    path = config.TRAINING_EVENT_LOG_PATH
    trace_log = xes_importer.import_log(path)
    event_log = transform.transform_trace_log_to_event_log(trace_log)
    event_log.sort()
    sum = len(event_log)
    start = time.clock()
    for one_event in event_log:
        event = {}
        for item in one_event.keys():
            if item == 'concept:name':
                event['activity'] = one_event.get(item)
            elif item == 'case:concept:name':
                event['case_id'] = one_event.get(item)
        rv = compliance_check(client, app.config['client_uuid'], event)
    end = time.clock()
    results = sum / (end - start)
    print(results)
    assert results > 300


def login(client, client_uuid):
    print('do logon', client_uuid)
    assert client.get('/create').status_code == 200
    return client.post('/login', data={'uuid':client_uuid,})


def compliance_check(client, client_uuid, event):
    print('do cc:', client_uuid)
    return client.post('/compliance-checker?uuid=' + client_uuid, json=json.dumps(event))