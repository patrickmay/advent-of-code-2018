#!/usr/bin/env python3

import sys
from collections import defaultdict

# Solution to the day 5 puzzle from Advent of Code 2018.
# https://adventofcode.com/2018/day/5

def load_polymer(filename):
    """ Return the polymer string from FILENAME. """
    polymer = None
    with open(filename) as f:
        for line in f:
            polymer = line.rstrip()
            break

    return polymer


def reduce_polymer(polymer):
    """ Make one pass through POLYMER removing triggered units. """
    reduced_polymer = ''
    iterator = iter(range(len(polymer)))
    for i in iterator:
        if ((i == len(polymer) - 1)
            or (not (polymer[i] != polymer[i + 1]
                     and polymer[i].lower() == polymer[i + 1].lower()))):
            reduced_polymer += polymer[i]
        else:
            next(iterator)

    return reduced_polymer


if __name__ == "__main__":
    if len(sys.argv) == 2:
        polymer = load_polymer(sys.argv[1])
        length = len(polymer)
        print("Reducing polymer of length " + str(length) + ".")
        polymer = reduce_polymer(polymer)
        while len(polymer) < length:
            length = len(polymer)
            polymer = reduce_polymer(polymer)
        print("The final polymer has length " + str(len(polymer)) + ".")
    else:
        print("Usage:  " + sys.argv[0] + " <data-file>")
