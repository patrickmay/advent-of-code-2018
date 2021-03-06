#!/usr/bin/env python3

import sys
from collections import defaultdict

# Solution to part 2 of the day 8 puzzle from Advent of Code 2018.
# https://adventofcode.com/2018/day/8

class Node:
    def __init__(self):
        self.child_nodes = list()
        self.metadata = list()

    def load(self,node_data):
        """ Load this node and all subnodes from FILENAME. """
        consumed_elements = 2  # child count and metadata count
        
        for child_count in range(node_data[0]):
            child_node = Node()
            consumed_elements += child_node.load(node_data[consumed_elements:])
            self.child_nodes.append(child_node)

        for metadata_count in range(node_data[1]):
            self.metadata.append(node_data[consumed_elements + metadata_count])
        consumed_elements += node_data[1]

        return consumed_elements

    def sum_metadata(self):
        """ Traverse the tree and sum all metadata. """
        total = sum(self.metadata)
        for child in self.child_nodes:
            total += child.sum_metadata()

        return total

    def value(self):
        """ Calculate the value of this node using the puzzle rules. """
        total = 0

        if not self.child_nodes:
            total = sum(self.metadata)
        else:
            # We need all indexes in child_nodes that correspond to metadata.
            indices = [(i - 1) for i in self.metadata
                       if i > 0 and i <= len(self.child_nodes)]
            for index in indices:
                total += self.child_nodes[index].value()

        return total


def load_nodes(filename):
    """ Load the nodes from FILENAME. """
    root = Node()

    with open(filename) as f:
        data = [int(i) for i in f.readline().split(' ')]

    root.load(data)

    return root


if __name__ == "__main__":
    if len(sys.argv) == 2:
        root = load_nodes(sys.argv[1])
        print(root.value())
    else:
        print("Usage:  " + sys.argv[0] + " <data-file>")
