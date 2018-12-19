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
        # for j in range(self.height_[0] - 1,self.height_[1] + 2):
        for j in range(0,self.height_[1] + 2):
            for i in range(self.width_[0] - 1,self.width_[1] + 2):
                if i in self.map_ and j in self.map_[i]:
                    print(self.map_[i][j],end='')
                else:
                    print(".",end='')
            print(" (" + str(j) + ")")

    def flow_left(self,x,y):
        left_drain = None
        leftmost = None

        if x > self.width_[0] and y < self.height_[1]:
            if self.map_[x][y] in ['.','|']:
                self.map_[x][y] = '|'
                if self.map_[x][y + 1] in ['.','|']:
                    left_drain = (x,y)
                    leftmost = x
                elif (x - 1) < self.width_[0] or self.map_[x - 1][y] == '#':
                    leftmost = x
                else:
                    left_drain, leftmost = self.flow_left(x - 1,y)

        return [left_drain,leftmost]
    
    def flow_right(self,x,y):
        right_drain = None
        rightmost = None

        if x <= self.width_[1] and y < self.height_[1]:
            if self.map_[x][y] in ['.','|']:
                self.map_[x][y] = '|'
                if self.map_[x][y + 1] in ['.','|']:
                    right_drain = (x,y)
                    rightmost = x
                elif (x + 1) > self.width_[1] or self.map_[x + 1][y] == '#':
                    rightmost = x
                else:
                    right_drain, rightmost = self.flow_right(x + 1,y)

        return [right_drain,rightmost]
    
    def flow_down(self,start = None):
        if start is None:
            start = self.water_source_
        x, y = start
        drains = set()

        if y < self.height_[1]:
            if self.map_[x][y] in ['+','|']:  # else already written over
                if self.map_[x][y + 1] in ['#','~']:
                    left_drain, leftmost = self.flow_left(x - 1,y)
                    right_drain, rightmost = self.flow_right(x + 1,y)
                    if left_drain is not None:
                        drains.add(left_drain)
                    elif leftmost is None:
                        leftmost = x
                    if right_drain is not None:
                        drains.add(right_drain)
                    elif rightmost is None:
                        rightmost = x
                    if len(drains) == 0:
                        for i in range(leftmost,rightmost + 1):
                            self.map_[i][y] = '~'
                            if self.map_[i][y - 1] == '|':
                                drains.add((i,y - 1))
                elif self.map_[x][y + 1] in ['.','|']:
                    self.map_[x][y + 1] = '|'
                    drains.add((x,y + 1))
            
        return drains

    def flow(self):
        drains = self.flow_down()
        while len(drains) > 0:
            new_drains = set()
            for drain in drains:
                for new_drain in self.flow_down(drain):
                    new_drains.add(new_drain)
            drains = new_drains

    def wet_tiles(self):
        count = 0
        for i in range(self.width_[0],self.width_[1] + 1):
            for j in range(self.height_[0],self.height_[1] + 1):
                if self.map_[i][j] in ['|','~']:
                    count += 1

        return count

    def water_tiles(self):
        count = 0
        for i in range(self.width_[0],self.width_[1] + 1):
            for j in range(self.height_[0],self.height_[1] + 1):
                if self.map_[i][j] == '~':
                    count += 1

        return count


if __name__ == "__main__":
    if len(sys.argv) == 2:
        clay, width, height = parse_clay(sys.argv[1])
        width[0] = 0
        width[1] += 1
        water = (500,0)
        ground_map = GroundMap(width,height,water,clay)
        ground_map.flow()
        print("Water can reach " + str(ground_map.wet_tiles()) + " tiles.")
        print("Water is in " + str(ground_map.water_tiles()) + " tiles.")
    else:
        print("Usage:  " + sys.argv[0] + " <data-file>")
