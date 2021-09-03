#!/usr/bin/env python
"""
file: search
author: adh
created_at: 8/12/21 3:28 PM
"""
import datetime

import pandas as pd
from github import Github

import labyrinth
from labyrinth.date_helpers import fixup_start_date, fixup_end_date
from labyrinth.rate_limit_helpers import check_rate_limits


def main():
    pass


if __name__ == "__main__":
    main()


def do_search(query, start_date=None, end_date=None, page_size=100):

    start_date = fixup_start_date(start_date)
    end_date = fixup_end_date(end_date)
    # these will be y-m-d strings

    start_dates = pd.date_range(start_date, end_date, freq="7D", tz="utc")
    end_dates = [d + pd.DateOffset(days=6) for d in start_dates]

    end_date_ts = pd.to_datetime(end_date, utc=True)
    if end_dates[-1] > end_date_ts:
        # we overshot end date, so fix that
        end_dates[-1] = end_date_ts

    # convert the timestamps back to our formatted date strings
    fmt_dates = lambda ts_iter: [d.strftime("%Y-%m-%d") for d in ts_iter]
    start_dates = fmt_dates(start_dates)
    end_dates = fmt_dates(end_dates)

    quals = [{"pushed": f"{d1}..{d2}"} for d1, d2 in zip(start_dates, end_dates)]

    print(f"Starting {len(quals)} queries", flush=True)

    if page_size > 100:
        raise ValueError("Github requires page_size <= 100")
    gh = Github(login_or_token=labyrinth.GH_TOKEN, per_page=page_size, retry=2)

    results = []
    for qualifiers in quals:
        check_rate_limits(gh)
        quals = " ".join(f"{k}:{v}" for k, v in qualifiers.items())
        qstr = f"{query} {quals}"

        print(f"Search: {qstr}", flush=True)

        result = gh.search_repositories(
            query, sort="updated", order="asc", **qualifiers
        )

        # result is a generator of repository objects
        count = 0
        for r in result:
            # check your rate limits every so often
            if len(results) % 50 == 0:
                check_rate_limits(gh)

            # timestamp
            ts = (
                datetime.datetime.utcnow()
                .replace(microsecond=0)
                .astimezone(datetime.timezone.utc)
                .isoformat()
            )

            data = r.raw_data

            data["matched_on"] = qstr
            data["matched_at"] = ts
            results.append(data)
            count += 1
        print(f"Found {count} results for {qstr}", flush=True)

    return results
