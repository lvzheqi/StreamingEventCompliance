import os


BASE_DIR = os.path.dirname(__file__) + os.sep + '..' + os.sep + '..' + os.sep

CLIENT_LOG_PATH = BASE_DIR + os.sep + 'client' + os.sep + '/client_log.log'

LOG_LEVEL = 'DEBUG'

LOG_FORMAT = '%(asctime)-15s %(message)s'

