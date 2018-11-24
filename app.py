from flask import Flask, request, send_file
from services import complianceChecker, deviationPDF, buildAutomata
from utils import config
from test import dbTest
from test.dbTest import db as testdb
from objects.automata.automata import db as atdb
from objects.automata.alertLog import db as altdb
import json


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = config.BASE_DIR
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_PATH


atdb.init_app(app)
altdb.init_app(app)
testdb.init_app(app)
app.app_context().push()

@app.route('/')
def index():
    return 'Welcome to Compliance Server! We will provide 2 services!'


@app.route('/compliance-checker', methods=['POST'])
def call_compliance_checker():
    '''
    This function provides the interface to check the compliance of the event.
    :return: status code, application/json
    '''
    client_uuid = request.args.get('uuid')
    event = request.json
    event = json.loads(event)
    return complianceChecker.compliance_checker(client_uuid, event)


@app.route('/show-deviation-pdf', methods=['GET', 'POST'])
def call_show_deviation_pdf():
    '''
    This function will render the deviation pdf with particular client_id in the browser,
    when the client has already done the “compliance checking”.
    :return: status code, application/pdf
    '''
    client_uuid = request.args.get('uuid')
    deviationPDF.show_deviation_pdf(client_uuid)
    try:
        automata_pdf = open(client_uuid + "-" + config.AUTOMATA_FILE, 'rb')
        return send_file(automata_pdf, attachment_filename='file.pdf')
    except:
        print('exception')


buildAutomata.test_automata_status()
# TODO: catch exceptions


###### Test ######
dbTest.init()

if __name__ == '__main__':
    app.debug = True
    app.run()



# TODO: 1. logging  2. exceptions handing  3. describe for service  4. CORS

