from console_logging.console import Console

console = Console()
console.setVerbosity(5)


class MyException(Exception):
    def __init__(self, message):
        super().__init__(self)
        self.message = message

    def get_message(self):
        console.error(self.message)


class EventException(MyException):
    def __init__(self, event):
        mess = 'ServerRequestError: Server Error! ' + str(event)
        super().__init__(mess)


class ReadFileException(MyException):
    def __init__(self, path, info):
        self.exception = info
        mess = "ReadFileError: The input path '" + path + "' does not " \
                                                          "exist or in wrong form!" + "\n" + str(self.exception)
        super().__init__(mess)


class ThreadException(MyException):
    def __init__(self, info):
        self.exception = info
        self.mess = 'ThreadError' + " " + str(self.exception)
        super().__init__(self.mess)

    def __str__(self):
        s = str(self.exception)
        return s
