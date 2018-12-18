#!/usr/bin/env python3

import sys
from collections import defaultdict

# Solution to the day 17 puzzle from Advent of Code 2018.
# https://adventofcode.com/2018/day/17

def parse_clay(filename):
    """
    Load the clay veins from FILENAME into a set of tuples.  Return the
    maximum width and height as well as the clay data.
    """
    # x=452, y=1077..1087
    clay = set()
    width = [None, None]
    height = [None, None]
    
    with open(filename) as f:
        for line in f:
            fixed, spread = line.rstrip().split(' ')
            if fixed[0] == 'x':
                x = int(fixed[2:-1])
                y_start, y_end = [int(y) for y in spread[2:].split('..')]
                if width[0] is None or width[0] > x:
                    width[0] = x
                if width[1] is None or width[1] < x:
                    width[1] = x
                if height[0] is None or height[0] > y_start:
                    height[0] = y_start
                if height[1] is None or height[1] < y_end:
                    height[1] = y_end
                for y in range(y_start,y_end + 1):
                    clay.add((x,y))
            else:
                y = int(fixed[2:-1])
                x_start, x_end = [int(x) for x in spread[2:].split('..')]
                if width[0] is None or width[0] > x_start:
                    width[0] = x_start
                if width[1] is None or width[1] < x_end:
                    width[1] = x_end
                if height[0] is None or height[0] > y:
                    height[0] = y
                if height[1] is None or height[1] < y:
                    height[1] = y
                for x in range(x_start,x_end + 1):
                    clay.add((x,y))

    return [clay, width, height]


class GroundMap:
    def __init__(self,width,height,water_source,clay):
        self.width_ = width
        self.height_ = height
        self.water_source_ = water_source
        self.map_ = defaultdict(lambda: defaultdict())
        
        #for j in range(self.height_[0],self.height_[1] + 1):
        for j in range(0,self.height_[1] + 1):
            for i in range(self.width_[0] - 1,self.width_[1] + 1):
                if (i, j) in clay:
                    self.map_[i][j] = '#'
                elif (i, j) == self.water_source_:
                    self.map_[i][j] = '+'
                else:
                    self.map_[i][j] = '.'

    def display(self):
        for j in range(self.height_[0] - 1,self.height_[1] + 2):
            for i in range(self.width_[0] - 1,self.width_[1] + 2):
                if i in self.map_ and j in self.map_[i]:
                    print(self.map_[i][j],end='')
                else:
                    print(".",end='')
                    
            print()

    def flow_left(self,x,y):
        if x - 1 >= self.width_[0]:
            if self.map_[x - 1][y] == '.':
                if self.map_[x - 1][y + 1] in ['#','~']:
                    self.map_[x - 1][y] = '~'
                    self.flow_left(x - 1,y)
                else:
                    self.map_[x - 1][y] = '|'

    def flow_right(self,x,y):
        if x + 1 <= self.width_[1]:
            if self.map_[x + 1][y] == '.':
                if self.map_[x + 1][y + 1] in ['#','~']:
                    self.map_[x + 1][y] = '~'
                    self.flow_right(x + 1,y)
                else:
                    self.map_[x + 1][y] = '|'
    
    def flow_down(self,x = None,y = None,seen = None):
        if x is None and y is None:
            x, y = list(self.water_source_)
        if seen is None:
            seen = set()
        flowed = True

        if (x,y) in seen:
            flowed = False
        elif y < self.height_[1] and self.map_[x][y + 1] in ['#','~']:
            seen.add((x,y))
            if self.map_[x][y] in ['.','|']:
                self.map_[x][y] = '~'
            self.flow_left(x,y)
            self.flow_right(x,y)
        elif y < self.height_[1]:
            seen.add((x,y))
            self.map_[x][y + 1] = '|'
            self.flow_down(x,y + 1,seen)
        else:
            flowed = False

        return flowed

    def flowing_water(self):
        flowing = list()
        for i in range(self.width_[0],self.width_[1] + 1):
            for j in range(self.height_[0],self.height_[1] + 1):
                if self.map_[i][j] == '|':
                    flowing.append((i,j))

        return flowing
    
    def flow(self):
        done = False
        while not done:
            self.flow_down()
            flowing = self.flowing_water()
            flowing.sort(key=lambda flow: tuple(reversed(flow)),reverse=True)
            lowest = flowing[0][1]  # largest y coordinate
            flowing = [flow for flow in flowing if flow[1] == lowest]
            results = list()
            for flow in flowing:
                results.append(self.flow_down(flow[0],flow[1]))
            done = True not in results


if __name__ == "__main__":
    if len(sys.argv) == 2:
        clay, width, height = parse_clay(sys.argv[1])
        water = (500,0)
        print(len(clay))
        print(width)
        print(height)
        ground_map = GroundMap(width,height,water,clay)
        ground_map.display()
        print()
        ground_map.flow()
        ground_map.display()
    else:
        print("Usage:  " + sys.argv[0] + " <data-file>")
