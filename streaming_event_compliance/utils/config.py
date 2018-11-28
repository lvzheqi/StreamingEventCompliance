import os

DATABASE_PATH = 'mysql+pymysql://compliancechecker:compliancechecker@localhost/compliancechecker'

AUTOMATA_FILE = 'automata.pdf'
BASE_DIR = os.path.dirname(__file__) + os.sep + '..' + os.sep + '..' + os.sep
WINDOW_SIZE = [1, 2, 3, 4]


TRAINING_EVENT_LOG_PATH = BASE_DIR + 'data' + os.sep + '/Example_EventLogForTraining.xes'
AUTOS_DEFAULT = False
MAXIMUN_WINDOW_SIZE = 4

