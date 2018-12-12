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


def plant_sum(state,offset):
    plant_sum_ = 0
    for i in range(len(state)):
        if state[i] == '#':
            plant_sum_ += i - offset

    return plant_sum_


if __name__ == "__main__":
    if len(sys.argv) == 2:
        initial_state, rules = parse_data(sys.argv[1])
        state = ('.' * 20) + initial_state + ('.' * 10000)
        #print(" 0:  " + state)
        for i in range(5000):
            state = next_generation(state,rules)
            if (i + 1) % 100 == 0:
                print("Gen "
                      + str(i + 1)
                      + ":  # of plants = "
                      + str(state.count('#'))
                      + ", leftmost = "
                      + str(state.index('#') - 20)
                      + ", rightmost = "
                      + str(state.rindex('#') - 20)
                      + ", sum = "
                      + str(plant_sum(state,20)))
    else:
        print("Usage:  " + sys.argv[0] + " <data-file>")
