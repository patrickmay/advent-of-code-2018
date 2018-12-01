#!/usr/bin/env python

import sys

# Solution to the day 1 puzzle from Advent of Code 2018.
# https://adventofcode.com/2018/day/1

def sum_integers_in_file(filename):
    """ Return the sum of the integers in FILENAME, assuming one per line.  """
    sum = 0
    with open(filename,"r") as f:
        for line in f:
            sum += int(line)

    return sum


if __name__ == "__main__":
    if len(sys.argv) == 2:
        print(sum_integers_in_file(sys.argv[1]))
    else:
        print("Usage:  " + sys.argv[0] + " <data-file-name>")

