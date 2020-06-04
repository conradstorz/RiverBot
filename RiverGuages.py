#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Declaration of CONSTANTS used by NWS_WebScrape.py
"""

NWS_website_baseaddress = 'https://water.weather.gov//ahps2/river.php?wfo=lmk&wfoid=18699&riverid=204624&pt%5B%5D='
NWS_website_tailaddress = '&pt%5B%5D=144523&allpoints=150960&data%5B%5D=obs&data%5B%5D=xml'
# river guage ID is inserted between these strings

NWS_OHIO_RIVER_ID = '204624'

ACTION_LABELS = ["First-action", "Minor-flood", "Moderate-flood", "Major-flood"]

MARKLAND_DAM_URL = "https://water.weather.gov/ahps2/hydrograph.php?wfo=iln&gage=mklk2"
MARKLAND_DAM_NAME = "Markland"
MARKLAND_DAM_LOWER_GUAGE_ID = '144523'
MARKLAND_GUAGE_XML_URL = f'{NWS_website_baseaddress}{MARKLAND_DAM_LOWER_GUAGE_ID}{NWS_website_tailaddress}'
# text_mode_page = 'https://water.weather.gov//ahps2/river.php?wfo=lmk&wfoid=18699&riverid=204624&pt%5B%5D=144523&allpoints=150960%2C141893%2C143063%2C144287%2C142160%2C145137%2C143614%2C141268%2C144395%2C143843%2C142481%2C143607%2C145086%2C142497%2C151795%2C152657%2C141266%2C145247%2C143025%2C142896%2C144670%2C145264%2C144035%2C143875%2C143847%2C142264%2C152144%2C143602%2C144126%2C146318%2C141608%2C144451%2C144523%2C144877%2C151578%2C142935%2C142195%2C146116%2C143151%2C142437%2C142855%2C142537%2C142598%2C152963%2C143203%2C143868%2C144676%2C143954%2C143995%2C143371%2C153521%2C153530%2C143683&data%5B%5D=obs'
# works the same https://water.weather.gov//ahps2/river.php?wfo=lmk&wfoid=18699&riverid=204624&pt%5B%5D=144523&data%5B%5D=obs


MCALPINE_DAM_URL = "https://water.weather.gov/ahps2/hydrograph.php?gage=mluk2&wfo=lmk"
MCALPINE_DAM_NAME = "McAlpine"
MCALPINE_DAM_UPPER_GUAGE_ID = '142935'
# text_mode_page = 'https://water.weather.gov//ahps2/river.php?wfo=lmk&wfoid=18699&riverid=204624&pt%5B%5D=142935&allpoints=150960%2C141893%2C143063%2C144287%2C142160%2C145137%2C143614%2C141268%2C144395%2C143843%2C142481%2C143607%2C145086%2C142497%2C151795%2C152657%2C141266%2C145247%2C143025%2C142896%2C144670%2C145264%2C144035%2C143875%2C143847%2C142264%2C152144%2C143602%2C144126%2C146318%2C141608%2C144451%2C144523%2C144877%2C151578%2C142935%2C142195%2C146116%2C143151%2C142437%2C142855%2C142537%2C142598%2C152963%2C143203%2C143868%2C144676%2C143954%2C143995%2C143371%2C153521%2C153530%2C143683&data%5B%5D=obs'
# works the same https://water.weather.gov//ahps2/river.php?wfo=lmk&wfoid=18699&riverid=204624&pt[]=142935&data[]=obs

# f-string substitution example: river_id, guage_id
# f'https://water.weather.gov//ahps2/river.php?wfo=lmk&wfoid=18699&riverid={river_id}&pt[]={guage_id}&data[]=obs'

MCALPINE_DAM_DETAILS = { # some of these values can be used to test and verify data scraped from website
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

