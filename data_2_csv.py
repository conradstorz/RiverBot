#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Create a file and populate with items from a data structure.
"""

import csv
from pathlib import Path
from filehandling import check_and_validate


def write_csv(data, filename="temp.csv", directory="CSV_DATA"):
    """'data' is expected to be a list of dicts 
    Take data and write all fields to storage as csv with headers from keys.
    """
    # writing to csv file
    dirobj = Path(Path.cwd(), directory)
    pathobj = check_and_validate(filename, dirobj)
    with open(pathobj, "w", newline="") as csvfile:
        headers = data[0].keys()
        # datalist = [item.values() for item in data]

        # creating a csv dict writer object
        writer = csv.DictWriter(csvfile, fieldnames=headers)

        # writing headers (field names)
        writer.writeheader()

        # writing data rows
        writer.writerows(data)
