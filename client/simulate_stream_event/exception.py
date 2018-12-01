import requests

class ConnectionException (Exception):
    message = 'ConnectionError: The server is not available, please try it later!'
    def __init__(self):
        super().__init__(self)



class ReadFileException (Exception):
    message = "ReadFileError: The input file doesn't exist or is empty!"
    def __init__(self, path):
        self.path = path
