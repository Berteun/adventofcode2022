#!/usr/bin/env python
# -*- coding: utf-8 -*-

def read_input():
    grid = []
    for line in open('input'):
        l = line.strip()
        if not l:
            continue
        grid.append([int(c) for c in l])
    return grid

def part1(grid):
    visible = [[False for _ in row] for row in grid]
    for y in range(len(grid)):
        height = -1
        for x in range(len(grid[y])):
            if grid[y][x] > height:
                visible[y][x] = True
                height = grid[y][x]
        height = -1
        for x in range(len(grid[y]) - 1, -1, -1):
            if grid[y][x] > height:
                visible[y][x] = True
                height = grid[y][x]

    for x in range(len(grid[0])):
        height = -1
        for y in range(len(grid)):
            if grid[y][x] > height:
                visible[y][x] = True
                height = grid[y][x]

        height = -1
        for y in range(len(grid) - 1, -1, -1):
            if grid[y][x] > height:
                visible[y][x] = True
                height = grid[y][x]
    return sum(sum(row) for row in visible)

def scenic_score(grid, x, y):
    minx, miny = 0, 0
    maxx, maxy = len(grid[0]) - 1, len(grid) - 1

    lx = x
    while lx - 1 >= minx:
        lx -= 1
        if grid[y][lx] >= grid[y][x]:
            break

    rx = x
    while rx + 1 <= maxx:
        rx += 1
        if grid[y][rx] >= grid[y][x]:
            break

    dy = y
    while dy - 1 >= miny:
        dy -= 1
        if grid[dy][x] >= grid[y][x]:
            break

    uy = y
    while uy + 1 <= maxy:
        uy += 1
        if grid[uy][x] >= grid[y][x]:
            break

    up = (uy - y)
    dn = (y - dy)
    lf = (x - lx)
    rt = (rx - x)
    score = up * rt * dn * lf
    #print("x", x, "y", y, "up", up, "rt", rt, "dn", dn, "lf", lf, score)
    return score

def part2(grid):
    scores = [[0 for _ in row] for row in grid]
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            score = scenic_score(grid, x, y)
            #print(score, x, y, end="; ")
            scores[y][x] = score
    return max(max(row) for row in scores)

def main():
    grid = read_input()
    print(part1(grid))
    print(part2(grid))


if __name__ == '__main__':
    main()
