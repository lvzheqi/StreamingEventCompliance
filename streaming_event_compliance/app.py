from flask import Flask, request, send_file
from flask_api import status
from streaming_event_compliance.services import compliance_checker, build_automata
from streaming_event_compliance.services import deviation_pdf
from streaming_event_compliance.utils import config, dbtools
from streaming_event_compliance.utils.dbtools import db
from streaming_event_compliance.objects.automata.alertlog import db as alogdb
from streaming_event_compliance.objects.automata.automata import db as autodb
from test import objects_test
import os
import json


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = config.BASE_DIR
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_PATH


app.app_context().push()
autodb.init_app(app)
db.init_app(app)
alogdb.init_app(app)



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


autos = build_automata.get_automata()


# TODO: catch exceptions

# --------------------------- init database --------------------------
dbtools.init_database()

# ----------------------------- test --------------------------------
# print(automataclass_test.test_automata())
# automataclass_test.test_alertlog()
dbtools.empty_tables()
autos = objects_test.test_automata()
print(autos)
dbtools.insert_node_and_connection(autos)
autoss = dbtools.init_automata()
print(autoss)
dbtools.create_user('u1')
# dbtools.create_user('u1')
# dbtools.update_user('u1',True)
alogs = objects_test.test_alertlog('u1', autos)
print(alogs)
dbtools.insert_alert_log(alogs)
dbtools.init_alert_log('u1', autos)
alogss = dbtools.init_alert_log('u1', autos)
print(alogss)


if __name__ == '__main__':
    app.debug = True
    app.run()



# TODO: 1. logging  2. exceptions handing  3. describe for service  4. CORS

