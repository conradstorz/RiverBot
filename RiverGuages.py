#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Declaration of CONSTANTS used by NWS_WebScrape.py
"""
PupDB_FILENAME = "SVTB-DB.json_db"
PupDB_MRTkey = "MostRecentTweet"
PupDB_MRLkey = "MostRecentRiverLevel"
PupDB_MRFkey = "MostRecentForecastLevel"
PupDB_ACTIONkey = "CurrentFloodingActionLevel"
HIGHEST_TAG = "Highest  Observation:"
LATEST_TAG = "Latest  observed"
FORECAST_TAG = "Highest  Forecast:"
OBSERVATION_TAGS = [LATEST_TAG, HIGHEST_TAG, FORECAST_TAG]

ACTION_LABELS = [
    "No Flooding",
    "First-action",
    "Minor-flood",
    "Moderate-flood",
    "Major-flood",
]
MINIMUM_CONCERN_LEVEL = 30
TWEET_FREQUENCY = [
    18000,
    9000,
    8000,
    7000,
    6000,
    5000,
    4000,
    3600,
]  # delay time in seconds
# Time between tweets decreases as flooding increases

# ACTION_LEVELS = [21, 23, 30, 38]
# ACTION_DICT = dict(zip(ACTION_LEVELS, ACTION_LABELS))
LOCATION_OF_INTEREST = 584  # river mile marker @ Bushman's Lake

NWS_website_baseaddress = (
    "https://water.weather.gov/"
    "/ahps2/river.php?wfo=lmk&wfoid=18699&"
    "riverid=204624&pt%5B%5D="
)
NWS_website_tailaddress = (
    "&pt%5B%5D=144523&allpoints=150960&data%5B%5D=obs&data%5B%5D=xml"
)
# river guage ID is inserted between these strings

NWS_OHIO_RIVER_ID = "204624"

MARKLAND_DAM_URL = "https://water.weather.gov/ahps2/hydrograph.php?wfo=iln&gage=mklk2"

MARKLAND_DAM_NAME = "Markland"
MARKLAND_DAM_LOWER_GUAGE_ID = "144523"
MARKLAND_GUAGE_XML_URL = (
    f"{NWS_website_baseaddress}{MARKLAND_DAM_LOWER_GUAGE_ID}{NWS_website_tailaddress}"
)


MCALPINE_DAM_NAME = "McAlpine"
MCALPINE_DAM_UPPER_GUAGE_ID = "142935"
MCALPINE_GUAGE_XML_URL = (
    f"{NWS_website_baseaddress}{MCALPINE_DAM_UPPER_GUAGE_ID}{NWS_website_tailaddress}"
)

MCALPINE_DAM_DETAILS = {  # some of these values can be used to test and verify data scraped from website
    "Friendly_Name": "McAlpine Dam Upper Guage",
    "guage_URL": MCALPINE_GUAGE_XML_URL,
    "milemarker": 606.8,
    "guage_elevation": 407.18,
    ACTION_LABELS[0]: 21,
    ACTION_LABELS[1]: 23,
    ACTION_LABELS[2]: 30,
    ACTION_LABELS[3]: 38,
}

MARKLAND_DAM_DETAILS = {
    "Friendly_Name": "Markland Dam Lower Guage",
    "guage_URL": MARKLAND_GUAGE_XML_URL,
    "milemarker": 531,
    "guage_elevation": 408,
    ACTION_LABELS[0]: 49,
    ACTION_LABELS[1]: 51,
    ACTION_LABELS[2]: 62,
    ACTION_LABELS[3]: 74,
}

RIVER_MONITORING_POINTS = {
    MCALPINE_DAM_NAME: MCALPINE_DAM_DETAILS,
    MARKLAND_DAM_NAME: MARKLAND_DAM_DETAILS,
}

RIVER_GUAGES = list(RIVER_MONITORING_POINTS.keys())

if __name__ == "__main__":
    for guage in RIVER_GUAGES:
        print()
        print(guage)
        print(RIVER_MONITORING_POINTS[guage])
    print(f'Total guages known: {len(RIVER_GUAGES)}')
