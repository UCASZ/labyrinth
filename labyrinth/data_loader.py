#!/usr/bin/env python
"""
file: data_loader
author: adh
created_at: 8/25/21 9:33 AM
"""
import pandas as pd
from labyrinth.dir_helpers import yearly_summaries, monthly_summaries, daily_summaries


def load_years(results_dir):
    files = yearly_summaries(results_dir)
    return load_data(files)


def load_months(results_dir):
    files = monthly_summaries(results_dir)
    return load_data(files)


def load_days(results_dir):
    files = daily_summaries(results_dir)
    return load_data(files)


def load_data(json_files):
    df = pd.DataFrame()
    for f in json_files:
        _df = pd.read_json(f)
        df = df.append(_df)
    return df
