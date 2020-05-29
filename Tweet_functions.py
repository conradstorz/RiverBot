#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Provide routines to Tweet strings to Twitter
"""

from loguru import logger
from twython import Twython, TwythonError
from Credentials import TWITTER_CREDENTIALS

# unpack the credentials before submitting to Twython
a, b, c, d = TWITTER_CREDENTIALS
# establish the twitter access object
twitter_access = Twython(a, b, c, d)

@logger.catch
def send_tweet(db, time, tweet, twttr):
    """Accept a database object, datetime object, a tweet string and a Twython object. 
    Place tweet and update filesystem storage to reflect activities.
    """

    try:
        twttr.update_status(status=tweet)
    except TwythonError as e:
        logger.error(str(e))
        logger.info("Tweet not sent.")
    else:
        logger.info("Tweet sent.")
    finally:
        logger.debug("Tweet string = " + str(tweet))
        logger.info("Length of string = " + str(len(tweet)))
        # place tweet time into longterm storage
        db.set(PupDB_MRTkey, str(time))
        # place tweet into longterm storage. Keep ALL tweets keyed on timestamp
        tweetKey = f"Tweet@{time}"
        db.set(tweetKey, tweet)
    return True
