#!/usr/bin/env python
# -*- coding: utf-8 -*-
import heapq
import math
import sys

from collections import defaultdict
from enum import IntFlag

class Blizzard(IntFlag):
    U = 1
    D = 2
    L = 4
    R = 8

    def __str__(self):
        cnt = bin(self).count("1")
        if cnt == 0:
            return "."
        if cnt > 1:
            return str(cnt)
        return {
            Blizzard.U: '^',
            Blizzard.D: 'v',
            Blizzard.L: '<',
            Blizzard.R: '>',
        }[self]

enum_map = {
    '^': Blizzard.U,
    'v': Blizzard.D,
    '<': Blizzard.L,
    '>': Blizzard.R,
}

movement = {
    Blizzard.U: -1j,
    Blizzard.D:  1j,
    Blizzard.L: -1,
    Blizzard.R:  1,
}

def read_input(filename):
    blizzards = defaultdict(lambda: Blizzard(0))
    for y, line in enumerate(open(filename)):
        for x, c in enumerate(line.strip()):
            if c in enum_map:
                blizzards[x + y * 1j] |= enum_map[c]
    return blizzards, x, y

green = "\033[0;32m"
reset = "\033[0m"
bold = "\033[1m"

def print_basin(basin, max_x, max_y, coord=None):
    print('#.' + '#' * (max_x - 1))
    for y in range(1, max_y):
        print('#' + ''.join(str(basin[x + y * 1j]) if (x + y * 1j) != coord else f'{green}{bold}@{reset}' for x in range(1, max_x)) + '#')
    print('#' * (max_x - 1) + '.#')

def generate_basins(basin, max_x, max_y):
    def wrap(c):
        if c.real == max_x:
            c = 1 + c.imag * 1j
        if c.real == 0:
            c = max_x - 1 + c.imag * 1j
        if c.imag == max_y:
            c = c.real + 1j
        if c.imag == 0:
            c = c.real + (max_y - 1) * 1j
        return c

    w = max_x - 1
    h = max_y - 1
    gcm = (w * h) // math.gcd(w, h)
    basins = [basin]
    for _ in range(gcm - 1):
        new_basin = defaultdict(lambda: Blizzard(0))
        for y in range(1, max_y):
            for x in range(1, max_x):
                c = x + y * 1j
                for bz in Blizzard:
                    if basins[-1][c] & bz:
                        new_c = wrap(c + movement[bz])
                        new_basin[new_c] |= bz
        basins.append(new_basin)
    return basins

def solve(basins, start, end, max_x, max_y, start_time):
    def h(c,t):
        return t + abs(end.real - c.real) + abs(end.imag - c.imag)

    def neighbours(coord, time):
        nbs = []
        for move in [0] + list(movement.values()):
            new_coord = coord + move
            if new_coord != end and new_coord != start:
                if new_coord.real == 0 or new_coord.real == max_x:
                    continue
                if new_coord.imag <= 0 or new_coord.imag == max_y:
                    continue
            if basins[(time + 1) % len(basins)][new_coord] == Blizzard(0):
                nbs.append(new_coord)
        return nbs


    dist = { (start, start_time): 0 }
    prev = {}

    # Heurstic score, dist, time, coord
    Q = [ (h(start, start_time), 0, start_time, hash(start), start) ]
    while Q:
        (score, d, time, _, coord) = heapq.heappop(Q)
        key = (coord, time)
        if key in dist and d > dist[key]:
            continue

        for nb in neighbours(coord, time):
            new_dist = dist[key] + 1
            if nb == end:
                return new_dist
            if (nb, time + 1) not in dist or new_dist < dist[(nb, time + 1)]:
                dist[(nb, time + 1)] = new_dist
                prev[(nb, time)] = (coord, time)
                new_loc = (h(nb, time + 1), new_dist, time + 1, hash(nb), nb)
                heapq.heappush(Q, new_loc)
    assert False

    
def part1(basins, max_x, max_y):
    start, end = 1, max_x - 1 + max_y * 1j  
    return solve(basins, start, end, max_x, max_y, 0)


def part2(basins, max_x, max_y):
    start, end = 1, max_x - 1 + max_y * 1j  
    j1 = solve(basins, start, end, max_x, max_y, 0)
    j2 = solve(basins, end, start, max_x, max_y, j1)
    j3 = solve(basins, start, end, max_x, max_y, j1 + j2)
    return(j1 + j2 + j3)

def main(filename):
    basin, max_x, max_y = read_input(filename)
    basins = generate_basins(basin, max_x, max_y)
    print(part1(basins, max_x, max_y))
    print(part2(basins, max_x, max_y))

if __name__ == '__main__':
    main('input' if len(sys.argv) == 1 else sys.argv[1])
