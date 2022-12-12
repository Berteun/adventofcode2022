#!/usr/bin/env python
# -*- coding: utf-8 -*-
import heapq

def read_input(filename):
    return [list(s.strip()) for s in open(filename)]

def neighbours(map, node):
    (x, y) = node
    neighbours = []
    if y > 0:
        neighbours.append((x, y - 1))
    if x > 0:
        neighbours.append((x - 1, y))
    if y < len(map) - 1:
        neighbours.append((x, y + 1))
    if x < len(map[0]) - 1:
        neighbours.append((x + 1, y))
    return [(nx, ny) for (nx, ny) in neighbours if ord(map[y][x]) + 1 >= ord(map[ny][nx])]

def neighbours2(map, node):
    (x, y) = node
    neighbours = []
    if y > 0:
        neighbours.append((x, y - 1))
    if x > 0:
        neighbours.append((x - 1, y))
    if y < len(map) - 1:
        neighbours.append((x, y + 1))
    if x < len(map[0]) - 1:
        neighbours.append((x + 1, y))
    return [(nx, ny) for (nx, ny) in neighbours if ord(map[y][x]) - 1 <= ord(map[ny][nx])]


def get_start(map):
    for y, row in enumerate(map):
        for x, n in enumerate(row):
            if n == 'S':
                map[y][x] = 'a'
                return (x, y)

def get_end(map):
    for y, row in enumerate(map):
        for x, n in enumerate(row):
            if n == 'E':
                map[y][x] = 'z'
                return (x, y)

def part1(map):
    start = get_start(map)
    end = get_end(map)
   
    dist = { start: 0 }
    prev = {}
    Q = [ (0, start) ]
    while Q:
        (d, node) = heapq.heappop(Q)
        if node in dist and d > dist[node]:
            continue

        for nb in neighbours(map, node):
            alt = dist[node] + 1
            if nb == end:
                return alt
            if nb not in dist or alt < dist[nb]:
                dist[nb] = alt
                prev[nb] = node
                heapq.heappush(Q, (alt, nb))
    return dist, prev

def part2(map):
    # Only to turn S into a
    _ = get_start(map)
    end = get_end(map)
   
    dist = { end: 0 }
    prev = {}
    Q = [ (0, end) ]
    while Q:
        (d, node) = heapq.heappop(Q)
        if node in dist and d > dist[node]:
            continue

        for nb in neighbours2(map, node):
            alt = dist[node] + 1
            if nb not in dist or alt < dist[nb]:
                dist[nb] = alt
                prev[nb] = node
                heapq.heappush(Q, (alt, nb))

    candidates = []
    for y, row in enumerate(map):
        for x, n in enumerate(row):
            if n == 'a' and (x, y) in dist:
                candidates.append(dist[(x,y)]) 
    return min(candidates)

def main(filename):
    map = read_input(filename)
    print(part1(map))

    map = read_input(filename)
    print(part2(map))

if __name__ == '__main__':
    import sys
    main('input' if len(sys.argv) == 1 else sys.argv[1])
