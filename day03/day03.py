#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import namedtuple
Rucksack = namedtuple('Rucksack', ['compartment1', 'compartment2'])

def prio(common_item):
    assert len(common_item) == 1, f"{len(common_item)} should be 1"
    item = common_item.pop()
    if 'a' <= item <= 'z':
        return 1 + ord(item) - ord('a')
    if 'A' <= item <= 'Z':
        return 27 + ord(item) - ord('A')
    assert False

def read_input_1():
    rucksacks = []
    for l in open('input'):
        line = l.strip()
        c1, c2 = line[:len(line) // 2], line[len(line) // 2:]
        rucksacks.append(Rucksack(set(c1), set(c2)))
    return rucksacks

def part1(rucksacks):
    return sum(prio(r.compartment1 & r.compartment2) for r in rucksacks)

def read_input_2():
    groups = []
    for i, line in enumerate(open('input')):
        if i % 3 == 0:
            groups.append([])
        groups[-1].append(line.strip())
    return groups

def part2(groups):
    return sum(prio(set(g[0]) & set(g[1]) & set(g[2])) for g in groups)

def main():
    inp1 = read_input_1()
    print(part1(inp1))

    inp2 = read_input_2()
    print(part2(inp2))


if __name__ == '__main__':
    main()
