import logging
from streaming_event_compliance import app
from pythonlangutil.overload import Overload, signature
import os


class ServerLogging:
    """
    Description:
        This class does the  formatting  of server side log  before sending it to the logging system.

        This class takes different arguments provided by the user and formats
        the 'message' variable accordingly. This message is further sent to basic
        configuration function in the 'format' variable

        The logs are broadly classified into two types.
        1.  For each activity the below details will be logged
        timestamp, message type(error,info),username, function name, message
        2. For some activities that involve thread and events,we shall also log
        case_id, thread_id and its activity

        Format of the log file is
        'timestamp message_type username func_name message'
        message is again formatted as below if  thread_id, case_id and activity_id is sent
        'thread_id:  case_id: activity: message'

        All the below functions do the same tasks but with different number of variables

    Instance Variables:
    filename: :`String` specifies the file name where the content will be logged
                Default value: client/client_log.log
    filemode: : Specifies the mode to open the file
                Default value: a
    level: :Set the root logger level to the specified level. It can be
                DEBUG, INFO, WARNING, ERROR, CRITICAL.
                Default value: DEBUG
    log_format: It is the format in which the time and message will be stored.
    """
    def __init__(self):
        self.filename = app.config['SERVER_LOG_PATH']
        if not os.path.exists(self.filename):
            with open(self.filename, 'w'):
                pass

        self.level = app.config['LOG_LEVEL']
        self.log_format = app.config['LOG_FORMAT']
        self.filemode = 'a'

    @Overload
    @signature('str', 'str')
    def log_info(self, func_name, message):
        """
        Description:
            This function is used to log info messages
            Format of logged data:
            <timestamp> INFO Username:Unknown <func_name>  <message>

        :param func_name::str: This is the name of the function from where this logging event was called.
        :param message::str: User defined custom messages
        """
        message = "'" + message + "'"
        message = ' INFO ' + 'Username:Unknown ' + func_name + ' ' + message
        logging.basicConfig(filename=self.filename, filemode=self.filemode, level=self.level, format=self.log_format)
        logging.info(message)

    @log_info.overload
    @signature('str', 'str', 'str')
    def log_info(self, func_name, username, message):
        """
        Description:
            This function is used to log info messages
            Format of logged data:
            <timestamp> INFO <username> <func_name>  <message>

        :param  func_name: :`String` This is the name of the function from where this logging event was called.
        :param  username: :`String` It is the username of the user that has initiated the client
        :param  message: :`String` User defined custom messages
        """
        message = "'" + message + "'"
        message = ' INFO ' + username + ' ' + func_name + ' ' + message
        logging.basicConfig(filename=self.filename, filemode=self.filemode, level=self.level, format=self.log_format)
        logging.info(message)

    @log_info.overload
    @signature('str', 'str', 'str', 'str', 'str')
    def log_info(self, func_name, username, case_id, activity, message):
        """
        Description:
            This function is used to log info messages
            Format of logged data:
            <timestamp> INFO <username> <func_name> <case_id> <activity> <<message>

        :param func_name: :`String` This is the name of the function from where this logging event was called.
        :param username: :`String` It is the username of the user that has initiated the client
        :param case_id: :`String` This is the case id of  the event being processed.
        :param activity: :`String` This is the activity of the event being processed.
        :param message: :`String`  User defined custom messages
        """
        message = "'" + message + "'"
        message = 'Case_id:' + case_id + ' ' + 'Activity:' + activity + ' ' + message
        message = ' INFO ' + username + ' ' + func_name + ' ' + message
        logging.basicConfig(filename=self.filename, filemode=self.filemode, level=self.level, format=self.log_format)
        logging.info(message)

    @log_info.overload
    @signature('str', 'str', 'str', 'str')
    def log_info(self, func_name, username, case_id, message):
        """
        Description:
            This function is used to log info messages
            Format of logged data:
            <timestamp> INFO <username> <func_name> <case_id> <activity> <<message>

        :param func_name: :`string` This is the name of the function from where this logging event was called.
        :param username: :`string` It is the username of the user that has initiated the client
        :param thread_id::int: Id of the thread handling the event
        :param case_id: :`string` This is the case id of  the event being processed.
        :param activity: :`string` This is the activity of the event being processed.
        :param message: :`string` User defined custom messages
        """
        message = "'" + message + "'"
        message = 'Case_id:' + case_id + ' ' + message
        message = ' INFO ' + username + ' ' + func_name + ' ' + message
        logging.basicConfig(filename=self.filename, filemode=self.filemode, level=self.level, format=self.log_format)
        logging.info(message)

    @log_info.overload
    @signature('str', 'str', 'int', 'str', 'str')
    def log_info(self, func_name, username, case_id, activity, message):
        """
        Description:
            This function is used to log info messages
            Format of logged data:
            <timestamp> INFO <username> <func_name> <case_id> <activity> <<message>

        :param func_name: :`string` This is the name of the function from where this logging event was called.
        :param username: :`string` It is the username of the user that has initiated the client
        :param thread_id::int: Id of the thread handling the event
        :param case_id: :`string` This is the case id of  the event being processed.
        :param activity: :`string` This is the activity of the event being processed.
        :param message: :`string` User defined custom messages
        """
        message = "'" + message + "'"
        message = 'Case_id:' + case_id + ' ' + 'Activity:' + activity + ' ' + message
        message = ' INFO ' + username + ' ' + func_name + ' ' + message
        logging.basicConfig(filename=self.filename, filemode=self.filemode, level=self.level, format=self.log_format)
        logging.info(message)

    @log_info.overload
    @signature('str', 'str', 'int',  'str', 'str', 'str')
    def log_info(self, func_name, username, thread_id, case_id, activity, message):
        """
        Description:
            This function is used to log info messages
            Format of logged data:
            <timestamp> INFO <username> <func_name> <case_id> <activity> <<message>

        :param func_name: :`string` This is the name of the function from where this logging event was called.
        :param username: :`string` It is the username of the user that has initiated the client
        :param thread_id::int: Id of the thread handling the event
        :param case_id: :`string` This is the case id of  the event being processed.
        :param activity: :`string` This is the activity of the event being processed.
        :param message: :`string` User defined custom messages
        """
        message = "'" + message + "'"
        message = 'Thread:' + str(thread_id) + ' ' + 'Case_id:' + case_id + ' ' + 'Activity:' + activity + ' ' + message
        message = ' INFO ' + username + ' ' + func_name + ' ' + message
        logging.basicConfig(filename=self.filename, filemode=self.filemode, level=self.level, format=self.log_format)
        logging.info(message)

    @Overload
    @signature('str', 'str')
    def log_error(self, func_name, message):
        """
        Description:
            This function is used to log info messages
            Format of logged data:
            <timestamp> ERROR Username:Unknown <func_name>  <message>

        :param func_name: :`string` This is the name of the function from where this logging event was called.
        :param message: :`string` User defined custom messages
        """
        message = "'" + message + "'"
        message = ' ERROR ' + 'Username:Unknown ' + func_name + ' ' + message
        logging.basicConfig(filename=self.filename, filemode=self.filemode, level=self.level, format=self.log_format)
        logging.error(message)

    @log_error.overload
    @signature('str', 'str', 'str')
    def log_error(self, func_name, username, message):
        """
        Desccription:
            This function is used to log info messages
            Format of logged data:
            <timestamp> ERROR <username> <func_name>  <message>

        :param  func_name: :`string` This is the name of the function from where this logging event was called.
        :param  username: :`string` It is the username of the user that has initiated the client
        :param  message: :`string` User defined custom messages
        """
        message = "'" + message + "'"
        message = ' ERROR ' + username + ' ' + func_name + ' ' + message
        logging.basicConfig(filename=self.filename, filemode=self.filemode, level=self.level, format=self.log_format)
        logging.error(message)

    @log_error.overload
    @signature('str', 'str', 'str', 'str', 'str')
    def log_error(self, func_name, username, case_id, activity, message):
        """
        Description:
            This function is used to log info messages
            Format of logged data:
            <timestamp> ERROR <username> <func_name> <case_id> <activity> <<message>

        :param func_name: :`string` This is the name of the function from where this logging event was called.
        :param username: :`string` It is the username of the user that has initiated the client
        :param case_id: :`string` This is the case id of  the event being processed.
        :param activity: :`string` This is the activity of the event being processed.
        :param message: :`string` User defined custom messages
        """
        message = "'" + message + "'"
        message = 'Case_id:' + case_id + ' ' + 'Activity:' + activity + ' ' + message
        message = ' ERROR ' + username + ' ' + func_name + ' ' + message
        logging.basicConfig(filename=self.filename, filemode=self.filemode, level=self.level, format=self.log_format)
        logging.error(message)

    @log_error.overload
    @signature('str', 'str', 'int', 'str', 'str', 'str')
    def log_error(self, func_name, username, thread_id, case_id, activity, message,):
        """
        Description:
            This function is used to log info messages
            Format of logged data:
            <timestamp> ERROR <username> <func_name> <case_id> <activity> <<message>

        :param func_name: :`string` This is the name of the function from where this logging event was called.
        :param username: :`string` It is the username of the user that has initiated the client
        :param thread_id::int: Id of the thread handling the event
        :param case_id: :`string` This is the case id of  the event being processed.
        :param activity: :`string` This is the activity of the event being processed.
        :param message: :`string` User defined custom messages
        """
        message = "'" + message + "'"
        message = 'Thread:' + str(thread_id) + ' ' + 'Case_id:' + case_id + ' ' + 'Activity:' + activity + ' ' + message
        message = ' ERROR ' + username + ' ' + func_name + ' ' + message
        logging.basicConfig(filename=self.filename, filemode=self.filemode, level=self.level, format=self.log_format)
        logging.error(message)



