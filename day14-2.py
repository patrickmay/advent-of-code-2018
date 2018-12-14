#!/usr/bin/env python3

import sys

# Solution to part 2 of the day 14 puzzle from Advent of Code 2018.
# https://adventofcode.com/2018/day/14

if __name__ == "__main__":
    if len(sys.argv) == 2:
        recipe_scores = sys.argv[1]
        recipes = [3,7]
        recipes_string = '37'
        elf_indices = [0,1]
        i = 0
        index = -1
        while True:
            new_recipe = 0
            for j in range(len(elf_indices)):
                new_recipe += recipes[elf_indices[j]]
            for digit in str(new_recipe):
                recipes.append(int(digit))
                recipes_string += digit
            for k in range(len(elf_indices)):
                elf_indices[k] = ((elf_indices[k] + 1 + recipes[elf_indices[k]])
                                  % len(recipes))
            index = recipes_string.find(recipe_scores)
            if index != -1:
                break
        print(index)
    else:
        print("Usage:  " + sys.argv[0] + " <recipe-count>")
