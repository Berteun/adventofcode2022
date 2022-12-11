#!/usr/bin/env python
# -*- coding: utf-8 -*-
import operator
import logging
from typing import Callable, Dict, List, Tuple
from dataclasses import dataclass

log = logging.getLogger("MONKEYS")
logging.basicConfig(format='%(message)s', level=logging.INFO)


@dataclass
class Monkey:
    number: int
    items: List[int]
    operation: Callable[[int], int]
    operation_desc: str
    test: Callable[[int], bool]
    test_number: int
    throws_to: Dict[bool, int]

def parse_monkey(b):
    operations = {
        '*': operator.mul,
        '+': operator.add,
    }
    operation_strs = {
        '*': "is multiplied by ",
        '+': "increases by ",
    }
    lines = b.strip().split('\n') 
    number = int(lines[0][-2])
    starting_items = [int(n.strip()) for n in lines[1].split(':')[1].split(', ')]
    rhs_operations = lines[2].split('=')[1].split(' ')
    if rhs_operations[3] == 'old':
        operation_str = operation_strs[rhs_operations[2]] + 'itself'
        operation = lambda old : operations[rhs_operations[2]](old, old)
    else:
        operation_str = operation_strs[rhs_operations[2]] + rhs_operations[3]
        operation = lambda old : operations[rhs_operations[2]](old, int(rhs_operations[3]))
    divisible_by = int(lines[3].split(' ')[-1])
    test = lambda n: n % divisible_by == 0
    throw_to = {
        True: int(lines[4].split(' ')[-1]),
        False: int(lines[5].split(' ')[-1]),
    }
    return Monkey(number, starting_items, operation, operation_str, test, divisible_by, throw_to)

def read_input(filename):
    return { m.number: m for m in (parse_monkey(b) for b in open(filename).read().split('\n\n'))}

def part12(monkeys, rounds, divisor):
    counts = { monkey : 0 for monkey in monkeys }
    gcm = 1
    for m in monkeys.values():
        gcm *= m.test_number
    for _rnd in range(rounds):
        log.debug(f"Round {_rnd + 1}")
        for m in range(len(monkeys)):
            monkey = monkeys[m]
            log.debug(f"  Monkey {monkey.number}:")
            while monkey.items:
                counts[monkey.number] += 1
                item = monkey.items.pop(0)
                log.debug(f"    Monkey inspects an item with a worry level of {item}")
                new = monkey.operation(item)
                log.debug(f"        Worry level {monkey.operation_desc} to {new}.")
                new_div = (new % gcm) // divisor
                log.debug(f"        Monkey gets bored with item. Worry level is divided by {divisor} to {new_div}.")
                outcome = monkey.test(new_div)
                log.debug(f"        Current worry level is {'not ' if not outcome else ''}divisible by {monkey.test_number}.")
                new_monkey = monkey.throws_to[outcome]
                log.debug(f"        Item with worry level {new_div} is thrown to monkey {new_monkey}.")
                monkeys[new_monkey].items.append(new_div)
        log.debug(f"End of round {_rnd + 1}")
        for m in range(len(monkeys)):
            monkey = monkeys[m]
            log.debug(f"  Monkey {monkey.number}: {', '.join(str(i) for i in monkey.items)}")
    sorted_counts = list(sorted(counts.values()))
    return sorted_counts[-1] * sorted_counts[-2]


def main(filename):
    monkeys = read_input(filename)
    print(part12(monkeys, 20, 3))
    monkeys = read_input(filename)
    print(part12(monkeys, 10_000, 1))

if __name__ == '__main__':
    import sys
    main('input' if len(sys.argv) == 1 else sys.argv[1])
