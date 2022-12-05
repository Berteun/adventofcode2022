#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import namedtuple

Instruction = namedtuple('Instruction', ['amount', 'fr', 'to'])

def read_input():
    instructions, stacks = [], [[] for _ in range(9)], 
    raw_stacks, raw_instructions = open('input').read().split("\n\n")
    for line in raw_stacks.split("\n")[:-1]:
        for i in range(9):
            index = 1 + i * 4
            if line[index] != ' ':
                stacks[i].append(line[index])
    for stack in stacks:
        stack.reverse()

    for raw_instr in raw_instructions.strip().split("\n"):
        _, amount_str, _, from_str, _, to_str = raw_instr.split(" ")
        instructions.append(Instruction(int(amount_str), int(from_str) - 1, int(to_str) - 1))
    return stacks, instructions

def part12(stacks, instructions, transform):
    for instruction in instructions:
        stacks[instruction.to] += transform(stacks[instruction.fr][-instruction.amount:])
        stacks[instruction.fr][-instruction.amount:] = []
    return stacks

def top_of_stacks(stacks):
    return ''.join(str(stack[-1]) for stack in stacks)

def main():
    stacks, instructions = read_input()
    print(top_of_stacks(part12([s[:] for s in stacks], instructions, reversed)))
    print(top_of_stacks(part12(stacks, instructions, lambda l: l)))

if __name__ == '__main__':
    main()
