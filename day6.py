#!/usr/bin/env python3

import sys
from collections import defaultdict

# Solution to the day 6 puzzle from Advent of Code 2018.
# https://adventofcode.com/2018/day/6

def load_points(filename):
    """ Load the map coordinates from FILENAME into a list of tuples. """
    points = list()
    with open(filename) as f:
        for line in f:
            x, y = line.rstrip().split(' ')
            points.append((int(x.rstrip(',')),int(y)))

    return points


def bounding_box(points):
    """ Return the coordinates for the box that contains all POINTS. """
    min_x = min([point[0] for point in points])
    min_y = min([point[1] for point in points])
    max_x = max([point[0] for point in points])
    max_y = max([point[1] for point in points])

    return [(min_x,min_y),(max_x,max_y)]
            

def manhattan_distance(a, b):
    """ Return the Manhattan distance between points A and B (both tuples). """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def distance_map(points):
    """
    Return an array of all coordinates in the bounding box for POINTS
    containing a list of each point in POINTS and the distance to that
    coordinate, as a tuple.
    """
    map = defaultdict(lambda: defaultdict(lambda: list()))
    bottom_left, top_right = bounding_box(points)
    for i in range(bottom_left[0],top_right[0]):
        for j in range(bottom_left[1],top_right[1]):
            for point in points:
                map[i][j].append((point,manhattan_distance(point,(i,j))))

    return map


def reduce_map(map):
    """
    Reduce the MAP so that each array cell contains only the closest
    points.  (This could be combined with distance_map() for better
    efficiency).
    """
    reduced_map = defaultdict(lambda: defaultdict(lambda: list()))
    for i in map:
        for j in map[i]:
            closest = min([point[1] for point in map[i][j]])
            reduced_map[i][j] = [point for point in map[i][j]
                                 if point[1] == closest]

    return reduced_map


def point_areas(map):
    """
    Return a dict where the key is a point from the MAP and the value is
    the number of coordinates where the point is the unique closest point.
    """
    areas = defaultdict(int)
    for i in map:
        for j in map[i]:
            if len(map[i][j]) == 1:
                point = map[i][j][0][0]
                areas[point] += 1

    return areas

    
def edge_points(points):
    """
    Return a list of coordinates on the edge of the bounding box that
    contains all POINTS.  These are the coordinates that have an infinite
    area.
    """
    bottom_left, top_right = bounding_box(points)
    return [point for point in points
            if (point[0] == bottom_left[0]
                or point[0] == top_right[0]
                or point[1] == bottom_left[1]
                or point[1] == top_right[1])]


if __name__ == "__main__":
    if len(sys.argv) == 2:
        points = load_points(sys.argv[1])
        areas = point_areas(reduce_map(distance_map(points)))
        print(bounding_box(points))
        print(edge_points(points))
        print(str(max(areas, key=lambda k: areas[k]))
              + ", "
              + str(max(areas.values())))
    else:
        print("Usage:  " + sys.argv[0] + " <data-file>")
