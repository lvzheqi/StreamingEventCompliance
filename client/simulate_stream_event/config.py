import os

#The base directory of the project is defined in this variable
BASE_DIR = os.path.dirname(__file__) + os.sep + '..' + os.sep + '..'

#Client log file is available in this path
CLIENT_LOG_PATH = BASE_DIR + os.sep + 'client' + os.sep + 'client_log.log'

#Logging level can be changed to INFO, WARNING, ERROR, CRITICAL .Default is  set to DEBUG
LOG_LEVEL = 'DEBUG'

#This variable is used to set format of the log message.
LOG_FORMAT = '%(asctime)-15s %(message)s'

