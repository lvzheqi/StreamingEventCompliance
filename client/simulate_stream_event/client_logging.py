import logging
from simulate_stream_event import config


def log_info(**kwargs):
    '''
    This function does the  formatting for 'info' messages before sending it to the logging system.

    This function takes all the arguments provided by the user and formats
    the 'message' variable accordingly. This message is further sent to basic
    configuration function in the 'format' variable

    The logs are broadly classified into two types.
    1.  For each activity the below details will be logged
    timestamp, message type(error,info),username, function name, message
    2. For some activities that involve thread and events,we shall also log
    case_id, thread_id and its activity

    Format of the log file is
    'timestamp message_type username func_name message'
    message is again formatted as
    'thread_id:  case_id: activity: message'


    :param kwargs:
    username:       It is the username of the user that has initiated the client
                    Default value: Username:Unknown
    func_name:      This is the name of the function from where this logging event was called.
                    Default value: Func:Unknown
    filename:       Specifies the file name where the content will be logged
                    Default value: client/client_log.log
    filemode:       Specifies the mode to open the file
                    Default value: a
    level:          Set the root logger level to the specified level. It can be
                    DEBUG, INFO, WARNING, ERROR, CRITICAL.
                    Default value: DEBUG
    message:        User defined custom messages
                    Default value: ''
    message_type:   It implies if the message is an error or information.
                    It can be either 'INFO' or 'ERROR'
                    Default value: INFO
    case_id:        This is the case id of  the event being processed.
                    Default value: ''
    activity:



    '''
    func_name = kwargs.pop("func_name", "Func:Unknown")
    filename = kwargs.pop("filename", config.CLIENT_LOG_PATH)
    message = kwargs.pop("message", "")
    thread_id = kwargs.pop("thread_id", None)
    case_id = kwargs.pop("case_id", '')
    activity = kwargs.pop("activity", None)
    message_type = kwargs.pop("message_type", "INFO")
    username = kwargs.pop("username", "Username:Unknown")
    message = "'" + message + "'"
    if case_id != '' and thread_id is None:
        message = "Case_id:" + case_id + ' ' + "Activity:" + activity + ' ' + message
    elif thread_id is not None:
        message = "Thread:" + str(thread_id) + ' ' + "Case_id:" + case_id + ' ' + "Activity:" + activity + ' ' + message
    message = message_type + ' ' + username + ' ' + func_name + ' ' + message
    level = kwargs.pop("level", config.LOG_LEVEL)
    filemode = kwargs.pop("filemode", "a")
    logging.basicConfig(filename=filename, filemode=filemode, level=level, format=config.LOG_FORMAT)
    logging.info(message)


def log_error(**kwargs):
    func_name = kwargs.pop("func_name", "Func:Unknown")
    filename = kwargs.pop("filename", config.CLIENT_LOG_PATH)
    message = kwargs.pop("message", "")
    thread_id = kwargs.pop("thread_id", None)
    case_id = kwargs.pop("case_id", '')
    activity = kwargs.pop("activity", None)
    message_type = kwargs.pop("message_type", "INFO")
    username = kwargs.pop("username", "Username:Unknown")
    message = "'" + message + "'"
    if case_id != '' and thread_id is None:
        message = "Case_id:" + case_id + ' ' + "Activity:" + activity + ' ' + message
    elif thread_id is not None:
        message = "Thread:" + str(thread_id) + ' ' + "Case_id:" + case_id + ' ' + "Activity:" + activity + ' ' + message
    message = message_type + ' ' + username + ' ' + func_name + ' ' + message
    level = kwargs.pop("level", config.LOG_LEVEL)
    filemode = kwargs.pop("filemode", "a")
    logging.basicConfig(filename=filename, filemode=filemode, level=level, format=config.LOG_FORMAT)
    logging.error(message)
