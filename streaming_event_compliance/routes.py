from streaming_event_compliance import app
from flask import request, send_file
from flask_api import status
from streaming_event_compliance.services import setup
from streaming_event_compliance.services.visualization import visualization_deviation_automata
from streaming_event_compliance.objects.variable.globalvar import gVars
from streaming_event_compliance.services.compliance_check import compliance_checker
from streaming_event_compliance.database import dbtools
from streaming_event_compliance.objects.exceptions.exception import ThreadException
import json, traceback
from console_logging.console import Console
console = Console()
console.setVerbosity(5)

CLEINT_DATA_PATH = app.config['CLEINT_DATA_PATH']
AUTOMATA_FILE = app.config['AUTOMATA_FILE']
FILE_TYPE = app.config['FILE_TYPE']


@app.route('/')
def index():
    return 'Welcome to Compliance Server! We will provide 2 services!'


@app.route('/login', methods=['POST'])
def call_login():
    uuid = request.args.get('uuid')
    if uuid in gVars.clients_cc_status:
        return 'Refuse', status.HTTP_200_OK
    return str(check_client_stauts(uuid)), status.HTTP_200_OK


@app.route('/compliance-checker', methods=['POST'])
def call_compliance_checker():
    '''
    This function provides the interface to check the compliance of the event.
    :return: status code, application/json
    '''

    uuid = request.args.get('uuid')
    response = json.dumps({'body': 'Error, something wrong!'})
    try:
        if uuid not in gVars.clients_status:
            check_client_stauts(uuid)
        elif gVars.get_client_status(uuid):
            dbtools.delete_alert(uuid)
            dbtools.update_client_status(uuid, False)
            gVars.clients_status[uuid] = False

        if uuid not in gVars.clients_cc_status:
            gVars.clients_cc_status[uuid] = True
            setup.init_compliance_checking(uuid)

        event = request.json
        event = json.loads(event)
        response = compliance_checker.compliance_checker(uuid, event), status.HTTP_200_OK
    except KeyError:
        console.error('Something wrong in parameter getting!' + traceback.format_exc())
    except ThreadException:
        console.error('Something wrong in threading!' + traceback.format_exc())
    except Exception as e:
        print(e)
    finally:
        return response


@app.route('/show-deviation-pdf', methods=['GET', 'POST'])
def call_show_deviation_pdf():
    '''
    This function will render the deviation pdf with particular client_id in the browser,
    when the client has already done the “compliance checking”.
    :return: status code, application/pdf
    '''
    client_uuid = request.args.get('uuid')
    pdf_status = visualization_deviation_automata.show_deviation_pdf(client_uuid)
    if pdf_status == 1:
        try:
            automata_pdf = open(CLEINT_DATA_PATH + client_uuid + '_' + AUTOMATA_FILE + FILE_TYPE, 'rb')
            return send_file(automata_pdf, attachment_filename='file.pdf'), status.HTTP_200_OK
        except Exception:
            console.error('Error! Something wrong in call_show_deviation_pdf!' + traceback.format_exc())
            return '', status.HTTP_404_NOT_FOUND
    else:
        return '', status.HTTP_200_OK


def check_client_stauts(uuid):
    client_status = dbtools.check_client_status(uuid)
    if client_status is None:
        client_status = False
    gVars.clients_status[uuid] = client_status
    return client_status
