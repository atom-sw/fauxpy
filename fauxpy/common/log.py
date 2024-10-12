import logging
from pathlib import Path

Logger = logging.getLogger()


def init(log_file_path: Path):
    global logging
    logging.basicConfig(
        filename=log_file_path, format="%(asctime)s %(message)s", filemode="w"
    )


# def seeTheLogFile():
#     return f"\n>>>>>>>See the log file in {logFilePath}.<<<<<<<\n"
