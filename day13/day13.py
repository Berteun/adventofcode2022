#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from functools import cmp_to_key

def read_input(filename):
    pairs = []
    for block in open(filename).read().split("\n\n"):
        l1, l2 = block.strip().split("\n")
        pairs.append((json.loads(l1), json.loads(l2)))
    return pairs

def right_order(p1, p2):
    if type(p1) == int and type(p2) == int:
        return p1 < p2
    if type(p1) == int and type(p2) == list:
        return right_order([p1], p2)
    if type(p1) == list and type(p2) == int:
        return right_order(p1, [p2])
    i = 0
    while i < len(p1) and i < len(p2):
        if right_order(p1[i], p2[i]):
            return True
        if right_order(p2[i], p1[i]):
            return False
        i += 1
    return len(p1) < len(p2)

def part1(pairs):
    return sum(i + 1 for i, (p1, p2) in enumerate(pairs) if right_order(p1, p2))

def part2(pairs):
    key = cmp_to_key(lambda p1, p2 :  right_order(p2, p1) - right_order(p1, p2))
    divider_packets = [ [[2]], [[6]] ]
    all_packets = sorted(divider_packets + [p1 for (p1, _) in pairs] + [p2 for (_, p2) in pairs], key=key)
    return (1 + all_packets.index(divider_packets[0])) * (1 + all_packets.index(divider_packets[1]))

def main(filename):
    pairs = read_input(filename)
    print(part1(pairs))
    print(part2(pairs))

if __name__ == '__main__':
    import sys
    main('input' if len(sys.argv) == 1 else sys.argv[1])
