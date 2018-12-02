#!/usr/bin/env python3

import sys
from collections import Counter

# Solution to the day 2 puzzle from Advent of Code 2018.
# https://adventofcode.com/2018/day/2

def count_exists(id,count):
    """
    Return True if the ID contains exactly COUNT instances of any letter.
    """
    exists = False
    counts = Counter(list(id))
    for c in counts.values():
        if c == count:
            exists = True
            break

    return exists
    

def checksum_from_file(filename):
    """
    Return the checksum, computed as the product of the number of IDs
    having exactly two of any letter and the number of IDs having exactly
    three of any letter, from the IDs in FILENAME, assuming one ID per
    line.
    """
    exactly_two = 0
    exactly_three = 0
    with open(filename,"r") as f:
        for line in f:
            if count_exists(line,2):
                exactly_two += 1
            if count_exists(line,3):
                exactly_three += 1

    return exactly_two * exactly_three


if __name__ == "__main__":
    if len(sys.argv) == 2:
        print(checksum_from_file(sys.argv[1]))
    else:
        print("Usage:  " + sys.argv[0] + " <data-file-name>")

