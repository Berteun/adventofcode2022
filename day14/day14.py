#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from collections import defaultdict

def read_input(filename):
    fragments = []
    for line in open(filename):
        segment = []
        for line_part in line.strip().split(' -> '):
            x,y = (int(n) for n in line_part.split(','))
            segment.append((x,y))
        fragments.append(segment)
    return fragments

def make_map(fragments):
    map = defaultdict(lambda: '.')
    min_x, max_x = 10_000, 0
    min_y, max_y = 0, 0

    for fragment in fragments: 
        s_x, s_y = fragment[0]

        for e_x, e_y in fragment[1:]:
            min_x, max_x = min(min_x, e_x, s_x), max(max_x, e_x, s_x)
            min_y, max_y = min(min_y, e_y, s_y), max(max_y, e_y, s_y)

            if s_x == e_x:
                for y in range(min(s_y, e_y), max(s_y, e_y) + 1):
                    map[(s_x, y)] = '#'
            elif s_y == e_y:
                for x in range(min(s_x, e_x), max(s_x, e_x) + 1):
                    map[(x, s_y)] = '#'
            s_x, s_y = e_x, e_y
    return map, (min_x, max_x, min_y, max_y)

def print_map(map, bounds):
    (min_x, max_x, min_y, max_y) = bounds
    print('\n'.join(''.join(map[(x,y)] for x in range(min_x, max_x + 1)) for y in range(min_y, max_y + 1)),'\n')

def part1(fragments):
    map, bounds = make_map(fragments)
    #print_map(map, bounds)
    total_resting = 0
    while True:
        sand_x, sand_y = 500, 0
        while True:
            if map[(sand_x, sand_y + 1)] == '.':
                sand_x, sand_y = sand_x, sand_y + 1
                if sand_y > bounds[3]:
                    return total_resting
            elif map[(sand_x - 1, sand_y + 1)] == '.':
                sand_x, sand_y = sand_x - 1, sand_y + 1
            elif map[(sand_x + 1, sand_y + 1)] == '.':
                sand_x, sand_y = sand_x + 1, sand_y + 1
            else:
                break
        total_resting += 1
        map[(sand_x, sand_y)] = 'o'
        #print_map(map, bounds)

def part2(fragments):
    map, bounds = make_map(fragments)
    total_resting = 0
    while True:
        sand_x, sand_y = 500, 0
        while sand_y < bounds[3] + 1:
            if map[(sand_x, sand_y + 1)] == '.':
                sand_x, sand_y = sand_x, sand_y + 1
            elif map[(sand_x - 1, sand_y + 1)] == '.':
                sand_x, sand_y = sand_x - 1, sand_y + 1
            elif map[(sand_x + 1, sand_y + 1)] == '.':
                sand_x, sand_y = sand_x + 1, sand_y + 1
            else:
                break
        total_resting += 1
        map[(sand_x, sand_y)] = 'o'
        if sand_x == 500 and sand_y == 0:
            return total_resting

def main(filename):
    fragments = read_input(filename)
    print(part1(fragments))
    print(part2(fragments))

if __name__ == '__main__':
    main('input' if len(sys.argv) == 1 else sys.argv[1])
