#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import namedtuple

Move = namedtuple('Move', ['dir', 'n'])

directions = { 'L': (-1 + 0j), 'U': ( 0 + 1j), 'R': ( 1 + 0j), 'D': ( 0 - 1j), }

def read_input(filename):
    return [Move(d, int(n)) for d, n in (l.strip().split(' ') for l in open(filename))]

def touching(head, tail):
    return abs(head - tail) < 1.42

def sign(n):
    return (n > 0) - (n < 0)

def adjust_tail(head, tail):
    return (tail.real + sign(head.real - tail.real)) + 1j * (tail.imag + sign(head.imag - tail.imag))

def part12(moves, n_knots):
    knots = [(0 + 0j) for _ in range(n_knots)]
    locations = set([knots[-1]])
    for move in moves:
        for n in range(move.n):
            knots[0] += directions[move.dir]
            for n in range(1, n_knots):
                if not touching(knots[n - 1], knots[n]):
                    knots[n] = adjust_tail(knots[n - 1], knots[n])
            locations.add(knots[-1])
    return len(locations)

def main(filename):
    moves = read_input(filename)
    print(part12(moves, 2))
    print(part12(moves, 10))

if __name__ == '__main__':
    import sys
    main('input' if len(sys.argv) == 1 else sys.argv[1])
