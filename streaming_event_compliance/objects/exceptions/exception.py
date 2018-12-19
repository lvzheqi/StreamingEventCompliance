class MyException(Exception):
    def __init__(self, message):
        super().__init__(self)
        self.message = message

    def get_message(self):
        print(self.message)


class EventException(MyException):
    def __init__(self, event):
        mess = 'ServerRequestError: Server Error! ' + str(event)
        super().__init__(mess)


class NoUserException(MyException):
    def __init__(self):
        mess = 'NoUserError: No user exist!'
        super().__init__(mess)


class ReadFileException(MyException):
    def __init__(self, path):
        mess = "ReadFileError: The input path '" + path + "' does not exist or is empty!"
        super().__init__(mess)


class ThreadException(MyException):
    def __init__(self, info):
        self.exception = info
        self.mess = 'ThreadError' + " " + str(self.exception)
        super().__init__(self.mess)

    def __str__(self):
        s = str(self.exception)
        return s