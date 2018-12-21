from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os, configparser, re
app = Flask(__name__)
from console_logging.console import Console
console = Console()
console.setVerbosity(5)

# Default Configuration:
DATABASE_PATH = 'mysql+pymysql://compliancechecker:compliancechecker@localhost/compliancechecker'
app.config['LOG_LEVEL'] = 'DEBUG'
app.config['LOG_FORMAT'] = '%(asctime)-15s %(message)s'
app.config['BASE_DIR'] = os.path.dirname(__file__) + os.sep + '..' + os.sep
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_PATH
app.config['AUTOS_DEFAULT'] = False
app.config['THRESHOLD'] = 0.2
app.config['AUTOMATA_FILE'] = 'automata'
app.config['CLEINT_DATA_PATH'] = app.config['BASE_DIR'] + 'p_automata' + os.sep
app.config['FILE_TYPE'] = '.pdf'
app.config['TRAINING_EVENT_LOG_PATH'] = app.config['BASE_DIR'] + 'data' + os.sep + \
                                        'Example_EventLogForTraining_Backup.xes'
app.config['WINDOW_SIZE'] = list(map(int, re.findall(r"\d+", '[1,2,3,4]')))
app.config['MAXIMUN_WINDOW_SIZE'] = max(app.config['WINDOW_SIZE'])
app.config['CHECKING_TYPE'] = 'KEEP_ALL_EVENTS'
app.config['SERVER_LOG_PATH'] = app.config['BASE_DIR'] + os.sep + 'data' + os.sep + 'server.log'
app.config['ALERT_TYPE'] = 'DELETE_M_EVENT'

config = configparser.ConfigParser()
app.config['CONFIG_PATH'] = app.config['BASE_DIR'] + 'config.ini'
config.read(app.config['CONFIG_PATH'])

# Checking config['USER-DEFINED']:
if config['USER-DEFINED'].get('TRAINING_EVENT_LOG_PATH') and config['USER-DEFINED']['TRAINING_EVENT_LOG_PATH'] is not None:

    app.config['TRAINING_EVENT_LOG_PATH'] = app.config['BASE_DIR'] + \
                                    config['USER-DEFINED']['TRAINING_EVENT_LOG_PATH'].replace('/', os.sep)

if config['USER-DEFINED'].get('WINDOW_SIZE') and config['USER-DEFINED']['WINDOW_SIZE'] is not None:
    app.config['WINDOW_SIZE'] = list(map(int, re.findall(r"\d+", config['USER-DEFINED']['WINDOW_SIZE'])))
    app.config['MAXIMUN_WINDOW_SIZE'] = max(app.config['WINDOW_SIZE'])

if config['USER-DEFINED'].get('THRESHOLD') and config['USER-DEFINED']['THRESHOLD'] is not None:
    app.config['THRESHOLD'] = float(config['USER-DEFINED']['THRESHOLD'])

if config['USER-DEFINED'].get('CHECKING_TYPE') and config['USER-DEFINED']['CHECKING_TYPE'] is not None:
    app.config['CHECKING_TYPE'] = config['USER-DEFINED']['CHECKING_TYPE']

if config['USER-DEFINED'].get('CHECKING_TYPE') and config['USER-DEFINED']['ALERT_TYPE'] is not None:
    app.config['ALERT_TYPE'] = config['USER-DEFINED']['ALERT_TYPE']

console.secure("PATH", app.config['TRAINING_EVENT_LOG_PATH'])

db = SQLAlchemy(app)


from streaming_event_compliance import routes
