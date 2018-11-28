import logging
import sys


def client_logging(**kwargs):
    log_format = '%(asctime)-15s %(message_type)s %(func_name)s %(username)s %(message)s'
    func_name = kwargs.pop("func_name", "Func:Unknown")
    print("Func_name is " + func_name)
    filename = kwargs.pop("filename", "client.log")
    print("Filename is " + filename)
    message = kwargs.pop("message", "")
    print("Message is " + message)
    thread_id = kwargs.pop("thread_id", None)
    case_id = kwargs.pop("case_id", None)
    activity = kwargs.pop("activity", None)
    if thread_id is None and case_id is None and activity is None:
        message = message
    elif thread_id is not None and case_id is not None and activity is not None:
        message = "Thread:" + thread_id + ' ' + "Case_id:" + case_id + ' ' + "Activity:" + activity + ' - ' + message
    elif thread_id is not None and case_id is None:
        message = "Thread:" + thread_id + " Case_id:Unknown" + ' - ' + message
    elif thread_id is None and case_id is not None:
        message = "Thread:Unknown" + ' ' + "Case_id:" + case_id + ' ' + "Activity:" + activity + ' - ' + message
    message_type = kwargs.pop("message_type", "INFO")
    print("Message_type is " + message_type)
    username = kwargs.pop("username", "Username:Unknown")
    print("Username is " + username)
    details = {
           'username': username,
           'func_name': func_name,
           'message_type': message_type,
    }
    level = kwargs.pop("level", "DEBUG")
    print("level is " + level)
    logging.basicConfig(filename=filename, level=level, format=log_format)
    if message_type == 'ERROR':
        logging.error(message, extra=details)
    elif message_type == 'INFO':
        logging.info(message, extra=details)


def my_function():
    func_name = sys._getframe().f_code.co_name
    client_logging(message="All good", message_type="ERROR", level="INFO", func_name=func_name)


my_function()