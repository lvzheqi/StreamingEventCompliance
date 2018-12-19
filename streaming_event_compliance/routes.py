from streaming_event_compliance import app
from flask import request, send_file
from flask_api import status
from streaming_event_compliance.services import visualization_deviation_automata, setup
from streaming_event_compliance.objects.variable.globalvar import gVars
from streaming_event_compliance.services.compliance_check import compliance_checker
from streaming_event_compliance.utils.config import CLEINT_DATA_PATH, AUTOMATA_FILE, FILE_TYPE
from streaming_event_compliance.database import dbtools
from streaming_event_compliance.objects.exceptions.exception import ThreadException
import json


@app.route('/')
def index():
    return 'Welcome to Compliance Server! We will provide 2 services!'


@app.route('/login', methods=['POST'])
def call_login():
    uuid = request.args.get('uuid')
    print('routes:', uuid)
    if dbtools.check_user_status(uuid) is None:
        user_status = False
    else:
        user_status = dbtools.check_user_status(uuid)
    gVars.clients_status[uuid] = user_status
    return str(user_status), status.HTTP_200_OK


@app.route('/compliance-checker', methods=['POST'])
def call_compliance_checker():
    '''
    This function provides the interface to check the compliance of the event.
    :return: status code, application/json
    '''
    uuid = request.args.get('uuid')
    if gVars.get_client_status(uuid):
        dbtools.delete_alert(uuid)
        dbtools.update_user_status(uuid, False)
        gVars.clients_status[uuid] = False

    if uuid not in gVars.clients_cc_status:
        gVars.clients_cc_status[uuid] = True
        setup.init_compliance_checking(uuid)

    event = request.json
    event = json.loads(event)
    try:
        return compliance_checker.compliance_checker(uuid, event), status.HTTP_200_OK
    except ThreadException:
        print('Error! Something wrong in compliance checking!')
        return "Server Error!"


@app.route('/show-deviation-pdf', methods=['GET', 'POST'])
def call_show_deviation_pdf():
    '''
    This function will render the deviation pdf with particular client_id in the browser,
    when the client has already done the “compliance checking”.
    :return: status code, application/pdf
    '''
    client_uuid = request.args.get('uuid')
    visualization_deviation_automata.show_deviation_pdf(client_uuid)
    try:
        automata_pdf = open(CLEINT_DATA_PATH + client_uuid + "_" + AUTOMATA_FILE + FILE_TYPE, 'rb')
        return send_file(automata_pdf, attachment_filename='file.pdf'), status.HTTP_200_OK
    except Exception:
        print('exception')
        return '', status.HTTP_404_NOT_FOUND
