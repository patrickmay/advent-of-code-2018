#!/usr/bin/env python3.7

import sys
from blist import blist
from collections import defaultdict

# Solution to the day 9 puzzle from Advent of Code 2018.
# https://adventofcode.com/2018/day/9

def parse_data(filename):
    """ Load the data from FILENAME. """
    data = list()

    with open(filename) as f:
        elements = f.readline().rstrip().split(' ')
        data = [int(elements[0]), int(elements[6])]

    return data


if __name__ == "__main__":
    if len(sys.argv) == 2:
        players, marbles = parse_data(sys.argv[1])
        current_player = 0
        board = blist([0])
        current_marble = 0
        scores = defaultdict(int)
        for i in range(marbles):
            marble_value = i + 1
            if marble_value % 23 == 0:
                current_marble = (current_marble - 7) % len(board)
                scores[current_player] += (marble_value
                                           + board.pop(current_marble))
            else:
                current_marble = ((current_marble + 1) % len(board)) + 1
                board.insert(current_marble,marble_value)
            current_player = (current_player + 1) % players
                
        print("For "
              + str(players)
              + " players with "
              + str(marbles)
              + " marbles, the high score is "
              + str(max(scores.values()))
              + ".")
    else:
        print("Usage:  " + sys.argv[0] + " <data-file>")
