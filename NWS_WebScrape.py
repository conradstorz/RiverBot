#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""NWS website scraping for river guage observations and forecasts.
This module will create local database of readings and forecasts.
A single database will contain the readings from any guages of interest.
Keys are the guage name + datetime of reading/forecast + R/F label
Data is tuple of level and flowrate. (currently no flow data is published)
"""
from loguru import logger

logger.remove()  # stop any default logger
LOGGING_LEVEL = "INFO"

from WebScrapeTools import retrieve_cleaned_html
from RiverGuages import MARKLAND_GUAGE_XML_URL as mrklnd

@logger.catch
def get_NWS_web_data(site):
    clean_soup = retrieve_cleaned_html(site)
    guage_id = clean_soup.h1["id"]
    guage_string = clean_soup.h1.string
    nws_class = clean_soup.find(class_="obs_fores")
    nws_obsfores_contents = nws_class.contents
    return (nws_obsfores_contents, guage_id, guage_string)


@logger.catch
def FixDate(s, currentyear, time_zone="UTC"):
    """Split date from time and add timezone label.
    Unfortunately, NWS chose not to include the year. 
    This will be problematic when forecast dates are into the next year.
    If Observation dates are in December, Forecast dates must be checked and fixed for roll over into next year.
    """
    date_string, time_string = s.split()
    month_digits, day_digits = date_string.split("/")
    return (month_digits, day_digits, currentyear, time_string, time_zone)


@logger.catch
def sort_and_label_data(web_data, guage_id, guage_string):
    readings = []
    labels = ["datetime", "level", "flow"]
    for i, item in enumerate(web_data):
        if i >= 1:  # zeroth item is an empty list
            # locate the name of this section (observed / forecast)
            section = item.find(class_="data_name").contents[0]
            sect_name = section.split()[0]
            row_dict = {"guage": guage_id, "type": sect_name}
            # extract all readings from this section
            section_data_list = item.find_all(class_="names_infos")
            # organize the readings and add details
            for i, data in enumerate(section_data_list):
                element = data.contents[0]
                pointer = i % 3  # each reading contains 3 unique data points
                if pointer == 0:  # this is the element for date/time
                    element = FixDate(element, "2020")
                row_dict[labels[pointer]] = element
                if pointer == 2:  # end of this reading
                    readings.append(row_dict)  # add to the compilation
                    # reset the dict for next reading
                    row_dict = {"guage": guage_id, "type": sect_name}
    return readings


@logger.catch
def compact_datestring(ds):
    """Return a string representing datetime of provided tuple.
    """
    return f"{ds[0]}{ds[1]}{ds[2]}_{ds[3]}{ds[4]}"


@logger.catch
def expand_datestring(ds):
    """Return elements of provided datestring.
    """
    x = ds.split("_")
    m = x[0][:2]
    d = x[0][2:4]
    y = x[0][-4:]
    t = x[1][:5]
    z = x[1][-3:]
    return (m, d, y, t, z)


@logger.catch
def generate_database_keys(web_list):
    """Take a list of dicts and return a unique key for each dict in list.
    """
    keys = []
    for itm in web_list:
        dt = compact_datestring(itm["datetime"])
        tp = itm["type"]
        gg = itm["guage"]
        key = f"{gg}-{tp}-{dt}"
        keys.append(key)
    return keys


@logger.catch
def decode_database_key(s):
    """Extract Guage_id, Reading_type, Datestr form provided keystring.
    """
    lst = s.split("-")
    gid = lst[0]
    rdng = lst[1]
    dstr = lst[2]
    return (gid, rdng, dstr)

@logger.catch
def Scrape_NWS_site(site):
    """Return a dictionary of guage readings from supplied XML tabular text site.
    """
    raw_data, guage_id, friendly_name = get_NWS_web_data(site)
    # TODO verify webscraping success
    data_list = sort_and_label_data(raw_data, guage_id, friendly_name)
    # TODO verify successful conversion of data
    database_keys = generate_database_keys(data_list)
    # TODO compare length of keys_list to length of data_list for validity
    database_dict = dict(zip(database_keys, data_list))
    # TODO compare length of database to data_list to verify all items included
    return database_dict


@logger.catch
def Main():
    # TODO scrape all guages of interest and combine into dictionary
    raw_data, guage_id, friendly_name = get_NWS_web_data(mrklnd)
    # TODO verify webscraping success
    data_list = sort_and_label_data(raw_data, guage_id, friendly_name)
    # TODO verify successful conversion of data
    database_keys = generate_database_keys(data_list)
    # TODO compare length of keys_list to length of data_list for validity
    database_dict = dict(zip(database_keys, data_list))
    # TODO compare length of database to data_list to verify all items included
    for k, v in database_dict.items():
        print(k)
        print(v)
        print()
    return True


Main()
