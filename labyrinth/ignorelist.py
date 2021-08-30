#!/usr/bin/env python
"""
file: ignorelist
author: adh
created_at: 8/26/21 3:12 PM
"""
import pkg_resources
import pandas as pd

_OWNER_LOGIN_LIST = pd.read_csv(
    pkg_resources.resource_stream(__name__, "data/owner_logins.txt"), header=None
)[0].to_list()

_REPO_NAME_LIST = pd.read_csv(
    pkg_resources.resource_stream(__name__, "data/repo_names.txt"), header=None
)[0].to_list()

_FULL_NAME_LIST = pd.read_csv(
    pkg_resources.resource_stream(__name__, "data/full_names.txt"), header=None
)[0].to_list()


# Keys must match elements found in *_summary.json files
_IGNORE_REPOS = {
    "owner_login": _OWNER_LOGIN_LIST,
    "name": _REPO_NAME_LIST,
    "full_name": _FULL_NAME_LIST,
}

IGNORE_REPOS = {}
for k, values in _IGNORE_REPOS.items():
    IGNORE_REPOS[k] = [v.lower() for v in values]

assert "certcc/labyrinth" in IGNORE_REPOS["full_name"]

IGNORE_FILE_EXTS = [
    ".json",
    ".png",
    ".jpg",
    ".gif",
    ".owl",
]

IGNORE_DIRS = [
    ".git",
]


def main():
    pass


if __name__ == "__main__":
    main()
