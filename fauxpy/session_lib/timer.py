import time

class Timer(object):
    """A simple timer class to measure elapsed time."""

    def __init__(self):
        """Initializes the Timer with a starting time of zero."""
        self._starting_time = 0

    def start(self):
        """Starts the timer by recording the current time."""
        self._starting_time = time.time()

    def end(self) -> float:
        """Ends the timer and returns the elapsed time.

        Returns:
            float: The number of seconds elapsed since the timer was started.
        """
        ending_time = time.time()
        return ending_time - self._starting_time
