import time


class Timer(object):
    def __init__(self):
        self._startingTime = 0

    def start_timer(self):
        self._startingTime = time.time()

    def end_timer(self):
        ending_time = time.time()
        return ending_time - self._startingTime
