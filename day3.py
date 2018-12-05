#!/usr/bin/env python3

import sys
from collections import defaultdict

# Solution to the day 3 puzzle from Advent of Code 2018.
# https://adventofcode.com/2018/day/3

def parse_claims(filename):
    """
    Read each line of FILENAME and return a dict where the key is a tuple
    containing a coordinate, (x y), and the value is the number of claims
    that include that coordinate.
    """
    coordinates = defaultdict(int)
    with open(filename) as f:
        for line in f:
            claim, at, origin, size = line.split(' ')
            x_start, y_start = origin.rstrip(':').split(',')
            x_range, y_range = size.rstrip().split('x')
            for x in range(int(x_start),int(x_start) + int(x_range)):
                for y in range(int(y_start),int(y_start) + int(y_range)):
                    coordinates[(x, y)] += 1

    return coordinates


def duplicate_count(counts):
    """ Return the number of entries in COUNTS with a value of 2 or more. """
    count = 0
    for v in counts.values():
        if v > 1:
            count += 1

    return count


if __name__ == "__main__":
    if len(sys.argv) == 2:
        coordinate_count = parse_claims(sys.argv[1])
        print("Duplicate count = " + str(duplicate_count(coordinate_count)))
    else:
        print("Usage:  " + sys.argv[0] + " <data-file>")
