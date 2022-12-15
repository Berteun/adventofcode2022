#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from dataclasses import dataclass

class Interval:
    def __init__(self, start, end):
        assert start <= end, "start cannot be past end"
        self.start = start
        self.end = end

    def contains(self, other):
        return self.start <= other.start and self.end >= other.end

    def overlaps(self, other):
        return self.start <= other.end and self.end >= other.start

    def merge_with(self, other):
        self.start = min(self.start, other.start)
        self.end = max(self.end, other.end)

    def size(self):
        return 1 + self.end - self.start

    def __repr__(self):
        return f'[{self.start}, {self.end}]'

class Intervals:
    def __init__(self):
        self.interval_list = []

    def add(self, interval):
        stable = False
        while not stable:
            for i in range(len(self.interval_list)):
                if self.interval_list[i].overlaps(interval):
                    self.interval_list[i].merge_with(interval)
                    interval = self.interval_list.pop(i)
                    break
            else:
                stable = True
        self.interval_list.append(interval)

    def size(self):
        return sum(i.size() for i in self.interval_list)

@dataclass
class Sensor:
    x: int
    y: int
    b_x: int
    b_y: int

    def radius(self):
        return self.dist(self.b_x, self.b_y)

    def dist(self, x, y):
        return abs(self.x - x) + abs(self.y - y)

    def get_y_range(self, y):
        if self.dist(self.x, y) > self.radius():
            return None
        else:
            steps = self.radius() - self.dist(self.x, y)
            return Interval(self.x - steps, self.x + steps)

def read_input(filename):
    sensors = []
    for line in open(filename):
        sensor_str, beacon_str = line.strip().split(": ")
        str_x, str_y = sensor_str.split(", ")
        str_bx, str_by = beacon_str.split(", ")
        sensors.append(Sensor(int(str_x.split('=')[1]), int(str_y.split('=')[1]), int(str_bx.split('=')[1]), int(str_by.split('=')[1])))
    return sensors

def part1(sensors, y=2_000_000):
    intervals = Intervals()

    for sensor in sensors:
        if (interval := sensor.get_y_range(y)) is not None:
            intervals.add(interval)

    beacons = set((s.b_x, s.b_y) for s in sensors if s.b_y == y)
    return intervals.size() - len(beacons)

def part2(sensors, max_xy=4000000):
    for y in range(max_xy + 1):
        intervals = Intervals()

        for sensor in sensors:
            if (interval := sensor.get_y_range(y)) is not None:
                intervals.add(interval)

        for interval in intervals.interval_list:
            if interval.start > 0: 
                beacon_x = interval.start - 1
                return beacon_x * 4000000 + y
                
            if interval.end < max_xy:
                beacon_x = interval.end + 1
                return beacon_x * 4000000 + y

    return 'ERROR'


def main(filename):
    sensors = read_input(filename)
    print(part1(sensors))
    print(part2(sensors))

if __name__ == '__main__':
    main('input' if len(sys.argv) == 1 else sys.argv[1])
