#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

shapes = [
    ["####"],
    [".#.",
     "###",
     ".#."],
    ["..#",
     "..#",
     "###"],
    ["#",
     "#",
     "#",
     "#"],
    ["##",
     "##"],
]

def read_input(filename):
    return open(filename).readline().strip()

def make_start_block(shape):
    return ['..' + l + '.' * (5 - len(l)) for l in shape]

EMPTY_LINE = '.......'
def ensure_empty_lines(field, n):
    top_line = len(field) - 1
    while field[top_line] == EMPTY_LINE:
        top_line -= 1
    empty_lines = len(field) -1 - top_line 
    for n in range(empty_lines, n):
        field.append(EMPTY_LINE)

def is_resting(field, block, dropped):
    block_top_y = len(field) + len(block) - dropped - 1
    for y in range(len(block)):
        if block_top_y - y >= len(field):
            continue
        for x in range(len(block[y])):
            if block[y][x] == '#' and field[block_top_y - y][x] == '#':
                return True
    return False

def apply_gust(gust, block, field, dropped):
    block_top_y = len(field) + len(block) - dropped - 1
    if gust == '<':
        # Hitting wall
        if any(l[0] == '#' for l in block):
            return block
        for y in range(len(block)):
            if block_top_y - y >= len(field):
                continue
            for x in range(len(block[y])):
                if block[y][x] == '#' and field[block_top_y - y][x - 1] == '#':
                    return block
        # No collission, move
        return [l[1:] + '.' for l in block]
    if gust == '>':
        # Hitting wall
        if any(l[-1] == '#' for l in block):
            return block
        for y in range(len(block)):
            if block_top_y - y >= len(field):
                continue
            for x in range(len(block[y])):
                if block[y][x] == '#' and field[block_top_y - y][x + 1] == '#':
                    return block
        # No collission, move
        return ['.' + l[:-1] for l in block]
    assert False

def settle_block(block, field, dropped):
    block_top_y = len(field) + len(block) - dropped
    if block_top_y == len(field):
        field.append(EMPTY_LINE)
    #print(len(field), len(block), dropped)
    for y in range(len(block)):
        field[block_top_y - y] = ''.join(['#' if field[block_top_y - y][x] == '#' or block[y][x] == '#' else '.' for x in range(len(block[y]))])

def solve(gusts):
    field = ['#######', EMPTY_LINE, EMPTY_LINE, EMPTY_LINE]
    shape_cnt, gust_cnt, cnt = 0, 0, 0

    previous_heights = {}
    part1, part2 = None, None
    while part1 is None or part2 is None:
        height = len(field) - 1
        while field[height] == EMPTY_LINE:
            height -= 1

        if cnt == 2022:
            part1 = height

        # Not sure why this exactly works, the top of the board
        # would have an influence as well, but I guess that is probably
        # the same; we just iterate until we are exactly an integer number of
        # cycles away from the end; only then can we predict the exact height
        if part2 is None and (shape_cnt, gust_cnt) in previous_heights:
            prev_height, prev_cnt = previous_heights[(shape_cnt, gust_cnt)]
            cycle_length = cnt - prev_cnt
            if (1_000_000_000_000 - cnt) % (cycle_length) == 0:
                cycles = (1_000_000_000_000 - cnt) // (cycle_length)
                part2 = height + (height - prev_height) * int(cycles)

        previous_heights[(shape_cnt, gust_cnt)] = (height, cnt)

        shape = shapes[shape_cnt]
        ensure_empty_lines(field, 3)
        block = make_start_block(shape)
        dropped = 0
        while not is_resting(field, block, dropped):
            block = apply_gust(gusts[gust_cnt], block, field, dropped)
            gust_cnt = (gust_cnt + 1) % len(gusts)
            dropped += 1
        settle_block(block, field, dropped)
        shape_cnt = (shape_cnt + 1) % len(shapes)
        cnt += 1
    return part1, part2

def main(filename):
    gusts = read_input(filename)
    part1, part2 = solve(gusts)
    print(part1)
    print(part2)

if __name__ == '__main__':
    main('input' if len(sys.argv) == 1 else sys.argv[1])
