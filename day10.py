#!/usr/bin/env python3

import sys
from collections import defaultdict

# Solution to the day 10 puzzle from Advent of Code 2018.
# https://adventofcode.com/2018/day/10

def parse_data(filename):
    """
    Load the position and velocity data from FILENAME into a dict where
    the key is a tuple containing the initial position and the value is a
    tuple containing the velocity.
    """
    data = defaultdict(lambda: tuple())

    with open(filename) as f:
        for line in f:
            position = line[line.find('<') + 1:line.find('>')].split(',')
            line = line[line.find('velocity'):]
            velocity = line[line.find('<') + 1:line.find('>')].split(',')

            position = [int(p.strip()) for p in position]
            velocity = [int(v.strip()) for v in velocity]
            data[tuple(position)] = tuple(velocity)

    return data


if __name__ == "__main__":
    if len(sys.argv) == 2:
        points = parse_data(sys.argv[1])
        min_x = min([v[0] for v in points])
        max_x = max([v[0] for v in points])
        min_y = min([v[1] for v in points])
        max_y = max([v[1] for v in points])
        print(min_x)
        print(max_x)
        print(min_y)
        print(max_y)

        # Each letter is 8 points high and 3-5 points wide with two empty
        # points between.  There are 313 points in total, so the message
        # can't have more than 24 characters (probably fewer).  If
        # they're all on one line, that means the y axis can't be more
        # than 168 points wide.  We can therefore only print out the point
        # maps where that is true.
        i = 0
        positions = [p for p in points]
        #while (max_y - min_y) > 273:
        while ((max_x - min_x) * (max_y - min_y)) > ((313 / (8 * 3)) * (10 * 7)):
            positions = [(p[0] + (i * points[p][0]),p[1] + (i * points[p][1]))
                         for p in points]
            min_x = min([p[0] for p in positions])
            max_x = max([p[0] for p in positions])
            min_y = min([p[1] for p in positions])
            max_y = max([p[1] for p in positions])
            i += 1

        print("Dimensions after "
              + str(i)
              + " seconds:  ("
              + str(min_x)
              + ", "
              + str(min_y)
              + "), ("
              + str(max_x)
              + ", "
              + str(max_y)
              + ")")
        for y in range(min_y,max_y + 1):
            output = ""
            for x in range(min_x,max_x + 1):
                if (x,y) in positions:
                    output += "#"
                else:
                    output += "."
            print(output)
    else:
        print("Usage:  " + sys.argv[0] + " <data-file>")
