from logging import getLogger, NullHandler, DEBUG, Handler
from typing import Union


def get_logger(name, handler: Handler = None, level: Union[int, str] = DEBUG):
    logger = getLogger(name)
    logger.setLevel(level)
    if handler is None:
        handler = NullHandler(level)
    logger.addHandler(handler)
    logger.propagate = False
    return logger
