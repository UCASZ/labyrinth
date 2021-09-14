#!/usr/bin/env python
"""
file: dir_helpers
author: adh
created_at: 8/12/21 3:33 PM
"""
import os
import glob
import logging

import labyrinth.config as cfg

logger = logging.getLogger(__name__)


def setup_daily_output_dirs(data_home, dt_dir):
    # make some directories
    data_dir = os.path.join(data_home, dt_dir)
    os.makedirs(data_dir, exist_ok=True)
    return data_dir


def setup_output_dirs():
    # make output dirs
    for d in (
        cfg.SEARCH_RESULTS_HOME,
        cfg.FILE_RESULTS_HOME,
        cfg.VUL_ID_RESULTS_HOME,
        cfg.REPO_ID_RESULTS_HOME,
    ):
        try:
            os.makedirs(d, exist_ok=False)
            logger.info(f"Created output dir {d}")
        except FileExistsError as e:
            logger.debug(f"Output dir {d} already exists")

    return cfg.SEARCH_RESULTS_HOME


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
