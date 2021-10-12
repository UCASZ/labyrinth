#!/usr/bin/env python
"""
file: config
author: adh
created_at: 9/14/21 2:03 PM
"""
import os

DEBUG = False
VERBOSE = False
GH_TOKEN = os.getenv("GH_TOKEN")  # will be None if unset

SEARCH_RESULTS_HOME = "results"
FILE_RESULTS_HOME = "data"
VUL_ID_RESULTS_HOME = os.path.join(FILE_RESULTS_HOME, "vul_id")
REPO_ID_RESULTS_HOME = os.path.join(FILE_RESULTS_HOME, "repo_id")
