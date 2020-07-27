#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Standardize time strings and datetime objects used in project.
"""


from datetime import datetime, date
import pytz


tz_UTC = pytz.timezone("UTC")
tz_LOCAL = pytz.timezone('America/Louisville')


def timefstring(dtobj):
    return f'{dtobj.strftime("%Y-%m-%d_%H:%M:%S")}UTC'


LOCAL_TODAY = date.today()
NOW_UTC = datetime.now(tz_UTC)
LOCAL_CURRENT_YEAR = str(LOCAL_TODAY.year)
TODAY_LOCAL_STRING = LOCAL_TODAY.strftime("%Y-%m-%d")
NOW_UTC_STRING = timefstring(NOW_UTC)
NOW_LOCAL = datetime.now(tz_LOCAL)

if __name__ == "__main__":
    print(f"LOCAL TODAY: {LOCAL_TODAY} type: {type(LOCAL_TODAY)}")
    print(f"UTC NOW: {NOW_UTC} type: {type(NOW_UTC)}")
    print(f"LOCAL NOW: {NOW_LOCAL} type: {type(NOW_LOCAL)}")
    print(f"LOCAL CURRENT_YEAR: {LOCAL_CURRENT_YEAR} type: {type(LOCAL_CURRENT_YEAR)}")
    print(f"LOCAL TODAY_STRING: {TODAY_LOCAL_STRING} type: {type(TODAY_LOCAL_STRING)}")
    print(f"UTC NOW_STRING: {NOW_UTC_STRING} type: {type(NOW_UTC_STRING)}")
