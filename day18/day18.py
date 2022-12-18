#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

def read_input(filename):
    return set(tuple(int(c) for c in line.strip().split(',')) for line in open(filename))

def neighbours(x, y, z):
    yield from ((x+1, y, z), (x, y+1, z), (x, y, z+1))
    yield from ((x-1, y, z), (x, y-1, z), (x, y, z-1))

def exposed_sides(coordinates, c):
    return sum(1 for nb in neighbours(*c) if nb not in coordinates)

def part1(coordinates):
    return sum(exposed_sides(coordinates, c) for c in coordinates) 

def get_outside_coordinates(coordinates):
    mins, maxs = tuple(min(x)-1 for x in zip(*coordinates)), tuple(max(x)+1 for x in zip(*coordinates))

    queue = {mins}
    outside = set()

    while queue:
        c = queue.pop()
        outside.add(c)
        for nb in neighbours(*c):
            if nb in coordinates or nb in outside:
                continue
            if any(c < mins[i] or c > maxs[i] for i, c in enumerate(nb)):
                continue

            queue.add(nb)

    return outside 

def really_exposed_sides(outside, c):
    return sum(1 for nb in neighbours(*c) if nb in outside)

def part2(coordinates):
    outside = get_outside_coordinates(coordinates)
    return sum(really_exposed_sides(outside, c) for c in coordinates)

def main(filename):
    coordinates = read_input(filename)
    print(part1(coordinates))
    print(part2(coordinates))

if __name__ == '__main__':
    main('input' if len(sys.argv) == 1 else sys.argv[1])
