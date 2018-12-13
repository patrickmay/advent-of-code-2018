#!/usr/bin/env python3

import sys
from collections import defaultdict

# Solution to the day 13 puzzle from Advent of Code 2018.
# https://adventofcode.com/2018/day/13

def parse_data(filename):
    """ Load the data from FILENAME. """
    carts = list()
    track = defaultdict(lambda: defaultdict())
    current_line = 0
    cart_id = 0
    with open(filename) as f:
        for line in f:
            for i in range(len(line)):
                segment = line[i]
                if segment in ['^','>','v','<']:
                    carts.append([(i,current_line),segment,'left',cart_id])
                    cart_id += 1
                    if segment == '^' or segment == 'v':
                        segment = '|'
                    elif segment == '>' or segment == '<':
                        segment = '-'
                track[i][current_line] = segment
            current_line += 1
            
    return [track, carts]


def overlapping_carts(carts):
    """ Return True if any of the CARTS occupy the same location. """
    locations = [cart[0] for cart in carts]
    
    return (len(set(locations)) < len(locations))


# Transition results when moving one tick.
TRANSITIONS = {('-','^'): None,
               ('-','>'): (1,0,'>'),
               ('-','v'): None,
               ('-','<'): (-1,0,'<'),
               ('|','^'): (0,-1,'^'),
               ('|','>'): None,
               ('|','v'): (0,1,'v'),
               ('|','<'): None,
               ('/','^'): (1,0,'>'),
               ('/','>'): (0,-1,'^'),
               ('/','v'): (-1,0,'<'),
               ('/','<'): (0,1,'v'),
               ('\\','^'): (-1,0,'<'),
               ('\\','>'): (0,1,'v'),
               ('\\','v'): (1,0,'>'),
               ('\\','<'): (0,-1,'^')}

# Turn results when moving one tick.
TURNS = {('left','^'): (-1,0,'straight','<'),
         ('left','>'): (0,-1,'straight','^'),
         ('left','v'): (1,0,'straight','>'),
         ('left','<'): (0,1,'straight','v'),
         ('straight','^'): (0,-1,'right','^'),
         ('straight','>'): (1,0,'right','>'),
         ('straight','v'): (0,1,'right','v'),
         ('straight','<'): (-1,0,'right','<'),
         ('right','^'): (1,0,'left','>'),
         ('right','>'): (0,1,'left','v'),
         ('right','v'): (-1,0,'left','<'),
         ('right','<'): (0,-1,'left','^')}

def one_tick(track,carts):
    """
    Move all the CARTS one segment along the TRACK.  Update each cart's
    position and return a list of the carts that crashed.  Carts must
    move in the order of their current location.
    """
    crashed_carts = list()
    ordered_carts = sorted(carts,key= lambda cart: cart[0])
    for cart in ordered_carts:
        if cart[3] not in crashed_carts:
            x = cart[0][0]
            y = cart[0][1]
            if (track[x][y],cart[1]) in TRANSITIONS:
                transition = TRANSITIONS[(track[x][y],cart[1])]
                cart[0] = (cart[0][0] + transition[0],
                           cart[0][1] + transition[1])
                cart[1] = transition[2]
            elif track[x][y] == '+':
                turn = TURNS[(cart[2],cart[1])]
                cart[0] = (cart[0][0] + turn[0],cart[0][1] + turn[1])
                cart[1] = turn[3]
                cart[2] = turn[2]
            else:
                print("Shouldn't see this.")

            for other_cart in carts:
                if (other_cart[3] != cart[3]
                    and other_cart[0] == cart[0]):
                    crashed_carts.append(other_cart[3])
                    crashed_carts.append(cart[3])
            
    return crashed_carts


if __name__ == "__main__":
    if len(sys.argv) == 2:
        track, carts = parse_data(sys.argv[1])
        i = 0
        while len(carts) > 1:
            crashed_carts = one_tick(track,carts)
            carts = [cart for cart in carts if cart[3] not in crashed_carts]
            i += 1

        print(i + 1)
        print(carts)
    else:
        print("Usage:  " + sys.argv[0] + " <data-file>")
