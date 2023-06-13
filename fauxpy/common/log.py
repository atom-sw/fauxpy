import logging
from . import file

Logger = logging.getLogger()


def init():
    global logging
    logFilePath = file.getLogFilePath()
    logging.basicConfig(filename=logFilePath,
                        format='%(asctime)s %(message)s',
                        filemode='w')

# def seeTheLogFile():
#     return f"\n>>>>>>>See the log file in {logFilePath}.<<<<<<<\n"
