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
    containing the sum of distances to all points in POINTS.
    """
    map = defaultdict(lambda: defaultdict(int))
    bottom_left, top_right = bounding_box(points)
    for i in range(bottom_left[0],top_right[0]):
        for j in range(bottom_left[1],top_right[1]):
            for point in points:
                map[i][j] += manhattan_distance(point,(i,j))

    return map


def reduce_map(map,distance):
    """
    Reduce the MAP to produce a list of all coordinates that have a total
    distance less than or equal to DISTANCE.
    """
    reduced_map = list()
    for i in map:
        for j in map[i]:
            if map[i][j] <= distance:
                reduced_map.append((i,j))

    return reduced_map


if __name__ == "__main__":
    if len(sys.argv) == 2:
        points = load_points(sys.argv[1])
        print(len(reduce_map(distance_map(points),10000)))
    else:
        print("Usage:  " + sys.argv[0] + " <data-file>")
