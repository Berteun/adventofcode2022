#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Interval:
    def __init__(self, start, end):
        assert start <= end, "start cannot be past end"
        self.start = start
        self.end = end

    def contains(self, other):
        return self.start <= other.start and self.end >= other.end

    def overlaps(self, other):
        return self.start <= other.end and self.end >= other.start

def parse_interval(interval: str):
    start, end = interval.split('-')
    return Interval(int(start), int(end))

def read_input():
    intervals = []
    for line in open('input'):
        i_1, i_2 = line.split(",")
        intervals.append((parse_interval(i_1), parse_interval(i_2)))
    return intervals

def part1(intervals):
    return sum(i1.contains(i2) or i2.contains(i1) for (i1, i2) in intervals)

def part2(intervals):
    return sum(i1.overlaps(i2) for (i1, i2) in intervals)

def main():
    inp = read_input()
    print(part1(inp))
    print(part2(inp))

if __name__ == '__main__':
    main()
