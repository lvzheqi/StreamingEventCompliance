from streaming_event_compliance import app, config
from flask import request, send_file
from flask_api import status
from streaming_event_compliance.services import compliance_checker
from streaming_event_compliance.services import deviation_pdf
import json
import os



@app.route('/')
def index():
    return 'Welcome to Compliance Server! We will provide 2 services!'


@app.route('/login', methods=['POST'])
def call_login():
    '''
    This function will create a user, if the given user name is not created
    '''
    client_uuid = request.args.get('uuid')
    # TODO: create user
    return '', status.HTTP_200_OK


@app.route('/compliance-checker', methods=['POST'])
def call_compliance_checker():
    '''
    This function provides the interface to check the compliance of the event.
    :return: status code, application/json
    '''
    client_uuid = request.args.get('uuid')
    print(client_uuid)
    event = request.json
    event = json.loads(event)
    print(event)
    print(compliance_checker.compliance_checker(client_uuid, event))
    return compliance_checker.compliance_checker(client_uuid, event), status.HTTP_200_OK


@app.route('/show-deviation-pdf', methods=['GET', 'POST'])
def call_show_deviation_pdf():
    '''
    This function will render the deviation pdf with particular client_id in the browser,
    when the client has already done the “compliance checking”.
    :return: status code, application/pdf
    '''
    client_uuid = request.args.get('uuid')
    deviation_pdf.show_deviation_pdf(client_uuid)
    try:
        automata_pdf = open(config.BASE_DIR + '/data' + os.sep + client_uuid + "-" + config.AUTOMATA_FILE, 'rb')
        return send_file(automata_pdf, attachment_filename='file.pdf'), status.HTTP_200_OK
    except Exception: # TODO: read file error
        print('exception')
        return '', status.HTTP_404_NOT_FOUND
