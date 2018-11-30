class ConnectionException (Exception):
    pass


class ReadFileException (Exception):
    message = "ReadFileException: The input file does not exist! You need to exit!"
    # TODO: Here can be improved, don't need to exit,just give a correct file path
    def __init__(self, path):
        self.path = path
