#!/usr/bin/env python3

import sys
from collections import defaultdict

# Solution to the day 7 puzzle from Advent of Code 2018.
# https://adventofcode.com/2018/day/7

def parse_steps(filename):
    """
    Read each line of FILENAME and return a dict where the key is the
    step and the value is a list of prerequisite steps.
    """
    steps = defaultdict(lambda: list())
    all_steps = set()
    with open(filename) as f:
        for line in f:
            words = line.split(' ')
            steps[words[7]].append(words[1])
            all_steps.add(words[1])

    # Add steps with no prerequisites.
    for step in all_steps:
        if step not in steps:
            steps[step] = []

    return steps


def remove_prerequisite(steps,prerequisite):
    """
    Return a copy of STEPS with PREREQUISITE removed from both the keys
    and lists of values.
    """
    next_steps = defaultdict(lambda: list())
    for step in steps:
        if step != prerequisite:
            next_steps[step] = [prereq for prereq in steps[step]
                                if prereq != prerequisite]

    return next_steps

    
def traverse_steps(steps):
    """
    Recursively traverse STEPS, returning the string resulting from
    selecting the alphabetically smallest step with no remaining
    prerequisites.
    """
    ordered_steps = ''
    available_steps = [step for step in steps if len(steps[step]) == 0 ]
    if len(available_steps) > 0:
        completed_step = min(available_steps)
        next_steps = remove_prerequisite(steps,completed_step)
        ordered_steps = completed_step + traverse_steps(next_steps)
    
    return ordered_steps


if __name__ == "__main__":
    if len(sys.argv) == 2:
        steps = parse_steps(sys.argv[1])
        print(traverse_steps(steps))
    else:
        print("Usage:  " + sys.argv[0] + " <data-file>")
