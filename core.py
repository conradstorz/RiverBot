#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""River monitor bot program.

# import needed routines

# import settings (twitter credentials, database details)

# declare logging parameters

# start loop

    # check river database
    # tweet status if needed and
    # update tweet database
    # update any local display devices

"""
# used to standardize string formats across modules
from time_strings import CURRENT_YEAR, TODAY_STRING, NOW_STRING

from RiverGuages import *
from NWS_WebScrape import Scrape_NWS_site
from core_logging_setup import defineLoggers
from Credentials import TWITTER_CREDENTIALS

from pathlib import Path
from loguru import logger
from pupdb.core import PupDB
from datetime import datetime

RUNTIME_NAME = Path(__file__).name

logger.remove()  # stop any default logger
LOGGING_LEVEL = "INFO"


@logger.catch
def Main(credentials):
    """Main loop. Run eternally.
    """
    defineLoggers()
    storage_db = PupDB(PupDB_FILENAME)    # activate PupDB file for persistent storage
    last_tweet = storage_db.get(PupDB_MRTkey)
    last_level = storage_db.get(PupDB_MRLkey)
    if last_tweet is None:  # Pre-load empty database
        last_tweet = str(NOW_STRING)
        last_level = MINIMUM_CONCERN_LEVEL
        storage_db.set(PupDB_MRTkey, last_tweet)
        storage_db.set(PupDB_MRLkey, last_level)
        forecast_level = last_level
        storage_db.set(PupDB_MRFkey, forecast_level)
    # initialization complete. Begin main loop. 
        # check river database
        # tweet status if needed and
        # update tweet database
        # update any local display devices      
    return False # should never end


if __name__ == "__main__":
    Main(TWITTER_CREDENTIALS)





"""Old code...
from os import sys, path
from time import time, sleep
from datetime import datetime
from loguru import logger
from pupdb.core import PupDB
from Credentials import TWITTER_CREDENTIALS
from LED_displays import DisplayMessage

RUNTIME_NAME = path.basename(__file__)

logger.remove()  # stop any default logger
LOGGING_LEVEL = "INFO"

@logger.catch
def Main(credentials):
    defineLoggers()
    # activate PupDB file for persistent storage
    TimeNow = datetime.now()
    storage_db = PupDB(PupDB_FILENAME)
    last_tweet = storage_db.get(PupDB_MRTkey)
    last_level = storage_db.get(PupDB_MRLkey)
    if last_tweet is None:  # Pre-load empty database
        last_tweet = str(TimeNow)
        last_level = MINIMUM_CONCERN_LEVEL
        storage_db.set(PupDB_MRTkey, last_tweet)
        storage_db.set(PupDB_MRLkey, last_level)
        forecast_level = last_level
        storage_db.set(PupDB_MRFkey, forecast_level)
    # initialization complete. Begin main loop.
    while True:
        TimeNow = datetime.now()
        wait, new_level = UpdatePrediction(twitter, TimeNow, storage_db)
        forecast_level = storage_db.get(PupDB_MRFkey)
        trend = DetermineTrend(new_level, forecast_level)
        print(f"New wait time: {wait}")
        print(f"New Level: {new_level}")
        print(f"Trend: {trend}")
        while wait > 0:
            startDisplay = int(time())
            sleep(1)  # guarantee at least a one second pause
            if (
                startDisplay % 10
            ) == 0:  # update external displays connected to server each ten seconds.
                print(".", end="", flush=True)
                DisplayMessage(
                    f"  {new_level:.2f}ft Latest. Trend: {trend}   Now {new_level:.2f}ft   Trend: {trend}"
                )
            if (
                startDisplay % 50
            ) == 0:  # every 50 seconds send a progress indication to attached display.
                print("")
                print(f"Wait time remaining: {wait}")
            endDisplay = int(time())
            elapsed = endDisplay - startDisplay
            print(f"{elapsed}.", end="", flush=True)
            wait = wait - elapsed
    return


@logger.catch
def defineLoggers():
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


if __name__ == "__main__":
    Main(TWITTER_CREDENTIALS)
"""