#!/usr/bin/env python
# -*- coding: utf-8 -*-
from enum import Enum
from dataclasses import dataclass

class RPS(Enum):
    Rock = 1
    Paper = 2
    Scissors = 3

    
@dataclass(frozen=True)
class Move:
    me: RPS
    opp: RPS

    def me_won(self):
        return (
            (self.me == RPS.Rock and self.opp == RPS.Scissors)
            or (self.me == RPS.Scissors and self.opp == RPS.Paper)
            or (self.me == RPS.Paper and self.opp == RPS.Rock))

    def me_lost(self):
        return Move(me=self.opp, opp=self.me).me_won()

    def me_draw(self):
        return not self.me_won() and not self.me_lost()


    def score(self):
        score = 0
        if self.me_draw():
            score += 3
        if self.me_won():
            score += 6
        if self.me == RPS.Rock:
            score += 1
        if self.me == RPS.Paper:
            score += 2
        if self.me == RPS.Scissors:
            score += 3
        return score


opp_map = {
    'A': RPS.Rock,
    'B': RPS.Paper,
    'C': RPS.Scissors,
}

me_map = {
    'X': RPS.Rock,
    'Y': RPS.Paper,
    'Z': RPS.Scissors,
}

def parse_line_1(l):
    opp, me = l.split(' ')
    return Move(me=me_map[me], opp=opp_map[opp])

def get_move(opp_raw, move):
    opp = opp_map[opp_raw]
    if move == 'Y':
        return opp
    if move == 'X':
        if opp == RPS.Rock: return RPS.Scissors
        if opp == RPS.Paper: return RPS.Rock
        if opp == RPS.Scissors: return RPS.Paper
    if move == 'Z':
        if opp == RPS.Rock: return RPS.Paper
        if opp == RPS.Paper: return RPS.Scissors
        if opp == RPS.Scissors: return RPS.Rock

def parse_line_2(l):
    opp_raw, move = l.split(' ')
    me = get_move(opp_raw, move)
    return Move(me, opp=opp_map[opp_raw])

def read_input_1():
    return [parse_line_1(l.strip()) for l in open('input')]

def read_input_2():
    return [parse_line_2(l.strip()) for l in open('input')]


def part1(moves):
    return sum(m.score() for m in moves)

def part2(moves):
    return sum(m.score() for m in moves)

def main():
    inp1 = read_input_1()
    print(part1(inp1))

    inp2 = read_input_2()
    print(part2(inp2))


if __name__ == '__main__':
    main()
