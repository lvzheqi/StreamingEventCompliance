from streaming_event_compliance import app
from streaming_event_compliance.objects.variable.globalvar import gVars
from streaming_event_compliance.services.build_automata import build_automata
from streaming_event_compliance.services import setup
import pytest
import json
from pm4py.objects.log.importer.xes import factory as xes_importer
from pm4py.objects.log import transform
import time
from console_logging.console import Console
console = Console()
console.setVerbosity(5)


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['client_uuid'] = 'client_test_1'
    client = app.test_client()
    with app.app_context():
        setup.init_automata()
        console.info("Init automata from database is finished, gVars.auto_status is " + str(gVars.auto_status))
        if gVars.auto_status == 0:
            build_automata.build_automata()
            console.info("Build automata is finished")
    yield client


def test_index(client):
    rv = client.get('/')
    assert b'Welcome to Compliance Server! We will provide 2 services!' in rv.data


def test_call_login(client):
    rv = login(client, app.config['client_uuid'])
    assert b'False' in rv.data


def test_compliance_check_time(client):
    '''
    Use event log with different length to test the time(average time).
    :param client:
    :return:
    '''
    uuid = app.config['client_uuid']
    login(client, uuid)

    path = app.config['TRAINING_EVENT_LOG_PATH']
    console.secure('Training Path:', str(path))

    path = app.config['BASE_DIR'] + '../../Downloads/C2018_Train.xes'
    event_log = prepare_event_log(path)
    sum = len(event_log)
    start = time.clock()
    compliance_check(client, uuid, event_log)
    end = time.clock()
    runtime = end - start
    results = sum / runtime
    console.secure('Testing Path:', str(path))
    console.secure('Events_number:', str(sum))
    console.secure('Running time:', str(runtime))
    console.secure('Average speed:', str(results) + ' per second!\n')
    assert results > 30


def compliance_check(client, uuid, event_log):
    '''
    Use the same event log as the trianing phase to do compliacnce checker, so the alerts should be only the
    type 'T'.
    :param client:
    :return:
    '''
    ok = 0
    alertT = 0
    alertM = 0
    error = 0
    for one_event in event_log:
        event = {}
        for item in one_event.keys():
            if item == 'concept:name':
                event['activity'] = one_event.get(item)
            elif item == 'case:concept:name':
                event['case_id'] = one_event.get(item)
        rv = client.post('/compliance-checker?uuid=' + uuid, json=json.dumps(event))
        ok += rv.data.count(b'OK')
        alertT += rv.data.count(b'T')
        alertM += rv.data.count(b'M')
        error += rv.data.count(b'Error')
        assert b'Error' not in rv.data
    console.secure('Results:', 'OK:' + str(ok) + '; Alert T:' + str(alertT) +
                   '; Alert M:' + str(alertM) + '; Error:' + str(error))


def login(client, uuid):
    return client.post('/login?uuid=' + uuid)


def prepare_event_log(path):
    trace_log = xes_importer.import_log(path)
    event_log = transform.transform_trace_log_to_event_log(trace_log)
    event_log.sort()
    return event_log
