from streaming_event_compliance import app
from streaming_event_compliance.services import globalvar
from flask_sqlalchemy import SQLAlchemy
import pytest
import os
import json


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['client_uuid'] = 'client_test'
    client = app.test_client()
    with app.app_context():
        globalvar.init()
        auto_status = globalvar.get_autos_status()
        print(auto_status)
        if auto_status == 0:
            globalvar.call_buildautos()
        print(auto_status)
    yield client


def test_index(client):
    """Start with a blank database."""
    rv = client.get('/')
    assert b'Welcome to Compliance Server! We will provide 2 services!' in rv.data


def test_call_login(client):
    rv = login(client, app.config['client_uuid'])
    assert b'False' in rv.data


def test_compliance_check(client):
    event = {}
    event['case_id'] = 'case1'
    event['activity'] = 'b'
    rv = compliance_check(client, app.config['client_uuid'], event)
    # assert b'Sorry, automata has not built, please wait for a while!' in rv.data
    assert b"{'case_id': 'case1', 'source_node': None, 'sink_node': 'b', 'cause': '', 'message': 'OK'}" in rv.data



def login(client, username):
    return client.post('/login', data=dict(
        username=username
    ), follow_redirects=True)


def compliance_check(client, client_uuid, event):
    return client.post('http://127.0.0.1:5000/compliance-checker?uuid=' + client_uuid,
                              json=json.dumps(event))