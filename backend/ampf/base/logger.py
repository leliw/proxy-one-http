import logging


CRITICAL = logging.CRITICAL
FATAL = logging.FATAL
ERROR = logging.ERROR
WARNING = logging.WARNING
WARN = logging.WARN
INFO = logging.INFO
DEBUG = logging.DEBUG
NOTSET = logging.NOTSET


def get_logger(logger_name: str) -> logging.Logger:
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    # Konsola
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)  # Ustawienie poziomu logowania na konsoli
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # Plik
    fh = logging.FileHandler("session.log")
    fh.setLevel(logging.DEBUG)  # Ustawienie poziomu logowania do pliku
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger
