#!/usr/bin/env python
"""
file: repo_processor
author: adh
created_at: 8/25/21 3:12 PM
"""
import os
import tempfile
import logging
import git
import git.exc
import time
import pandas as pd
import re


import labyrinth
from labyrinth.errors import LabyrinthError
from labyrinth.file_processor import process_dir
from labyrinth.patterns import find_vul_ids, id_to_path, repo_id_to_path
from labyrinth.dir_helpers import (
    setup_output_dirs,
    REPO_ID_RESULTS_HOME,
    VUL_ID_RESULTS_HOME,
)
from labyrinth.ignorelist import IGNORE_REPOS

logger = logging.getLogger(__name__)

DAYHOURS = 24
DAYMIN = DAYHOURS * 60  # 1440
DAYSEC = DAYMIN * 60  # 86400
AGE_LIMIT_DAYS = 7


def process_git_url(clone_from, workdir):
    logger.debug(f"Cloning {clone_from} to {workdir}")
    try:
        git.Repo().clone_from(
            url=clone_from,
            to_path=workdir,
            depth=1,
        )
    except git.exc.GitCommandError as e:
        logger.warning(f"Skipping git repo at {clone_from} due to GitCommandError: {e}")
        return pd.DataFrame()

    df = process_dir(workdir, workdir)
    return df


def _dump_json(df, fpath):
    df.to_json(fpath, orient="records", indent=2, date_format="iso", date_unit="s")


def _dump_csv(df, outfile):
    df.to_csv(outfile, index=False, float_format="%.6f")


def process_row(row):
    # each row is a record for a repository

    repo_name = row["full_name"]
    repo_id = row["id"]
    clone_url = row["clone_url"]

    repo_num = row["index"]
    repo_tot = row["total_repos"]

    df = pd.DataFrame()

    for key, ignorelist in IGNORE_REPOS.items():
        if row[key].lower() in ignorelist:
            return df

    repo_path = os.path.join(REPO_ID_RESULTS_HOME, repo_id_to_path(repo_id))
    csvfile = os.path.join(repo_path, f"{repo_id}.csv")

    # do we already have results for repo?
    if os.path.exists(csvfile):
        mtime = os.path.getmtime(csvfile)
        age_seconds = time.time() - mtime
        age_days = age_seconds / DAYSEC
        # are they recent?
        # TODO: change this to use a github api request and compare mtime to repo.pushed_atgre

        if age_days < AGE_LIMIT_DAYS:
            logger.info(
                f"Found existing results for {repo_name} within past {AGE_LIMIT_DAYS} days, skipping"
            )
            return df
    else:
        # write an empty json file to at least record that we looked at this repo
        # it will get overwritten later if we have results
        logger.debug(f"No existing results found for {csvfile}, creating placeholder")
        os.makedirs(repo_path, exist_ok=True)
        df.to_csv(csvfile, index=False)

    cols2check = [
        "full_name",
        "html_url",
        "description",
        "url",
        "homepage",
    ]
    # concatenate some string columns so we can do a single vul ID pattern match
    # note that this has to be done before we truncate the descriptions in the next step
    _concatenated_strings = " ".join([str(x) for x in row[cols2check]])
    row_matches = find_vul_ids(_concatenated_strings)

    if len(row_matches):
        df["match"] = row_matches
        df["file"] = "_GITHUB_REPO_METADATA_"
        df["file_sha1"] = None

    with tempfile.TemporaryDirectory(prefix="git-clone-") as workdir:
        logger.info(f"Cloning {clone_url} {repo_num} of {repo_tot}")
        _df = process_git_url(clone_url, workdir)
    # confirm cleanup
    if os.path.isdir(workdir):
        raise LabyrinthError(f"Failed to clean up workdir: {workdir}")

    if len(_df):
        df = df.append(_df)

    if not len(df):
        return df

    df = df.sort_values(by="match")

    # set a weight based on how many different IDs matched in total
    # this will be used to sort the by-vul-id output
    # count unique matches in this frame
    ucount = df["match"].nunique()
    df["match_weight"] = 1.0 / ucount

    # these are the same for every row
    df["repo_full_name"] = repo_name
    df["repo_id"] = repo_id
    df["repo_html_url"] = row["html_url"]
    df["repo_pushed_at"] = row["pushed_at"]
    # df["repo_updated_at"] = row["updated_at"]
    # df["repo_matched_at"] = row["matched_at"]

    return df


def dump_results_by_vul_id(df):
    outdir = VUL_ID_RESULTS_HOME
    os.makedirs(outdir, exist_ok=True)

    # how many files matched
    # how many vuls matched this file
    # how many vuls matched the repo
    # tf-idf of match relative to repo

    cols = [
        "match",
        "repo_full_name",
        "repo_id",
        "repo_html_url",
        "match_weight",
    ]

    try:
        df = pd.DataFrame(df[cols])
    except KeyError as e:
        logger.warning("Caught KeyError: {e}")
        return

    df = df.drop_duplicates(subset=["match", "repo_id"])

    for gname, group in df.groupby(by=["match"]):
        group_path = id_to_path(gname)
        group_dir = os.path.join(outdir, group_path)
        os.makedirs(group_dir, exist_ok=True)

        csvfile = os.path.join(group_dir, f"{gname}.csv")

        if os.path.exists(csvfile):
            logger.debug(f"Loading existing results for {gname} from {csvfile}")
            old_df = pd.read_csv(csvfile)
            new_df = old_df.append(group)
        else:
            new_df = group

        # because old_df has old results before the new ones we just got
        # this will keep the most recent result for each repo
        new_df = new_df.drop_duplicates(
            subset="repo_id",
            keep="last",
        )

        logger.debug(f"Write {gname} results to {csvfile} ({len(new_df)})")
        # goal is to avoid merge conflicts
        # sort by repo_id to keep the row ordering consistent across runs
        # new_df = new_df.sort_values(by="repo_id", ascending=True)

        # sort by match_weight to keep the most likely single-exploits repos
        # at the top. This will cause some rows to move around as new repos
        # are scanned
        new_df = new_df.sort_values(by="match_weight", ascending=False)

        col_order = [
            "match",
            "match_weight",
            "repo_full_name",
            "repo_html_url",
            "repo_id",
        ]
        new_df = new_df[col_order]
        _dump_csv(new_df, csvfile)


def dump_results_by_repo(df):
    outdir = REPO_ID_RESULTS_HOME
    os.makedirs(outdir, exist_ok=True)

    cols = ["repo_id", "repo_full_name", "file", "file_sha1", "match"]
    try:
        df = pd.DataFrame(df[cols])
    except KeyError as e:
        logger.warning(f"Caught KeyError on DataFrame: {e}")
        return

    df = df.drop_duplicates()
    df = df.sort_values(by=["repo_id", "file"])

    for gname, group in df.groupby(by=["repo_id"]):
        group_path = repo_id_to_path(gname)
        group_dir = os.path.join(outdir, group_path)
        os.makedirs(group_dir, exist_ok=True)

        csvfile = os.path.join(group_dir, f"{gname}.csv")

        # we're just going to overwrite the old data since we just looked at the whole thing
        new_df = group
        new_df = new_df.sort_values(by=["match", "file"], ascending=True)
        new_df = new_df.drop_duplicates(
            subset=["file_sha1", "match"],
            keep="first",
        )

        repo_name = group["repo_full_name"].unique()[0]

        logger.debug(f"Write {repo_name} results to {csvfile} ({len(new_df)})")
        # sort by file_sha1 to keep the json ordering consistent across runs
        new_df = new_df.sort_values(by="file_sha1", ascending=True)
        _dump_csv(new_df, csvfile)


def scan_repos_from(json_file):
    # read json to df
    in_df = pd.read_json(json_file)
    if labyrinth.DEBUG:
        # choose from the bottom three quartiles in terms of size
        upper = in_df["size"].quantile(0.75)
        in_df = in_df.loc[(in_df["size"] < upper)].sample(10)

    # start small
    in_df = in_df.sort_values(by="size", ascending=True)
    # get a clean index
    in_df = in_df.reset_index(drop=True)
    # now index is a size rank from small to large
    # reset it again so we get that as a column we can use
    in_df = in_df.reset_index(drop=False)
    # but it's zero based and we want a 1-based counter
    in_df["index"] += 1
    # so now the total is just the max of the index
    in_df["total_repos"] = in_df["index"].max()

    # process it row-wise
    results = in_df.apply(process_row, axis=1).to_list()
    # aggregate results
    df = pd.concat(results)

    if len(df):
        df = df.sort_values(by="match")

    return df


def process_summary(json_file):
    setup_output_dirs()

    df = scan_repos_from(json_file)

    dump_results_by_vul_id(df)
    dump_results_by_repo(df)


def concat_string_fields(df):
    cols2check = [
        "full_name",
        "html_url",
        "description",
        "url",
        "homepage",
    ]
    # concatenate some string columns so we can do a single vul ID pattern match
    # note that this has to be done before we truncate the descriptions in the next step
    _concatenated_strings = (
        df[cols2check].fillna("").applymap(str).agg(" ".join, axis=1)
    )
    return _concatenated_strings
