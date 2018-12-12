#!/usr/bin/env python3

import sys
from collections import defaultdict

# Solution to the day 12 puzzle from Advent of Code 2018.
# https://adventofcode.com/2018/day/12

def parse_data(filename):
    """ Load the data from FILENAME. """
    initial_state = None
    rules = defaultdict()
    
    with open(filename) as f:
        initial_state = f.readline().rstrip().split(' ')[2]
        f.readline()  # get the blank line
        for line in f:
            elements = line.rstrip().split(' ')
            rules[elements[0]] = elements[2]

    return [initial_state,rules]


def next_generation(state,rules):
    """ Return the string that results from applying RULES to STATE. """
    next_state = ''
    for i in range(2,len(state) - 2):
        pattern = state[i - 2:i + 3]
        if pattern in rules:
            next_state += rules[pattern]
        else:
            next_state += '.'

    return '..' + next_state + '..'


if __name__ == "__main__":
    if len(sys.argv) == 2:
        initial_state, rules = parse_data(sys.argv[1])
        state = ('.' * 20) + initial_state + ('.' * 20)
        #print("0:  " + state)
        for i in range(20):
            state = next_generation(state,rules)
            #print(str(i + 1) + ":  " + state)

        plant_sum = 0
        for i in range(len(state)):
            if state[i] == '#':
                plant_sum += i - 20

        print(plant_sum)
    else:
        print("Usage:  " + sys.argv[0] + " <data-file>")
