
class FileNotFound(Exception):
    def __init__(self, file: str, msg: str = 'File \'{0}\' not found!'):
        self.file = file
        self.msg = msg.format(file)

    def __str__(self):
        return self.msg
