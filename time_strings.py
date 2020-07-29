#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Standardize time strings and datetime objects used in a project.
"""


from datetime import datetime, date
from time import sleep
import pytz


tz_UTC = pytz.timezone("UTC")
tz_LOCAL = pytz.timezone("America/Louisville")


def timefstring(dtobj):
    """Standardize the format used for timestamp string format.
    """
    return f'{dtobj.strftime("%Y-%m-%d_%H:%M:%S")}UTC'


LOCAL_TODAY = date.today()
UTC_NOW = datetime.now(tz_UTC)
LOCAL_CURRENT_YEAR = str(LOCAL_TODAY.year)
LOCAL_TODAY_STRING = LOCAL_TODAY.strftime("%Y-%m-%d")
UTC_NOW_STRING = timefstring(UTC_NOW)
LOCAL_NOW = datetime.now(tz_LOCAL)
LOCAL_NOW_STRING = timefstring(LOCAL_NOW)


if __name__ == "__main__":
    for i in range(5):
        print(f"LOCAL TODAY: {LOCAL_TODAY} type: {type(LOCAL_TODAY)}")
        print(f"UTC NOW: {UTC_NOW} type: {type(UTC_NOW)}")
        print(f"LOCAL NOW: {LOCAL_NOW} type: {type(LOCAL_NOW)}")
        print(f"LOCAL CURRENT_YEAR: {LOCAL_CURRENT_YEAR} type: {type(LOCAL_CURRENT_YEAR)}")
        print(f"LOCAL TODAY_STRING: {LOCAL_TODAY_STRING} type: {type(LOCAL_TODAY_STRING)}")
        print(f"UTC NOW_STRING: {UTC_NOW_STRING} type: {type(UTC_NOW_STRING)}")
        print(f"LOCAL NOW_STRING: {LOCAL_TODAY_STRING} type: {type(LOCAL_TODAY_STRING)}")
        sleep(2)
        print()

