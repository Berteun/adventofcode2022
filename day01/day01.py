#!/usr/bin/env python
# -*- coding: utf-8 -*-

def read_input():
    f = open('input').read()
    blocks = [[int(s) for s in block.split('\n') if s] for block in f.split('\n\n')]
    return blocks


def part1(blocks):
    return max(sum(b) for b in blocks)

def part2(blocks):
    return sum(list(sorted(sum(b) for b in blocks))[-3:])

def main():
    inp = read_input()

    print(part1(inp))
    print(part2(inp))


if __name__ == '__main__':
    main()
