#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

snafu_dec_map = { '=': -2, '-': -1, '0':  0, '1':  1, '2':  2 }
dec_snafu_map = { v : k for k, v in snafu_dec_map.items() }

def snafu_to_dec(number):
    return sum(snafu_dec_map[c] * 5**p for (p,c) in enumerate(number[::-1]))

def dec_to_snafu(number):
    snafu = ''
    while number > 0:
        number, rem = divmod(number, 5)
        if rem <= 2:
            snafu += dec_snafu_map[rem]
        else:
            snafu += dec_snafu_map[rem - 5]
            number += 1
    return snafu[::-1] if snafu else '0'

def read_input(filename):
    return [l.strip() for l in open(filename)]

def part1(numbers):
    return dec_to_snafu(sum(snafu_to_dec(n) for n in numbers))

def main(filename):
    numbers = read_input(filename) 
    print(part1(numbers))

if __name__ == '__main__':
    main('input' if len(sys.argv) == 1 else sys.argv[1])
