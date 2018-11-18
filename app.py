from flask import Flask, request, Response, make_response
from services import complianceChecker, deviationPDF, buildAutomata
import json



app = Flask(__name__)


@app.route('/compliance-checker', methods=['POST'])
def call_compliance_checker():
    client_uuid = request.args.get('uuid')
    event = request.json
    event = json.loads(event)
    return complianceChecker.compliance_checker(client_uuid, event)


@app.route('/show-deviation-pdf', methods=['GET'])
def call_show_deviation_pdf():
    client_uuid = request.args.get('uuid')
    deviationPDF.show_deviation_pdf(client_uuid)
    # What happened if the pdf is missing

# TODO: catch exceptions


if __name__ == '__main__':
    app.run()



# TODO: 1. logging  2. exceptions handing  3. describe for service  4. CORS

