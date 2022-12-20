#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

def read_input(filename):
    return [int(l.strip()) for l in open(filename)]

def part12(numbers, key, iterations):
    inumbers = [(n * key, i) for (i,n) in enumerate(numbers)]
    numbers_copy = inumbers[:]
    for _ in range(iterations):
        for (n, i) in numbers_copy:
            idx = inumbers.index((n, i))
            p = inumbers.pop(idx)
            new_idx = (idx + n) % len(inumbers)
            inumbers.insert(new_idx, p)
    zero_idx = [i for (i, (n,_)) in enumerate(inumbers) if n == 0][0]
    return sum(inumbers[zero_idx + o % len(inumbers)][0] for o in (1000, 2000, 3000)) 

def main(filename):
    numbers = read_input(filename)
    print(part12(numbers, 1, 1))
    print(part12(numbers, 811589153, 10))

if __name__ == '__main__':
    main('input' if len(sys.argv) == 1 else sys.argv[1])
