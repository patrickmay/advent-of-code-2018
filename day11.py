#!/usr/bin/env python3

import sys

# Solution to the day 11 puzzle from Advent of Code 2018.
# https://adventofcode.com/2018/day/11

def power_level(x,y,serial_number):
    """ Calculate the power level for the specified cell. """
    rack_id = x + 10
    power = rack_id * y
    power += serial_number
    power *= rack_id
    if power < 100:
        power = 0
    else:
        power = int((power - (int(power / 1000) * 1000)) / 100)
    power -= 5

    return power


def fuel_cells(serial_number):
    """ Return a 300x300 array of fuel cell power levels. """
    cells = [[0 for x in range(300)] for y in range(300)]
    for x in range(300):
        for y in range(300):
            cells[x][y] = power_level(x + 1,y + 1,serial_number)

    return cells


def highest_power(cells):
    """
    Return the coordinates of the top left corner of the 3x3 array of
    cells with the highest total power.
    """
    max_power = 0
    coords = (-1,-1)
    for x in range(300 - 2):
        for y in range(300 - 2):
            power = 0
            for i in range(x,x + 3):
                for j in range(y,y + 3):
                    power += cells[i][j]
            if power > max_power:
                coords = (x + 1,y + 1)
                max_power = power

    return [coords, max_power]


if __name__ == "__main__":
    if len(sys.argv) == 2:
        serial_number = int(sys.argv[1])
        cells = fuel_cells(serial_number)
        print(highest_power(cells))
    else:
        print("Usage:  " + sys.argv[0] + " <grid-serial-number>")
