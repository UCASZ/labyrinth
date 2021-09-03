#!/usr/bin/env python
"""
file: __init__.py
author: adh
created_at: 8/10/21 10:45 AM
"""
import os

DEBUG = False
VERBOSE = False
GH_TOKEN = os.getenv("GH_TOKEN")  # will be None if unset
