#!/usr/bin/env python3

import sys

# Solution to part 2 of the day 1 puzzle from Advent of Code 2018.
# https://adventofcode.com/2018/day/1

def integers_from_file(filename):
    """ Return a list of the integers in FILENAME, assuming one per line.  """
    integers = []
    with open(filename,"r") as f:
        for line in f:
            integers.append(int(line))

    return integers


def apply_deltas(start,deltas):
    """ Return a list of the sums of DELTAS starting from START. """
    result = []
    current = start
    for delta in deltas:
        current = current + delta
        result.append(current)

    return result


def first_repeat(values):
    """ Find the first repeating value in VALUES. """
    seen = set()
    repeat = None
    for value in values:
        if value in seen:
            repeat = value
            break
        else:
            seen.add(value)

    return repeat


if __name__ == "__main__":
    if len(sys.argv) == 2:
        deltas = integers_from_file(sys.argv[1])
        start = 0
        frequencies = apply_deltas(start,deltas)
        repeat = None
        while repeat is None:
            repeat = first_repeat(frequencies)
            if repeat is None:
                start = frequencies[-1]
                frequencies += apply_deltas(start,deltas)

        print("First repeated frequency = " + str(repeat))
    else:
        print("Usage:  " + sys.argv[0] + " <data-file-name>")

