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

    def hit_points(self):
        return self.hit_points_

    def damage(self,amount):
        self.hit_points_ -= amount
        if self.hit_points_ <= 0:
            self.map_.cull()

    def targets(self):
        # Return a list of all targets in the list.
        return [combatant for combatant in self.map_.combatants()
                if combatant.id() != self.id_]

    def target_adjacent_squares(self):
        # Return a list of all open squares near a target.
        open_squares = list()
        target_squares = [combatant.location() for combatant in self.targets()]
        for square in target_squares:
            for neighbor in self.map_.open_neighbors(square[0],square[1]):
                open_squares.append(neighbor)

        return open_squares

    def attack(self):
        # Attack the adjacent target with the fewest hit points.
        adjacent_squares = self.map_.open_neighbors(self.x(),self.y())
        targets = [target for target in self.targets()
                   if (target.location() in adjacent_squares
                       and target.id() != self.id_)]
        if len(targets) > 0:
            targets.sort(key=lambda target: target.hit_points())
            targets = [target for target in targets
                       if target.hit_points() == targets[0].hit_points()]
            targets.sort(key=lambda target: tuple(reversed(target.location())))
            target = targets[0]
            target.damage(self.attack_power_)

    def distance_matrix(self,coordinate):
        # Return a matrix with the distances to COORDINATE from this
        # combatant's location.  Uses BFS to traverse all reachable
        # squares.
        matrix = defaultdict(lambda: defaultdict())
        distance = 0
        seen = set()
        remaining = defaultdict(lambda: list())
        remaining[0].append(coordinate)
        while remaining[distance]:
            next = remaining[distance].pop()
            if (not (next in seen)):
                matrix[next[0]][next[1]] = distance
                seen.add(next)
                remaining[distance + 1].extend(self.map_.unoccupied_neighbors(next[0],next[1]))
            if not remaining[distance]:
                distance += 1
                
        return matrix

    def next_location(self,target_squares):
        # Calculate the next location for this combatant based on the
        # distance to the TARGET_SQUARES.
        location = None

        # Clean up target squares.
        target_squares = [square for square in target_squares
                          if self.map_.value(square[0],square[1]) == '.']

        # Order the target squares left-right / up-down.
        target_squares.sort(key=lambda target: tuple(reversed(target)))

        # Find the open squares around the current location.
        path_starts = self.map_.unoccupied_neighbors(self.x(),self.y())
        if len(path_starts) > 0:
            # Order the path starts left-right / up-down.
            path_starts.sort(key=lambda start: tuple(reversed(start)))

            # Find the shortest distance to any of the path starts in the
            # distance matrix with the lowest index.
            shortest = -1
            for square in target_squares:
                distance = self.distance_matrix(square)
                    
                for start in path_starts:
                    x, y = start
                    if ((x in distance and y in distance[x])
                        and (shortest == -1
                             or distance[x][y] < shortest)):
                        shortest = distance[x][y]
                        location = start
            
        return location
        
    def move(self):
        # If next to a target, attack.  Otherwise, move toward the
        # nearest target.  If no targets are found, return False.
        target_count = sum([1 for combatant in self.map_.combatants()
                            if combatant.id() != self.id_])
        if target_count > 0:
            target_squares = self.target_adjacent_squares()
            if len(target_squares) > 0:
                if self.location_ in target_squares:
                    self.attack()
                else:
                    move_to = self.next_location(target_squares)
                    if move_to is not None:
                        self.location_ = move_to
                        if self.location_ in target_squares:
                            self.attack()
                    
        return (target_count > 0)
            
            
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

    def width(self):
        return len(self.map_)

    def height(self):
        return len(self.map_[0])

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
    
    def cull(self):
        # Remove dead combatants
        self.combatants_ = [combatant for combatant in self.combatants_
                            if combatant.hit_points() > 0]
    
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


# For the test data, this should give 76 rounds with 2656 hit points
# remaining for a score of 201856.
if __name__ == "__main__":
    if len(sys.argv) == 3:
        cave_map = parse_starting_map(sys.argv[1])
        elf_attack_power = int(sys.argv[2])
        starting_elves = 0
        for combatant in cave_map.combatants():
            if combatant.id() == 'E':
                combatant.attack_power_ = elf_attack_power
                starting_elves += 1
        round = 0
        done = False
        while not done:
            for combatant in cave_map.combatants():
                if combatant.hit_points() > 0:
                    if not combatant.move():
                        done = True
                        break
            if not done:
                round += 1
            print("Round " + str(round) + " complete.")
            
        remaining_hit_points = sum([combatant.hit_points()
                                    for combatant in cave_map.combatants()])
        print("Combat ended after "
              + str(round)
              + " rounds.  The winning group has "
              + str(remaining_hit_points)
              + " hit points remaining ("
              + str(round * remaining_hit_points)
              + ").")
        print("Lost "
              + str(starting_elves
                    - sum([1 for combatant in cave_map.combatants()
                           if combatant.id() == 'E']))
              + " elves.")
    else:
        print("Usage:  " + sys.argv[0] + " <data-file> <elf-attack-power>")
