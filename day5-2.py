#!/usr/bin/env python3

import sys
from collections import defaultdict

# Solution to part 2 of the day 5 puzzle from Advent of Code 2018.
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


def fully_reduce_polymer(polymer):
    """ Remove all triggered units from POLYMER until none remain. """
    length = len(polymer)
    polymer = reduce_polymer(polymer)
    while len(polymer) < length:
        length = len(polymer)
        polymer = reduce_polymer(polymer)

    return len(polymer)


def length_without_unit(polymer,unit):
    """
    Return the length of the fully reduced POLYMER after removing all
    instances of UNIT.
    """
    short_polymer = polymer.replace(unit.lower(),'').replace(unit.upper(),'')
    return fully_reduce_polymer(short_polymer)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        polymer = load_polymer(sys.argv[1])
        letters = "abcdefghijklmnopqrstuvwxyz"
        counts = defaultdict(int)
        for letter in letters:
            print("Processing " + letter.upper() + "...")
            counts[letter] = length_without_unit(polymer,letter)
        print(str(min(counts, key=lambda k: counts[k])))
        print(str(min(counts.values())))
    else:
        print("Usage:  " + sys.argv[0] + " <data-file>")
