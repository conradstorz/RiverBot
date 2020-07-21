#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Define logging parameters
"""

from loguru import logger

@logger.catch
def defineLoggers():
    """Set options for logging.
    """
    logger.add(
        sys.stderr,
        colorize=True,
        format="<green>{time}</green> {level} <red>{message}</red>",
        level=LOGGING_LEVEL,
    )
    logger.add(  # create a new log file for each run of the program
        "./LOGS/" + RUNTIME_NAME + "_{time}.log",
        retention="10 days",
        compression="zip",
        level="DEBUG",  # always send debug output to file
    )
    logger.add(  # create a log file for each run of the program
        "./LOGS/" + RUNTIME_NAME + ".log",
        retention="10 days",
        compression="zip",
        level="DEBUG",  # always send debug output to file
    )
    return
