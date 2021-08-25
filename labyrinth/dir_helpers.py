#!/usr/bin/env python
"""
file: dir_helpers
author: adh
created_at: 8/12/21 3:33 PM
"""
import os
import glob

def main():
    pass


if __name__ == "__main__":
    main()


def setup_daily_output_dirs(data_home, dt_dir):
    # make some directories
    data_dir = os.path.join(data_home, dt_dir)
    os.makedirs(data_dir, exist_ok=True)
    return data_dir


def setup_output_dirs():
    # make output dirs
    output_home = "results"
    data_home = output_home
    os.makedirs(output_home, exist_ok=True)
    # these won't change anything if both are set to output home
    os.makedirs(data_home, exist_ok=True)
    return data_home

def yearly_summaries(results_dir):
    glob_pattern = "**/[12][0-9][0-9][0-9]_summary.json"
    return _file_glob(glob_pattern, results_dir)

def monthly_summaries(results_dir):
    glob_pattern = "**/[12][0-9][0-9][0-9]-[01][0-9]_summary.json"
    return _file_glob(glob_pattern, results_dir)

def daily_summaries(results_dir):
    glob_pattern = "**/[12][0-9][0-9][0-9]-[01][0-9]-[0-3][0-9]_summary.json"
    return _file_glob(glob_pattern, results_dir)

def _file_glob(glob_pattern, results_dir):
    full_glob = os.path.join(results_dir, glob_pattern)
    files = glob.glob(full_glob, recursive=True)
    return files
