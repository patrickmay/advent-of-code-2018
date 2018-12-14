#!/usr/bin/env python3

import sys

# Solution to the day 14 puzzle from Advent of Code 2018.
# https://adventofcode.com/2018/day/14

if __name__ == "__main__":
    if len(sys.argv) == 2:
        recipe_count = int(sys.argv[1])
        recipes = [3,7]
        elf_indices = [0,1]
        for i in range(recipe_count + 10):
            new_recipe = 0
            for j in range(len(elf_indices)):
                new_recipe += recipes[elf_indices[j]]
            for digit in str(new_recipe):
                recipes.append(int(digit))
            for k in range(len(elf_indices)):
                elf_indices[k] = ((elf_indices[k] + 1 + recipes[elf_indices[k]])
                                  % len(recipes))
        print(recipes[recipe_count:recipe_count + 10])
    else:
        print("Usage:  " + sys.argv[0] + " <recipe-count>")
