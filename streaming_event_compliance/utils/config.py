import os

DATABASE_PATH = 'mysql+pymysql://compliancechecker:compliancechecker@localhost/compliancechecker'

AUTOMATA_FILE = 'automata.pdf'

WINDOW_SIZE = [1, 2, 3, 4]
MAXIMUN_WINDOW_SIZE = 4

BASE_DIR = os.path.dirname(__file__) + os.sep + '..' + os.sep + '..' + os.sep
TRAINING_EVENT_LOG_PATH = BASE_DIR + 'data' + os.sep + 'Example_EventLogForTraining.xes'
# TRAINING_EVENT_LOG_PATH = BASE_DIR + 'data' + os.sep + 'Example_EventLogForTraining_Backup.xes'
# TRAINING_EVENT_LOG_PATH = BASE_DIR + 'data' + os.sep + 'A21.xes'
# TRAINING_EVENT_LOG_PATH = BASE_DIR + 'data' + os.sep + 'A1.xes'
# TRAINING_EVENT_LOG_PATH = BASE_DIR + 'data' + os.sep + 'A4.xes'
# TRAINING_EVENT_LOG_PATH = BASE_DIR + 'data' + os.sep + 'A2.xes'
SERVER_LOG_PATH = BASE_DIR + os.sep + 'data' + os.sep + 'server.log'

AUTOS_DEFAULT = False
THRESHOLD = 0.00

LOG_LEVEL = 'DEBUG'
LOG_FORMAT = '%(asctime)-15s %(message)s'

