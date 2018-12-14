#!/usr/bin/env python3

import sys

# Solution to part 2 of the day 14 puzzle from Advent of Code 2018.
# https://adventofcode.com/2018/day/14

if __name__ == "__main__":
    if len(sys.argv) == 2:
        recipe_scores = sys.argv[1]
        recipes = [3,7]
        elf_indices = [0,1]
        recipe_count = -1
        while 1:
            new_recipe = 0
            for j in range(len(elf_indices)):
                new_recipe += recipes[elf_indices[j]]
            for digit in str(new_recipe):
                recipes.append(int(digit))
                if len(recipes) >= len(recipe_scores):
                    recent_scores = ''.join([str(score)
                                             for score
                                             in recipes[-len(recipe_scores):]])
                    if recent_scores == recipe_scores:
                        recipe_count = len(recipes) - len(recipe_scores)
                        print(recipe_count)
                        sys.exit()
            for k in range(len(elf_indices)):
                elf_indices[k] = ((elf_indices[k] + 1 + recipes[elf_indices[k]])
                                  % len(recipes))
    else:
        print("Usage:  " + sys.argv[0] + " <recipe-count>")
