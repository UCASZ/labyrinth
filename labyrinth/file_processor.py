#!/usr/bin/env python
"""
file: file_processor
author: adh
created_at: 8/24/21 11:15 AM
"""
import hashlib
import os
import pandas as pd

from labyrinth.patterns import find_vul_ids
import logging

logger = logging.getLogger(__name__)


def process_file(fpath, workdir="/"):
    relpath = os.path.relpath(fpath, start=workdir)
    logger.debug(f"Processing {relpath}")

    df = pd.DataFrame()
    if not os.path.isfile(fpath):
        return df

    try:
        with open(fpath, "r", encoding="ISO-8859-1") as fp:

            filematches = []
            for line in fp.readlines():
                linematches = find_vul_ids(line.strip())
                filematches.extend(linematches)
            # unique them
            filematches = list(set(filematches))

            if len(filematches):
                logger.info(f"File {relpath} matched on {', '.join(filematches)}")
                df["match"] = filematches
                df["file"] = relpath

                file_sha1 = _file_sha1(fpath)
                df["file_sha1"] = file_sha1

                df = df.sort_values(by="match").reset_index(drop=True)

    except UnicodeDecodeError as e:
        logger.warning(f"Skipping file {relpath} because of UnicodeDecodeError: {e}")

    return df


def _file_sha1(fpath):
    # get the file sha1
    # BUF_SIZE is totally arbitrary, change for your app!
    BUF_SIZE = 65536  # lets read stuff in 64kb chunks!
    sha1 = hashlib.sha1()
    with open(fpath, "rb") as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha1.update(data)
    file_sha1 = sha1.hexdigest()
    return file_sha1


ignore_dirs = [
    ".git",
]


def process_dir(path, workdir="/"):
    df = pd.DataFrame()

    for (dirpath, dirnames, filenames) in os.walk(path, topdown=True):
        # filter dirnames we're willing to visit
        dirnames[:] = [d for d in dirnames if not d in ignore_dirs]
        # forget about .gitignore etc
        filenames[:] = [f for f in filenames if not f.startswith(".git")]

        for f in filenames:
            fpath = os.path.join(dirpath, f)
            _df = process_file(fpath, workdir)
            if len(_df):
                df = df.append(_df)

    if "match" in df.columns:
        df = df.sort_values(by="match").reset_index(drop=True)
    return df
