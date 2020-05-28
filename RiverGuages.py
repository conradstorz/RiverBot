#!/usr/bin/env python
# -*- coding: utf-8 -*-

ACTION_LABELS = ["First-action", "Minor-flood", "Moderate-flood", "Major-flood"]

MARKLAND_DAM_URL = "https://water.weather.gov/ahps2/hydrograph.php?wfo=iln&gage=mklk2"
MARKLAND_DAM_NAME = "Markland"

MCALPINE_DAM_URL = "https://water.weather.gov/ahps2/hydrograph.php?gage=mluk2&wfo=lmk"
MCALPINE_DAM_NAME = "McAlpine"

MCALPINE_DAM_DETAILS = {
    "Friendly_Name": "McAlpine Dam Upper Guage",
    "Dam_URL": MCALPINE_DAM_URL,
    "milemarker": 606.8,
    "guage_elevation": 407.18,
    ACTION_LABELS[0]: 21,
    ACTION_LABELS[1]: 23,
    ACTION_LABELS[2]: 30,
    ACTION_LABELS[3]: 38,
}

MARKLAND_DAM_DETAILS = {
    "Friendly_Name": "Markland Dam Lower Guage",
    "Dam_URL": MARKLAND_DAM_URL,
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
IMPORTANT_OBSERVATIONS = ["Forecast:", "Latest", "Highest"]

