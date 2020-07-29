#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Provide routines to Tweet strings to Twitter.

TODO
    Create OOP implementation. example: obj/my_account  methods: tweet,init,status(last tweet and time of tweet)
"""

from loguru import logger
from twython import Twython, TwythonError
# from Credentials import TWITTER_CREDENTIALS

# unpack the credentials before submitting to Twython
# a, b, c, d = TWITTER_CREDENTIALS
# establish the twitter access object
# twitter_access = Twython(a, b, c, d)

PupDB_MRTkey = 'Most_Recent_Tweet'


@logger.catch
def store_tweet(credentials_hash, tweet):
    """Args:
        credentials_hash (string): [unique string for any twitter account]
        tweet ([string]): [the actual text of tweet]

    Returns:
        [bool]: [success or failure]
    """


@logger.catch
def send_tweet(tweet, TWITTER_CREDENTIALS):
    """Accept a database object, datetime object, a tweet string and a Twython object. 
    Place tweet and update filesystem storage to reflect activities.
    """
    # unpack the credentials before submitting to Twython
    a, b, c, d = TWITTER_CREDENTIALS
    # establish the twitter access object
    twitter_access = Twython(a, b, c, d)   
    try:
        twitter_access.update_status(status=tweet)
    except TwythonError as e:
        logger.error(str(e))
        logger.info("Tweet not sent.")
    else:
        logger.info("Tweet sent.")
    finally:
        logger.debug("Tweet string = " + str(tweet))
        logger.info("Length of string = " + str(len(tweet)))
        account_hash = hash(TWITTER_CREDENTIALS)
        store_tweet(account_hash, tweet)

    return True
