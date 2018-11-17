from flask import Flask, request, send_file
from services import complianceChecker, deviationPDF, buildAutomata
from config import defaultConfig
import json


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = defaultConfig.BASE_DIR


@app.route('/')
def index():
    return 'Welcome to Compliance Server! We will provide 2 services!'


@app.route('/compliance-checker', methods=['POST'])
def call_compliance_checker():
    '''

    :return:
    '''
    client_uuid = request.args.get('uuid')
    event = request.json
    event = json.loads(event)
    return complianceChecker.compliance_checker(client_uuid, event)


@app.route('/show-deviation-pdf', methods=['GET', 'POST'])
def call_show_deviation_pdf():
    client_uuid = request.args.get('uuid')
    deviationPDF.show_deviation_pdf(client_uuid)
    print(defaultConfig.BASE_DIR)
    try:
        automata_pdf = open(defaultConfig.AUTOMATA_FILE, 'rb')
        return send_file(automata_pdf, attachment_filename='file.pdf')
    except:
        print('exception')


# TODO: catch exceptions
buildAutomata.test_automata_status()


if __name__ == '__main__':
    app.debug = True
    app.run()



# TODO: 1. logging  2. exceptions handing  3. describe for service  4. CORS

