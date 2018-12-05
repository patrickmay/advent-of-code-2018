#!/usr/bin/env python3

import sys
from collections import defaultdict

# Solution to part 2 of the day 3 puzzle from Advent of Code 2018.
# https://adventofcode.com/2018/day/3

def parse_claims(filename):
    """
    Read each line of FILENAME and return a dict where the key is a tuple
    containing a coordinate, (x y), and the value is a set of the claims
    that include that coordinate.
    """
    coordinates = defaultdict(lambda: set())
    with open(filename) as f:
        for line in f:
            claim, at, origin, size = line.split(' ')
            x_start, y_start = origin.rstrip(':').split(',')
            x_range, y_range = size.rstrip().split('x')
            for x in range(int(x_start),int(x_start) + int(x_range)):
                for y in range(int(y_start),int(y_start) + int(y_range)):
                    coordinates[(x, y)].add(claim)

    return coordinates


def non_overlapping_claims(claims):
    """ Return a list of all claims that don't overlap with others. """
    unique_claims = set()
    non_unique_claims = set()
    for v in claims.values():
        if len(v) == 1:
            unique_claims = unique_claims.union(v)
        else:
            non_unique_claims = non_unique_claims.union(v)

    return unique_claims.difference(non_unique_claims)
            

if __name__ == "__main__":
    if len(sys.argv) == 2:
        coordinate_claims = parse_claims(sys.argv[1])
        print("Unique claims = "
              + str(non_overlapping_claims(coordinate_claims)))
    else:
        print("Usage:  " + sys.argv[0] + " <data-file>")
