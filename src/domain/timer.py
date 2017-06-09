import datetime

class Timer(object):
    def __init__(self):
        self.start_time: None

    def start(self):
        self.start_time = datetime.datetime.now()
        return self.start_time

    def elapsed(self):
        return (datetime.datetime.now() - self.start_time).total_seconds()