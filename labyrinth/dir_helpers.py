#!/usr/bin/env python
"""
file: dir_helpers
author: adh
created_at: 8/12/21 3:33 PM
"""
import os
import glob
import logging

logger = logging.getLogger(__name__)

SEARCH_RESULTS_HOME = "results"
FILE_RESULTS_HOME = "data"
VUL_ID_RESULTS_HOME = os.path.join(FILE_RESULTS_HOME, "vul_id")
REPO_ID_RESULTS_HOME = os.path.join(FILE_RESULTS_HOME, "repo_id")


def setup_daily_output_dirs(data_home, dt_dir):
    # make some directories
    data_dir = os.path.join(data_home, dt_dir)
    os.makedirs(data_dir, exist_ok=True)
    return data_dir


def setup_output_dirs():
    # make output dirs
    for d in (
        SEARCH_RESULTS_HOME,
        FILE_RESULTS_HOME,
        VUL_ID_RESULTS_HOME,
        REPO_ID_RESULTS_HOME,
    ):
        try:
            os.makedirs(d, exist_ok=False)
            logger.info(f"Created output dir {d}")
        except FileExistsError as e:
            logger.debug(f"Output dir {d} already exists")

    return SEARCH_RESULTS_HOME


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
