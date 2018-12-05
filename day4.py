#!/usr/bin/env python3

import sys
from collections import defaultdict

# Solution to the day 4 puzzle from Advent of Code 2018.
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


def most_minutes_asleep(naps):
    """ Return the ID of the guard who naps the most. """
    most_minutes = 0
    sleepiest = None
    for guard, recorded_naps in naps.items():
        total = 0
        for nap in recorded_naps:
            total += nap[1] - nap[0]
        if total > most_minutes:
            most_minutes = total
            sleepiest = guard

    return sleepiest


def most_asleep_minute(naps):
    """ Return the minute that appears in the most ranges of NAPS. """
    minutes = defaultdict(int)
    for nap in naps:
        for i in range(nap[0],nap[1]):
            minutes[i] += 1

    return max(minutes, key=lambda k: minutes[k])

    
if __name__ == "__main__":
    if len(sys.argv) == 2:
        naps = parse_records(sys.argv[1])
        sleepiest_guard = most_minutes_asleep(naps)
        print("Guard "
              + sleepiest_guard
              + " is most often asleep during minute "
              + str(most_asleep_minute(naps[sleepiest_guard]))
              + ".")
    else:
        print("Usage:  " + sys.argv[0] + " <data-file>")
