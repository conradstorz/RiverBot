#!/usr/bin/env python
# -*- coding: utf-8 -*-
# version 1.0
"""Standardize methods for file handling.
"""

from pathlib import Path

# set your reference point with the location of the python file you’re writing in
this_file = Path(__file__)

# Here are three ways to get the folder of the current python file
this_folder1 = Path(__file__, "..")
this_folder2 = Path(__file__) / ".."
this_folder3 = Path(__file__).parent
# This will fail becasue the variables are relative paths:
# assert this_folder1 == this_folder2 == this_folder3

# The resolve() method removes '..' segments, follows symlinks, and returns
# the absolute path to the item.
# this works:
# assert this_folder1.resolve() == this_folder2.resolve() == this_folder3.resolve()

# folder_where_python_was_run = Path.cwd()

# create a new folder:
# Path("/my/directory").mkdir(parents=True, exist_ok=True)

# project_root = Path(__file__).resolve().parents[1] # this is the folder 2 levels up from your running code.
# create a new PathObj:
# static_files = project_root / 'static' # if you like this sort of thing they overrode the divide operator.
# media_files = Path(project_root, 'media') # I prefer this method.

# how to define 2 sub-directories at once:
# compiled_js_folder = static_files.joinpath('dist', 'js') # this is robust across all OS.

# list(static_files.iterdir()) # returns a list of all items in directory.

# [x for x in static_files.iterdir if x.is_dir()] # list of only directories in a folder.

# [x for x in static_files.iterdir if x.is_file()] # same for files only.

# get a list of items matching a pattern:
# list(compiled_js_folder.glob('*.js')) # returns files ending with '.js'.

# search recursively down your folders path:
# sorted(project_root.rglob('*.js'))

# verify a path exists:
# Path('relative/path/to/nowhere').exists() # returns: False

#Example of directory deletion by pathlib
#pathobj = Path("demo/")
#pathobj.rmdir()
	
#Example of file deletion by pathlib
#pathobj = Path("demo/testfile.txt")
#pathobj.unlink()

""" access parts of a filename:
>>> Path('static/dist/js/app.min.js').name
'app.min.js'
>>> Path('static/dist/js/app.min.js').suffix
'.js'
>>> Path('static/dist/js/app.min.js').suffixes
'.min.js'
>>> Path('static/dist/js/app.min.js').stem
'app'
"""


def clean_filename_str(fn):
    """Remove invalid characters from provided string.
    """
    if type(fn) != str: return fn
    return Path("".join(i for i in fn if i not in "\/:*?<>|"))


def check_and_validate(fname, direc, rename=True):
    """Return a PathObj for this filename/directory.
    Fail if filename already exists in directory but optionally rename.
    """
    fn = clean_filename_str(fname)
    dr = clean_filename_str(direc)
    dr.mkdir(parents=True, exist_ok=True)
    OUT_PATH_HANDLE = Path(dr, fn)
    i = 0
    while Path(OUT_PATH_HANDLE).exists():
        if rename:
            # TODO  strip old (#) from name and rename
            i += 1
            fn = f'{fn}({i})'
            OUT_PATH_HANDLE = Path(dr, fn)
        else:
            raise(FileExistsError)
    return OUT_PATH_HANDLE


if __name__ == "__main__":
    print(f'This file {this_file} has no current standalone function.')
    