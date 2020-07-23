#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""National Weather Service(NWS) website scraping 
for river guage observations and forecasts.
This module will create local database of readings and forecasts.
A single database will contain the readings from any guages of interest.
Keys are the guage name + date of webscrape.
    Data is a dict of webscrape times in UTC. 
        Webscrape times contain a dict of NWS reported times in UTC.
            Data is guagename and details, 
                    observed/forecast tag, 
                    NWS:UTC timestamp for value.
"""

from os import path
from pupdb.core import PupDB
from datetime import *
from dateutil.parser import *
from loguru import logger

LOGGING_LEVEL = "INFO"
RUNTIME_NAME = path.basename(__file__)
from core_logging_setup import defineLoggers

# used to standardize string formats across modules
from time_strings import LOCAL_CURRENT_YEAR, NOW_UTC_STRING, LOCAL_TODAY, timefstring

TS_LABEL_STR = "timestamp" # for use in generating data and indexing result

from WebScrapeTools import retrieve_cleaned_html
from RiverGuages import RIVER_MONITORING_POINTS, RIVER_GUAGES, PupDB_FILENAME

# National Weather Service does not put the YEAR into the tabular data of their website
# we must declare the current year here.


@logger.catch
def get_NWS_web_data(site):
    """Retrieve data from National Weather Service website. Provided 'site' variable
    should point to a page that provides tabular river data. This function returns
    the contents of the site and a timestamp of the actual website scraping event.
    """
    start_time = datetime.now()
    clean_soup = retrieve_cleaned_html(site)
    finish_time = datetime.now()
    elapsed_time = finish_time - start_time
    guage_id = clean_soup.h1["id"]
    guage_string = clean_soup.h1.string
    nws_class = clean_soup.find(class_="obs_fores")
    nws_obsfores_contents = nws_class.contents
    return (nws_obsfores_contents, guage_id, guage_string, start_time, elapsed_time)


@logger.catch
def FixDate(s, currentyear, time_zone="UTC"):
    """Split date from time and add timezone label.
    Unfortunately, NWS chose not to include the year. 
    This will be problematic when forecast dates are into the next year.
    If Observation dates are in December, Forecast dates must be checked 
    and fixed for roll over into next year.
    """
    # TODO check and fix end of year forecast dates

    return timefstring(parse(s))


@logger.catch
def sort_and_label_data(web_data, guage_details, time):
    """Returns a list of relevant data from webscrape.
    """
    readings = []
    guage_id = guage_details[0]
    elev = guage_details[1]
    milemarker = guage_details[2]
    relevant_label = [TS_LABEL_STR, "level", "flow"]
    for i, item in enumerate(web_data):
        if i >= 1:  # zeroth item is an empty list
            # locate the name of this section (observed / forecast)
            section = item.find(class_="data_name").contents[0]
            sect_name = section.split()[0]
            row_dict = {
                "guage": guage_id,
                "scrape time": time,
                "elevation": elev,
                "milemarker": milemarker,
                "type": sect_name,
            }
            # extract all readings from this section
            section_data_list = item.find_all(class_="names_infos")
            # organize the readings and add details
            for i, data in enumerate(section_data_list):
                element = data.contents[0]
                pointer = i % 3  # each reading contains 3 unique data points
                if pointer == 0:  # this is the element for date/time
                    element = FixDate(element, LOCAL_CURRENT_YEAR)
                row_dict[relevant_label[pointer]] = element
                if pointer == 2:  # end of this reading
                    readings.append(row_dict)  # add to the compilation
                    # reset the dict for next reading
                    row_dict = {
                        "guage": guage_id,
                        "scrape time": time,
                        "elevation": elev,
                        "milemarker": milemarker,
                        "type": sect_name,
                    }
    return readings


@logger.catch
def generate_primary_database_keys(web_list):
    """Take a list of dicts and return a key for each dict in list.
    """
    keys = []

    for itm in web_list:
        cdt = itm[TS_LABEL_STR]
        key = f"{cdt}"
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
    site_url = site["guage_URL"]
    # get the data for this guage
    (
        raw_data,
        guage_id,
        friendly_name,
        scrape_start_time,
        duration_of_scrape,
    ) = get_NWS_web_data(site_url)
    logger.info(f"Time to process website: {duration_of_scrape}")
    logger.info(f"Webscrape started at: {scrape_start_time}")
    # TODO verify webscraping success
    guage_data = (guage_id, site["guage_elevation"], site["milemarker"], friendly_name)
    valuabledata_list = sort_and_label_data(raw_data, guage_data, NOW_UTC_STRING)
    # TODO verify successful conversion of data
    database_keys = generate_primary_database_keys(valuabledata_list)
    # TODO compare length of keys_list to length of data_list for validity
    database_dict = dict(zip(database_keys, valuabledata_list))
    # TODO compare length of database to data_list to verify all items included
    return (database_dict, valuabledata_list)


@logger.catch
def Main():

    from tabulate import tabulate

    defineLoggers(LOGGING_LEVEL, RUNTIME_NAME)
    logger.info("Program Start.")
    logger.info(f"Today is: {LOCAL_TODAY}")
    storage_db = PupDB(PupDB_FILENAME)  # activate PupDB file for persistent storage
    mrklndguage = RIVER_GUAGES[1]
    mrklnd = RIVER_MONITORING_POINTS[mrklndguage]
    logger.info(mrklnd)
    dbd, vdl = Scrape_NWS_site(mrklnd)

    # TODO verify webscraping success

    print(tabulate(vdl, headers="keys"))
    count = len(dbd)
    logger.info(f"Total values retrieved: {count}")

    """
    # send records to CSV format
    import csv
    with open('mycsvfile.csv','wb') as f:
        w = csv.writer(f)
        w.writerow(dbd.items())
    """

    return True


if __name__ == "__main__":
    Main()
