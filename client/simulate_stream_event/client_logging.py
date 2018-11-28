import logging
from . import config


def client_logging(**kwargs):
    """
        This function does formatting for messages before sending it to the logging system.

        This function takes all the arguments provided by the user and formats
        the 'message' variable accordingly. This message is further sent to basic
        configuration function in the 'format' variable

        The logs are broadly classified into two types.
        1.  For each activity the below details will be logged
        timestamp, message type(error,info), username, function name, message
        2. For some activities that involve thread and events,case_id,
        thread_id and its activity shall also be logged

        Format of the log file is
        'timestamp message_type username func_name message'
        message is again formatted as
        'thread_id:  case_id: activity: message'

        A number of optional keyword arguments may be specified, which can alter
        the default behaviour.

        filename        Specifies the file name where the content will be logged.
                        Default value:/client/client_log.log
        filemode        Specifies the mode to open the file, if filename is specified
                        (if filemode is unspecified, it defaults to 'a').
        message         User defined custom messages
                        Default value: ''
        username        It is the username of the user that has initiated the client
                        Default value :'Username:Unknown'
        func_name       This is the name of the function from where this logging event
                        was called.
                        Default value: 'Func:Unknown'
        level           Set the root logger level to the specified level. It can be
                        DEBUG, INFO, WARNING, ERROR, CRITICAL.
                        Default value: 'DEBUG'
        message_type    It implies if the message is an error or information. It can be
                        either 'INFO' or 'ERROR'
                        Default value: 'INFO"
        case_id         This is the case id of  the event being processed.
                        Default value: ''
        activity        This is the activity of the event being processed.
                        Default value: None
        thread_id       If specified, this  would be thread id of the thread handling the
                        event with case_id and activity same as mentioned above
                        Default value: None
    """
    log_format = '%(asctime)-15s %(message)s'
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
        message = "Thread:" + thread_id + ' ' + "Case_id:" + case_id + ' ' + "Activity:" + activity + ' ' + message
    message = message_type + ' ' + username + ' ' + func_name + ' ' + message
    level = kwargs.pop("level", "DEBUG")
    filemode = kwargs.pop("filemode", "a")
    logging.basicConfig(filename=filename, filemode=filemode, level=level, format=log_format)
    if message_type == 'ERROR':
        logging.error(message)
    elif message_type == 'INFO':
        logging.info(message)
