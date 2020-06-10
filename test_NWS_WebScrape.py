#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Code coverage for NWS_WebScrape functions.
"""

from .NWS_WebScrape import expand_datestring, compact_datestring

"""
@composite # generate a tuple containing month,day,year,time,tzone in fixed sizes
def xds_tuple(draw, elements=text()):
    xm = draw(text( min_size=2, max_size=2 ))
    xd = draw(text( min_size=2, max_size=2 ))
    xy = draw(text( min_size=4, max_size=4 ))
    xt = draw(text( min_size=5, max_size=5 ))
    xz = draw(text( min_size=3, max_size=3 ))
    return (xm, xd, xy, xt, xz)

hypothesis.strategies.characters
hypothesis.strategies.dates
hypothesis.strategies.datetimes
hypothesis.strategies.integers
hypothesis.strategies.text
hypothesis.strategies.times
hypothesis.strategies.tuples(integers(), integers()) 
"""

def test_datestring_conversions():
    ds = ('03', '12', '2019', '11:59', 'UTC')
    assert ds == expand_datestring(compact_datestring(ds))
