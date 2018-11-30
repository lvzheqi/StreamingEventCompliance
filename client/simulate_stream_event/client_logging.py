import logging
from simulate_stream_event import config


def client_logging(**kwargs):
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
