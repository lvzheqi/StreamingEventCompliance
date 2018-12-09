import os

DATABASE_PATH = 'mysql+pymysql://compliancechecker:compliancechecker@localhost/compliancechecker'

AUTOMATA_FILE = 'automata.pdf'
BASE_DIR = os.path.dirname(__file__) + os.sep + '..' + os.sep + '..' + os.sep
WINDOW_SIZE = [1, 2, 3, 4]


TRAINING_EVENT_LOG_PATH = BASE_DIR + 'data' + os.sep + 'Example_EventLogForTraining.xes'
AUTOS_DEFAULT = False
MAXIMUN_WINDOW_SIZE = 4
THRESHOLD = 0.00


SERVER_LOG_PATH = BASE_DIR + os.sep + 'data' + os.sep + '/server.log'

LOG_LEVEL = 'DEBUG'

LOG_FORMAT = '%(asctime)-15s %(message)s'

