#!/usr/bin/env python3

import sys
from collections import defaultdict

# Solution to part 2 of the day 4 puzzle from Advent of Code 2018.
# https://adventofcode.com/2018/day/4

def parse_records(filename):
    """
    Read each line of FILENAME and return a dict where the key is the
    guard ID and the value is a list of tuples containing the start and
    stop times of the guard's naps.  FILENAME is assumed to be sorted by
    timestamp.
    """
    naps = defaultdict(lambda: list())
    current_guard = None
    start = None
    with open(filename) as f:
        for line in f:
            columns = line.split(' ')
            minute = int(columns[1].rstrip(']').split(':')[1])
            if columns[2] == 'Guard':
                current_guard = columns[3]
            elif columns[2] == 'falls':
                start = minute
            elif columns[2] == 'wakes':
                naps[current_guard].append((start,minute))

    return naps


def guard_nap_minutes(naps):
    """
    Return a dict where the key is a tuble of guard ID and minute and the
    value is the number of times the guard was napping during that minute.
    """
    nap_minutes = defaultdict(int)
    for guard, naps in naps.items():
        for nap in naps:
            for i in range(nap[0],nap[1]):
                nap_minutes[(guard, i)] += 1

    return nap_minutes


if __name__ == "__main__":
    if len(sys.argv) == 2:
        naps = parse_records(sys.argv[1])
        nap_minutes = guard_nap_minutes(naps)
        print(str(max(nap_minutes, key=lambda k: nap_minutes[k])))
    else:
        print("Usage:  " + sys.argv[0] + " <data-file>")
