#!/usr/bin/env python3

import sys
from collections import defaultdict

# Solution to the day 20 puzzle from Advent of Code 2018.
# https://adventofcode.com/2018/day/20

class DirectionTree:
    # A tree of directions.
    def __init__(self,regex):
        self.regex_ = regex
        self.path_ = ''
        self.next_paths_ = list()
        self.map_ = defaultdict(lambda: defaultdict())
        self.top_left_ = (0,0)
        self.bottom_right_ = (0,0)

    def parse_regex(self):
        # Parse the regex, which starts with either '^' or '(', and
        # return the number of characters consumed.
        count = 0
        if self.regex_[count] == '^':
            # print(self.regex_)
            count = 1
            while self.regex_[count] != '$':
                node = DirectionTree(self.regex_[count:])
                count += node.parse_regex()
                self.next_paths_.append(node)
            count += 1
        elif self.regex_[count] == '(':
            # print(self.regex_)
            count = 1
            while self.regex_[count] != ')':
                node = DirectionTree(self.regex_[count:])
                count += node.parse_regex()
                self.next_paths_.append(node)
            count += 1
        elif self.regex_[count] in ['N','S','E','W','|']:
            # print(self.regex_)
            while self.regex_[count] in ['N','S','E','W','|']:
                self.path_ += self.regex_[count]
                count += 1
                # print(self.path_)
        else:
            print("Error parsing regex.")
            
        return count

    def neighbors(self,x,y):
        return [(x,y - 1),(x + 1,y),(x,y + 1),(x - 1,y)]
    
    def corners(self,x,y):
        return [(x - 1,y - 1),(x + 1,y - 1),(x + 1,y + 1),(x - 1,y + 1)]

    def update_dimensions(self,x,y):
        new_x = self.top_left_[0]
        new_y = self.top_left_[1]
        if x < new_x:
            new_x = x
        if y < new_y:
            new_y = y
        self.top_left_ = (new_x,new_y)

        new_x = self.bottom_right_[0]
        new_y = self.bottom_right_[1]
        if x > new_x:
            new_x = x
        if y > new_y:
            new_y = y
        self.bottom_right_ = (new_x,new_y)

    def initialize_map(self):
        self.map_[0][0] = 'X'
        for neighbor in self.neighbors(0,0):
            i, j = neighbor
            self.map_[i][j] = '?'
            self.update_dimensions(i,j)
        for corner in self.corners(0,0):
            i, j = corner
            self.map_[i][j] = '#'
            self.update_dimensions(i,j)

    def map_neighbors(self,x,y):
        for neighbor in self.neighbors(x,y):
            i, j = neighbor
            if (not (i in self.map_ and j in self.map_[i])):
                self.map_[i][j] = '?'
                self.update_dimensions(i,j)
        for corner in self.corners(x,y):
            self.map_[corner[0]][corner[1]] = '#'
            self.update_dimensions(neighbor[0],neighbor[1])

    def set_map_cell(self,x,y,value,overwrite = None):
        if overwrite is None:
            overwrite = False

        if (overwrite or (not (x in self.map_ and y in self.map_[y]))):
            self.map_[x][y] = value

    def map_path(self,path,coordinates):
        ends = list()
        x, y = coordinates
        for i in range(len(path)):
            if path[i] == 'E':
                x += 1
                self.set_map_cell(x,y,'|')
                x += 1
                self.set_map_cell(x,y,'.')
                self.map_neighbors(x,y)
            elif path[i] == 'N':
                y -= 1
                self.set_map_cell(x,y,'-')
                y -= 1
                self.set_map_cell(x,y,'.')
                self.map_neighbors(x,y)
            elif path[i] == 'S':
                y += 1
                self.set_map_cell(x,y,'-')
                y += 1
                self.set_map_cell(x,y,'.')
                self.map_neighbors(x,y)
            elif path[i] == 'W':
                x -= 1
                self.set_map_cell(x,y,'|')
                x -= 1
                self.set_map_cell(x,y,'.')
                self.map_neighbors(x,y)
            elif path[i] == '|':
                ends.append((x,y))
                x, y = coordinates
        ends.append((x,y))
        
        return ends
            
    def create_map(self,node = None,starting = None):
        if (node is None and starting is None):
            node = self
            starting = [(0,0)]
            self.initialize_map()

        endings = starting
        for coordinates in starting:
            x, y = coordinates
            if len(node.path_) > 0:
                endings = self.map_path(node.path_,coordinates)
                print("path endings = " + str(endings))
            else:
                for next in node.next_paths_:
                    endings = (self.create_map(next,endings))
                    print("node endings = " + str(endings))
                    
        return endings

    def display_map(self):
        print("display_map:  "
              + str(self.top_left_)
              + ", "
              + str(self.bottom_right_))
        for j in range(self.top_left_[1],self.bottom_right_[1] + 1):
            for i in range(self.top_left_[0],self.bottom_right_[0] + 1):
                if (i in self.map_ and j in self.map_[i]):
                    print(self.map_[i][j],end='')
                else:
                    print(" ",end='')
            print()
                    
    def display(self,indent = None):
        if indent is None:
            indent = ""
        if len(self.path_) > 0:
            print(indent,end='')
            print(self.path_)
        else:
            print(indent,end='')
            print(".")
            indent += "  "
            for path in self.next_paths_:
                path.display(indent)
            

def parse_directions(filename):
    """ Load the direction string from FILENAME. """
    # Rooms = '.', walls = '#', doors = '|' or '-'.
    # Current position = 'X'.
    # Rooms are size 1.
    # Movement is possible only through doors.
    # Start = '^', end = '$'.
    # Parenthesis containing a final '|', e.g. (NEWS|) mean that the
    # branch could be skipped entirely.
    directions = ''

    with open(filename) as f:
        directions = f.readline().rstrip()

    return directions


if __name__ == "__main__":
    if len(sys.argv) == 2:
        regex = parse_directions(sys.argv[1])
        directions = DirectionTree(regex)
        directions.parse_regex()
        directions.display()
        directions.create_map()
        directions.display_map()
    else:
        print("Usage:  " + sys.argv[0] + " <data-file>")
