#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from collections import defaultdict, namedtuple, Counter

def read_input(filename):
    field = defaultdict(lambda: '.')
    elves = set()
    for y, line in enumerate(open(filename)):
        for x, c in enumerate(line.strip()):
            field[x + y * 1j] = c
            if c == '#':
                elves.add(x + y * 1j)
    return field, elves 

nbs = [x + y for x in [-1, 0, 1] for y in [-1j, 0, 1j] if x + y != 0]

N = -1j
S = -N
E =  1
W = -E

NW = N + W
NE = N + E
SW = S + W
SE = S + E

Direction = namedtuple('Direction', ['move', 'nb1', 'nb2'])
directions = [
    Direction(N, NW, NE),
    Direction(S, SE, SW),
    Direction(W, NW, SW),
    Direction(E, NE, SE),
]

def get_bounds(field):
    min_x, max_x = 100_000, 0
    min_y, max_y = 100_000, 0

    for coord in field:
        if field[coord] == '#':
            min_x = min(coord.real, min_x)
            max_x = max(coord.real, max_x)
            min_y = min(coord.imag, min_y)
            max_y = max(coord.imag, max_y)
    return int(min_x), int(max_x), int(min_y), int(max_y)

def print_field(field):
    min_x, max_x, min_y, max_y = get_bounds(field)
    for y in range(min_y, max_y + 1):
        print(''.join(field[x + y * 1j] for x in range(min_x, max_x + 1)))
    print()

def count_empty(field):
    min_x, max_x, min_y, max_y = get_bounds(field)
    return sum(1 for y in range(min_y, max_y + 1) for x in range(min_x, max_x + 1) if field[x + y * 1j] == '.')

def part12(field, elves, directions, max_rounds):
    stable = False
    rounds = 0
    while not stable and rounds < max_rounds:
        stable = True
        proposed = {}
        for elf_c in elves:
            if all(field[elf_c + nb] == '.' for nb in nbs):
                continue
            for d in directions:
                if all(field[elf_c + o] == '.' for o in d):
                    proposed[elf_c] = elf_c + d.move
                    break

        counted = Counter(proposed.values())
        for old, new in proposed.items():
            if counted[new] == 1:
                stable = False
                field[old], field[new] = field[new], field[old]

                elves.remove(old)
                elves.add(new)
        directions = directions[1:] + directions[:1]
        rounds += 1
    return count_empty(field), rounds

                    
def main(filename):
    field, elves = read_input(filename)
    print(part12(field, elves, directions[:], max_rounds=10)[0])
    field, elves = read_input(filename)
    print(part12(field, elves, directions[:], max_rounds=1_000_000)[1])

if __name__ == '__main__':
    main('input' if len(sys.argv) == 1 else sys.argv[1])
