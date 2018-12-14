#!/usr/bin/env python3

import sys

# Solution to the day 2 puzzle from Advent of Code 2018.
# https://adventofcode.com/2018/day/2

def ids_as_lists(filename):
    """
    Return the IDs in FILENAME as lists of characters, assuming one ID
    per line.
    """
    ids = []
    with open(filename,"r") as f:
        for line in f:
            ids.append(list(line.rstrip()))

    return ids


def difference_count(a,b):
    """ Return the number of differences between A and B. """
    diffs = 0
    z = zip(a,b)
    for x, y in z:
        if x != y:
            diffs += 1

    return diffs


def incremental_ids(ids):
    """ Find two IDs that differ by only one character. """
    matches = tuple()
    for i in range(0,len(ids) - 1):
        for j in range(i + 1,len(ids)):
            if difference_count(ids[i],ids[j]) == 1:
                matches = (''.join(ids[i]),''.join(ids[j]))
                break

    return matches


if __name__ == "__main__":
    if len(sys.argv) == 2:
        ids = ids_as_lists(sys.argv[1])
        print(incremental_ids(ids))
    else:
        print("Usage:  " + sys.argv[0] + " <data-file-name>")

