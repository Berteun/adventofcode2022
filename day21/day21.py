#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

class LitNode:
    def __init__(self, value):
        self.value = value

    def eval(self, _nodes):
        return self.value

class ExprNode:
    def __init__(self, lhs, op, rhs):
        self.lhs = lhs
        self.rhs = rhs
        self.op = op
    
    def eval(self, nodes):
        lhs = nodes[self.lhs].eval(nodes)
        rhs = nodes[self.rhs].eval(nodes)
        if self.op == '+':
            return lhs + rhs
        if self.op == '*':
            return lhs * rhs
        if self.op == '/':
            return lhs / rhs
        if self.op == '-':
            return lhs - rhs

class HumnNode:
    def __init__(self):
        self.c = 0
        self.x = 1
    def __add__(self, other):
        self.c += other
        return self
    def __radd__(self, other):
        self.c += other
        return self
    def __sub__(self, other):
        self.c -= other
        return self
    def __rsub__(self, other):
        self.c = other - self.c
        return self
    def __mul__(self, other):
        self.c *= other
        self.x *= other
        return self
    def __rmul__(self, other):
        self.c *= other
        self.x *= other
        return self
    def __truediv__(self, other):
        self.c /= other
        self.x /= other
        return self

    def eval(self, nodes):
        return self

class RootNode:
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs
    
    def solve(self, nodes):
        lhs = nodes[self.lhs].eval(nodes)
        rhs = nodes[self.rhs].eval(nodes)
        if isinstance(lhs, HumnNode):
            return abs((rhs - lhs.c)/lhs.x)
        else:
            return abs((lhs - rhs.c)/rhs.x)


def read_input(filename):
    nodes = {}
    for line in open(filename):
        left, right = line.strip().split(': ')
        if right.isdigit():
            nodes[left] = LitNode(int(right))
        else:
            lhs, op, rhs = right.split(' ')
            nodes[left] = ExprNode(lhs, op, rhs)
    return nodes

def part1(nodes):
    return int(round(nodes['root'].eval(nodes)))

def part2(nodes):
    nodes["humn"] = HumnNode()
    nodes["root"] = RootNode(nodes["root"].lhs, nodes["root"].rhs)
    return int(round(nodes["root"].solve(nodes)))

def main(filename):
    nodes = read_input(filename)
    print(part1(nodes))
    print(part2(nodes))

if __name__ == '__main__':
    main('input' if len(sys.argv) == 1 else sys.argv[1])
