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

from pathlib import Path
from time import sleep
from pupdb.core import PupDB
from datetime import *
from dateutil.parser import *
from loguru import logger
from tabulate import tabulate


LOGGING_LEVEL = "INFO"
RUNTIME_NAME = Path(__file__).name
from core_logging_setup import defineLoggers

# used to standardize string formats across modules
from time_strings import LOCAL_CURRENT_YEAR, UTC_NOW_STRING, LOCAL_TODAY, timefstring, tz_UTC

TS_LABEL_STR = "timestamp" # for use in generating data and indexing result

from WebScrapeTools import retrieve_cleaned_html
from RiverGuages import RIVER_MONITORING_POINTS, RIVER_GUAGES, PupDB_FILENAME
from data_2_csv import write_csv

# National Weather Service does not put the YEAR into the tabular data of their website
# we must declare the current year here.


@logger.catch
def get_NWS_web_data(site):
    """Retrieve data from National Weather Service website. Provided 'site' variable
    should point to a page that provides tabular river data. This function returns
    the contents of the site and a timestamp of the actual website scraping event.
    """
    start_time = datetime.now(tz_UTC)
    clean_soup = retrieve_cleaned_html(site)
    finish_time = datetime.now(tz_UTC)
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
    """Returns a list of dicts containing relevant data from webscrape.
    """
    readings = []
    guage_id, elev, milemarker, _ = guage_details
    relevant_labels = [TS_LABEL_STR, "level", "flow"]
    for i, item in enumerate(web_data):
        if i >= 1:  # zeroth item is an empty list
            # locate the name of this section (observed / forecast)
            section = item.find(class_="data_name").contents[0]
            sect_name = section.split()[0]
            row_dict = {}
            # extract all readings from this section
            section_data_list = item.find_all(class_="names_infos")
            # organize the readings and add details
            for i, data in enumerate(section_data_list):
                element = data.contents[0]
                pointer = i % 3  # each reading contains 3 unique data points
                label = relevant_labels[pointer]
                if pointer == 0:  # this is the element for date/time
                    element = FixDate(element, LOCAL_CURRENT_YEAR)
                row_dict[label] = element
                if pointer == 2:  # end of this reading
                    row_dict["guage"] = guage_id
                    row_dict["scrape time"] = time
                    row_dict["elevation"] = elev
                    row_dict["milemarker"] = milemarker
                    row_dict["type"] = sect_name             
                    readings.append(row_dict)  # add to the compilation
                    # reset the dict for next reading
                    row_dict={}

    return readings


@logger.catch
def generate_keys_based_on_timestamp(web_list):
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

    logger.info(f"Time to process website: {duration_of_scrape.total_seconds()} seconds.")
    logger.info(f"Webscrape started at: {scrape_start_time}")
    # TODO verify webscraping success
    guage_data = (guage_id, site["guage_elevation"], site["milemarker"], friendly_name)
    ValuableData_listOfDicts = sort_and_label_data(raw_data, guage_data, timefstring(scrape_start_time))
    # TODO verify successful conversion of data
    database_keys = generate_keys_based_on_timestamp(ValuableData_listOfDicts)
    # TODO compare length of keys_list to length of data_list for validity
    database_dict = dict(zip(database_keys, ValuableData_listOfDicts))
    # TODO compare length of database to data_list to verify all items included
    return (database_dict, ValuableData_listOfDicts)


@logger.catch
def display_tabulardata(datalist_of_dicts):
    """create a new file based on the time of scrape
    """
    #print(tabulate(datalist_of_dicts, headers="keys"))    


@logger.catch
def save_results_to_storage(list_of_dicts):
    """save unique readings and forecasts to longterm storage.
    list_of_dicts is expected to contain one dict for each reading/forecast
    """
    fname = list_of_dicts[0]['scrape time']
    logger.info(f'Creating CSV filename: {fname}')
    # TODO organize storage as a tree of directories: YEAR/MONTH/DAY/xx:xx:xx
    write_csv(list_of_dicts, filename=fname)


@logger.catch
def update_web_scrape_results():
    """Update filesystem CSV records for latest website scrapes.
    """
    for guage in RIVER_GUAGES:
        details = RIVER_MONITORING_POINTS[guage]
        logger.info(details)
        dbd, vdl = Scrape_NWS_site(details)
        display_tabulardata(vdl)
        save_results_to_storage(vdl)
        sleep(1) # guarantee at least 1 second difference in webscrapes timestamps
        # TODO verify webscraping success
        count = len(dbd)
        logger.info(f"Total values retrieved: {count} from {details['Friendly_Name']}")

    return True


@logger.catch
def Main():
    """Update webscrape files.
    """
    defineLoggers(LOGGING_LEVEL, RUNTIME_NAME)
    logger.info("Program Start.")
    logger.info(f"Today is: {LOCAL_TODAY}")
    
    update_web_scrape_results()

    return True


if __name__ == "__main__":
    Main()
