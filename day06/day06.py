#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import namedtuple


def read_input():
    return open('input').readline().strip()

def part12(buffer, distinct_chars):
    for n in range(len(buffer) - distinct_chars):
        s = set(buffer[n:n+distinct_chars])
        if len(s) == distinct_chars:
            return n + distinct_chars 

def main():
    buffer = read_input()
    print(part12(buffer, 4))
    print(part12(buffer, 14))

if __name__ == '__main__':
    main()
