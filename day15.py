#!/usr/bin/env python3

import sys
from collections import defaultdict

# Solution to the day 15 puzzle from Advent of Code 2018.
# https://adventofcode.com/2018/day/15

class Combatant:
    def __init__(self,id,location,cave_map):
        self.id_ = id
        self.location_ = location
        self.map_ = cave_map
        self.hit_points_ = 200
        self.attack_power_ = 3

    def id(self):
        return self.id_

    def location(self):
        return self.location_

    def x(self):
        return self.location_[0]

    def y(self):
        return self.location_[1]

    def targets(self):
        # Return a list of all targets in the list.
        return [combatant for combatant in self.map_.combatants()
                if combatant.id() != self.id_]

    def target_adjacent_squares(self):
        # Return a list of all open squares near a target.
        open_squares = list()
        target_squares = [combatant.location() for combatant in self.targets()]
        for square in target_squares:
            for neighbor in self.map_.unoccupied_neighbors(square[0],square[1]):
                open_squares.append(neighbor)

        return open_squares

    def attack(self):
        pass

    def distance_matrix(self,
                        coordinate,
                        distance = 0,
                        matrix = defaultdict(lambda: defaultdict())):
        # Return a matrix with the distances to COORDINATE from this
        # combatant's location.
        print("distance_matrix:  " + str(coordinate) + ", " + str(distance))
        x, y = coordinate
        if (distance != 0) and (self.map_.value(x,y) != '.'):
            matrix[x][y] = None
        elif ((not (x in matrix and y in matrix[x]))
              or (matrix[x][y] is None)
              or (matrix[x][y] > distance)):
            matrix[x][y] = distance
            for neighbor in self.map_.unoccupied_neighbors(x,y):
                matrix = self.distance_matrix(neighbor,distance + 1,matrix)

        print("Distances for " + str(coordinate)
              + " (starting = " + str(distance) + ")")
        for i in matrix:
            for j in matrix[i]:
                print(str((i, j)) + ":  " + str(matrix[i][j]))
        return matrix
                
    def move(self):
        # If next to a target, attack.  Otherwise, move toward the
        # nearest target.
        target_squares = self.target_adjacent_squares()
        print("Target squares = " + str(target_squares))
        if self.location_ in target_squares:
            self.attack()
        else:
            distances = [self.distance_matrix(square)
                         for square in target_squares]
            path_starts = self.map_.unoccupied_neighbors(self.x(),self.y())
            next_location = None
            shortest_path = -1
            sorted_starts = sorted(path_starts,
                                   key=lambda start: tuple(reversed(start)))
            print("Start squares = " + str(sorted_starts))
            for start in sorted_starts:
                for matrix in distances:
                    x, y = start
                    if ((x in matrix) and (y in matrix[x])
                        and matrix[x][y] is not None):
                        print("Start = " + str(start))
                        print("Matrix distance = " + str(matrix[x][y]))
                        if ((shortest_path == -1)
                            or (matrix[x][y] < shortest_path)):
                            next_location = start
                            shortest_path = matrix[x][y]
            if next_location is not None:
                print("Moving from " + str(self.location_) + " to " + str(next_location) + " (distance = " + str(shortest_path) + ")")
                self.location_ = next_location
                if self.location_ in target_squares:
                    self.attack()
            
            
class Elf(Combatant):
    def __init__(self,location,starting_map):
        super().__init__('E',location,starting_map)
        

class Goblin(Combatant):
    def __init__(self,location,starting_map):
        super().__init__('G',location,starting_map)
        

class Map:
    def __init__(self):
        self.map_ = defaultdict(lambda: defaultdict())
        self.combatants_ = list()
        
    def value(self,x,y):
        symbol = self.map_[x][y]
        combatant = [combatant for combatant in self.combatants_
                     if combatant.location() == (x,y)]
        if len(combatant) == 1:
            symbol = combatant[0].id()
        
        return symbol

    def combatants(self):
        # Return the list of combatants in order of location (left-right,
        # up-down).
        self.combatants_ = sorted(self.combatants_,
                                  key=lambda combatant:
                                  tuple(reversed(combatant.location())))
        return self.combatants_

    def set_coordinate(self,x,y,value):
        self.map_[x][y] = value

    def add_combatant(self,combatant):
        self.combatants_.append(combatant)
    
    def remove_combatant(self,combatant):
        pass
    
    def display(self):
        # Print the contents of the Map to the screen.
        for y in range(len(self.map_[0])):
            for x in range(len(self.map_)):
                print(self.value(x,y),end='')
            print()

    def open_neighbors(self,x,y):
        # Return a list of neighboring coordinates that aren't walls.
        neighbors = list()
        if x in self.map_ and y in self.map_[x]:
            if self.map_[x][y - 1] != '#':
                neighbors.append((x,y - 1))
            if self.map_[x + 1][y] != '#':
                neighbors.append((x + 1,y))
            if self.map_[x][y + 1] != '#':
                neighbors.append((x,y + 1))
            if self.map_[x - 1][y] != '#':
                neighbors.append((x - 1,y))
                
        return neighbors

    def unoccupied_neighbors(self,x,y):
        # Return a list of neighboring coordinates that are open floor.
        neighbors = list()
        if x in self.map_ and y in self.map_[x]:
            if self.value(x,y - 1) == '.':
                neighbors.append((x,y - 1))
            if self.value(x + 1,y) == '.':
                neighbors.append((x + 1,y))
            if self.value(x,y + 1) == '.':
                neighbors.append((x,y + 1))
            if self.value(x - 1,y) == '.':
                neighbors.append((x - 1,y))
                
        return neighbors


def parse_starting_map(filename):
    """
    Load the map and combatants from FILENAME.  Maps are assumed to be
    rectangular.
    """
    starting_map = Map()

    with open(filename) as f:
        line_number = 0
        for line in f:
            line = line.rstrip()
            if line[0] != ';':  # ignore comments
                for i in range(len(line)):
                    if line[i] == 'E':
                        starting_map.add_combatant(Elf((i,line_number),
                                                       starting_map))
                        starting_map.set_coordinate(i,line_number,'.')
                    elif line[i] == 'G':
                        starting_map.add_combatant(Goblin((i,line_number),
                                                          starting_map))
                        starting_map.set_coordinate(i,line_number,'.')
                    else:
                        starting_map.set_coordinate(i,line_number,line[i])
                line_number += 1

    return starting_map


if __name__ == "__main__":
    if len(sys.argv) == 2:
        starting_map = parse_starting_map(sys.argv[1])
        starting_map.display()
        print("Combatant locations:")
        print([combatant.location() for combatant in starting_map.combatants()])

        for combatant in starting_map.combatants():
            combatant.move()
        starting_map.display()

        print([combatant.location() for combatant in starting_map.combatants()])
        for combatant in starting_map.combatants():
            print("Moving combatant at " + str(combatant.location()))
            combatant.move()
        starting_map.display()
        
        print([combatant.location() for combatant in starting_map.combatants()])
        for combatant in starting_map.combatants():
            combatant.move()
        starting_map.display()
    else:
        print("Usage:  " + sys.argv[0] + " <data-file>")
