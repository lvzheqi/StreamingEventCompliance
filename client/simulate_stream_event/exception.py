from console_logging.console import Console
console = Console()
console.setVerbosity(5)


class MyException(Exception):
    '''
    This is the exception class and rest of the exception classes are inherited from this.
    '''
    def __init__(self, message):
        super().__init__(self)
        self.message = message

    def get_message(self):
        '''
        This function prints the message to console
        '''
        console.error(self.message)


class ConnectionException(MyException):
    '''
    This exception is raised when client not able to connect to server.
    '''
    def __init__(self):
        mess = 'ConnectionError: The server is not available, please try it later!'
        super().__init__(mess)


class ServerRequestException(MyException):
    '''
    This exception is raised when client is requesting server.
    '''
    def __init__(self, text):
        mess = 'ServerRequestError: Server Error! ' + text
        super().__init__(mess)


class ReadFileException(MyException):
    '''
    This exception is raised when testing or training file is cannot be read when path is not reachable
    '''
    def __init__(self, path):
        mess = "ReadFileError: The input path '" + path + "' does not exist or is empty!"
        super().__init__(mess)


class ThreadException(MyException):
    '''
    This exception is raised when thread fails due to some error.
    '''
    def __init__(self, info):
        self.exception = info
        self.mess = 'ThreadError' + " " + str(self.exception)
        super().__init__(self.mess)

    def __str__(self):
        s = str(self.exception)
        return s
