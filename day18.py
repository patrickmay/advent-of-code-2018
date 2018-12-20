#!/usr/bin/env python3

import sys
from collections import defaultdict

# Solution to the day 18 puzzle from Advent of Code 2018.
# https://adventofcode.com/2018/day/18

class LumberYard:
    def __init__(self,filename):
        self.map_ = defaultdict(lambda: defaultdict())
        with open(filename) as f:
            y = 0
            for line in f:
                for x in range(len(line.rstrip())):
                    self.map_[x][y] = line[x]
                y += 1
        self.width_ = len(self.map_[0])
        self.height_ = len(self.map_)

    def width(self):
        return self.width_

    def height(self):
        return self.height_

    def count_acres(self,state):
        count = 0
        for x in range(self.width_):
            for y in range(self.height_):
                if self.map_[x][y] == state:
                    count += 1

        return count

    def open_acres(self):
        return self.count_acres('.')

    def wooded_acres(self):
        return self.count_acres('|')

    def lumberyards(self):
        return self.count_acres('#')
    
    def display(self):
        for y in range(self.height_):
            for x in range(self.width_):
                print(self.map_[x][y],end='')
            print()

    def neighbors(self,x,y):
        states = list()
        for i in range(x - 1,x + 2):
            for j in range(y - 1,y + 2):
                if (i in self.map_ and j in self.map_[i]
                    and not (i == x and j == y)):
                    states.append(self.map_[i][j])

        return states
    
    def apply_rules(self,x,y):
        current = self.map_[x][y]
        states = self.neighbors(x,y)
        if current == '.':
            if states.count('|') >= 3:
                current = '|'
        elif current == '|':
            if states.count('#') >= 3:
                current = '#'
        elif current == '#':
            if not ('|' in states and '#' in states):
                current = '.'

        return current

    def increment(self):
        next_map = defaultdict(lambda: defaultdict())
        for x in range(self.width_):
            for y in range(self.height_):
                next_map[x][y] = self.apply_rules(x,y)
        self.map_ = next_map


if __name__ == "__main__":
    if len(sys.argv) == 3:
        yard = LumberYard(sys.argv[1])
        minutes = int(sys.argv[2])
        yard.display()
        for i in range(minutes):
            yard.increment()
        print()
        yard.display()
        print("Resource value = "
              + str(yard.wooded_acres() * yard.lumberyards()))
    else:
        print("Usage:  " + sys.argv[0] + " <map-file> <minutes>")
