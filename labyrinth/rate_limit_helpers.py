#!/usr/bin/env python
"""
file: rate_limit_helpers
author: adh
created_at: 8/12/21 12:54 PM
"""
import datetime
import time
import random


rl_timers = {
    "core": 3600,
    "search": 60,
    "graphql": 3600,
}


def _rl_pause(rlkey, rl, threshold=10):
    """
    If you are too close to a rate limit threshold, take a nap.
    Otherwise just return and go about your day.
    """
    remaining = rl.remaining
    if remaining < (5 * threshold):
        print(f"Rate limit {rlkey} has {remaining} remaining", flush=True)

    if remaining > threshold:
        return

    # how long to wait?
    nap_delta = rl.reset - datetime.datetime.utcnow()
    # nap_delta is a timedelta object
    # .total_seconds() is what you want, beware of .seconds()!!!
    nap_seconds = nap_delta.total_seconds()

    if nap_seconds > 0:
        # it's positive, rl.reset is still in the future
        # but we don't want to go too big
        nap_seconds = min(nap_seconds, rl_timers[rlkey])
    else:
        # it's negative, and rl.reset is already in the past
        # still might be a little out of sync though so
        # take a short nap
        nap_seconds = 1

    # add some jitter up to a minute
    nap_seconds += random.random() * min(60, nap_seconds * 0.1)

    print(
        f"Pausing for {nap_seconds:.1f} to wait for {rlkey} rate limit to catch up ({remaining})",
        flush=True,
    )
    time.sleep(nap_seconds)
    return True


def check_rate_limits(gh, nap_count=0):
    if nap_count > 50:
        raise RuntimeError("Too many naps. Try again when things aren't so busy.")

    limits = {
        "core": gh.get_rate_limit().core,
        "search": gh.get_rate_limit().search,
        "graphql": gh.get_rate_limit().graphql,
    }

    thresh = {"core": 100, "graphql": 100, "search": 5}

    for key, rl in limits.items():
        napped = _rl_pause(key, rl, threshold=thresh[key])
        if napped:
            nap_count += 1
            # we don't know what happened while we were asleep
            return check_rate_limits(gh, nap_count)
