from flask import Flask, request, send_file
from flask_api import status
from streaming_event_compliance.services import compliance_checker, build_automata
from streaming_event_compliance.services import deviation_pdf
from streaming_event_compliance.utils import config
from test.db_test import DatabaseTest
from streaming_event_compliance.objects.automata.automata import db as atdb
from streaming_event_compliance.objects.automata.automata import db as altdb
import json


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = config.BASE_DIR
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_PATH


atdb.init_app(app)
altdb.init_app(app)
testdb = DatabaseTest()
testdb.db.init_app(app)
app.app_context().push()


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
        automata_pdf = open('data/' + client_uuid + "-" + config.AUTOMATA_FILE, 'rb')
        return send_file(automata_pdf, attachment_filename='file.pdf'), status.HTTP_200_OK
    except Exception: # TODO: read file error
        print('exception')
        return '', status.HTTP_404_NOT_FOUND


build_automata.test_automata_status()
# TODO: catch exceptions


###### Test ######
testdb.init()

if __name__ == '__main__':
    app.debug = True
    app.run()



# TODO: 1. logging  2. exceptions handing  3. describe for service  4. CORS

