#!/usr/bin/env python
"""
file: date_helpers
author: adh
created_at: 8/12/21 12:48 PM
"""
import re
from datetime import date, timedelta
import argparse

import pandas as pd
from pandas._libs.tslibs.offsets import YearBegin, YearEnd, MonthBegin, MonthEnd


year_pat = re.compile("^\d{4}$")
month_pat = re.compile("^\d{4}-\d{2}$")
day_pat = re.compile("^\d{4}-\d{2}-\d{2}$")
year_begin = lambda x: (pd.to_datetime(x) - YearBegin(0)).strftime("%Y-%m-%d")
year_end = lambda x: (pd.to_datetime(x) + YearEnd(1)).strftime("%Y-%m-%d")
month_begin = lambda x: (pd.to_datetime(x) - MonthBegin(0)).strftime("%Y-%m-%d")
month_end = lambda x: (pd.to_datetime(x) + MonthEnd(1)).strftime("%Y-%m-%d")


def fixup_end_date(end_date=None):
    if end_date is None:
        return date.today().strftime("%Y-%m-%d")

    if year_pat.match(end_date):
        return year_end(end_date)

    if month_pat.match(end_date):
        return month_end(end_date)

    return end_date


def fixup_start_date(start_date=None):
    if start_date is None:
        yesterday = date.today() - timedelta(days=1)
        return yesterday.strftime("%Y-%m-%d")

    if year_pat.match(start_date):
        return year_begin(start_date)

    if month_pat.match(start_date):
        return month_begin(start_date)

    return start_date


def year_type(arg_value, pat=year_pat):
    if not pat.match(arg_value):
        raise argparse.ArgumentTypeError
    return arg_value


def month_type(arg_value, pat=month_pat):
    if not pat.match(arg_value):
        raise argparse.ArgumentTypeError
    return arg_value


def day_type(arg_value, pat=day_pat):
    if not pat.match(arg_value):
        raise argparse.ArgumentTypeError
    return arg_value
