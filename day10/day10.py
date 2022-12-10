#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Tuple
from dataclasses import dataclass

instr_cycles = { 'addx': 2, 'noop': 1}
@dataclass(frozen=True)
class Instruction:
    code: str
    args: Tuple
    cycles: int


def parse_instr(l):
    code, *args = l.strip().split(' ')
    if code in ['addx']:
        args = [int(a) for a in args]

    return Instruction(code=code, args=args, cycles=instr_cycles[code])

def read_input(filename):
    return [parse_instr(l) for l in open(filename)]

def part1(instructions):
    cur = instructions[0]
    next_instr = 1
    remaining_cycles = cur.cycles
    regX = 1
    cycle_count = 1
    solution = 0
    crt_x_pos, crt_y_pos = 0, 0
    output = [[' ' for x in range(40)] for y in range(6)]

    while next_instr <= len(instructions):
        # During instruction
        if (cycle_count - 20) % 40 == 0:
            solution += cycle_count * regX 
        # Here CRT Draws
        if abs(crt_x_pos -regX) <= 1:
            output[crt_y_pos][crt_x_pos] = u'█'
        crt_x_pos, crt_y_pos = (crt_x_pos + 1) % 40, crt_y_pos + (crt_x_pos == 39)

        # Next cycle
        cycle_count += 1
        remaining_cycles -= 1 
        if remaining_cycles == 0:
            if cur.code == 'addx':
                regX += cur.args[0]
            if next_instr < len(instructions):
                cur = instructions[next_instr]
                remaining_cycles = cur.cycles
            next_instr += 1
    return solution, output


def main(filename):
    instructions = read_input(filename)
    sol1, sol2 = part1(instructions)
    print(sol1)
    print('\n'.join(''.join(line) for line in sol2))

if __name__ == '__main__':
    import sys
    main('input' if len(sys.argv) == 1 else sys.argv[1])
