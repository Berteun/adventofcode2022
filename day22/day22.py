#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from collections import defaultdict, namedtuple

def parse_board(board_str):
    board = defaultdict(lambda: ' ')
    for y, line in enumerate(board_str.split("\n")):
        for x, c in enumerate(line):
            board[x + y * 1j] = c
    return board


UP    = -1j 
LEFT  = -1
RIGHT =  1
DOWN  =  1j 

Action = namedtuple('Action', ['type', 'value'])

def move_to_other_face(pos, orientation):
    y = pos.imag
    x = pos.real

    # Vertical faces
    if   x == -1  and 100 <= y <= 149:
        return 50 + (149 - y) * 1j, RIGHT
    elif x == -1  and 150 <= y <= 199:
        return (y - 100, DOWN)
    elif x == 49  and   0 <= y <= 49:
        return (149 - y) * 1j, RIGHT
    elif x == 49  and  50 <= y <= 99:
        return y - 50 + 100j, DOWN
    elif x == 50  and 150 <= y <= 199:
        return y - 100 + 149j, UP
    elif x == 100 and  50 <= y <= 99:
        return 50 + y + 49j, UP
    elif x == 100 and 100 <= y <= 149:
        return 149 + (149 - y) * 1j, LEFT
    elif x == 150 and   0 <= y <= 149:
        return 99 + (149 - y) * 1j, LEFT

    # Horizontal faces
    elif y == -1  and  50 <= x <= 99:
        return (100 + x) * 1j, RIGHT
    elif y == -1  and 100 <= x <= 149:
        return x - 100 + 199j, UP
    elif y == 50  and 100 <= x <= 149:
        return 99 + (x - 50) * 1j, LEFT
    elif y == 99  and 0 <= x <= 49:
        return 50 + (50 + x) * 1j, RIGHT
    elif y == 150 and 50 <= x <= 99:
        return 49 + (100 + x) * 1j, LEFT
    elif y == 200 and  0 <= x <= 49:
        return 100 + x, DOWN
    raise RuntimeError(f"wrong input x={x} y={y}, orientation={get_char(orientation)}")

def parse_route(route_str):
    state = 'digit'
    pos = 0
    number = ''
    actions = []
    while pos < len(route_str):
        if route_str[pos].isdigit():
            number += route_str[pos]
        elif route_str[pos] in ('L', 'R'):
            if number:
                actions.append(Action(type='move', value=int(number)))
                number = ''
            actions.append(Action(type='turn', value=1j if route_str[pos] == 'R' else -1j))
        else:
            raise RuntimeError(f"pos={pos}, unexpected character: {route_str[pos]}")
        pos += 1
    if number:
        actions.append(Action(type='move', value=int(number)))
    return actions

def read_input(filename):
    board_str, route_str = open(filename).read().split("\n\n")
    return parse_board(board_str), parse_route(route_str.strip())

def get_bounds(board):
    return int(max(c.real for c in board)), int(max(c.imag for c in board))

def get_char(orientation):
    return {RIGHT:'>',UP:'^',LEFT:'<',DOWN:'v'}[orientation]

def print_board(board, pos, orientation):
    x_max, y_max = get_bounds(board)
    for y in range(y_max):
        for x in range(x_max):
            if (x + y * 1j) == pos:
                print(get_char(orientation), sep='', end='')
            else:
                print(board[x + y * 1j], sep='', end='')
        print()
    print()

def orientation_value(orientation):
    return {
        RIGHT: 0, 
        DOWN : 1,
        LEFT : 2,
        UP   : 3,
    }[orientation]

def do_action(action, board, pos, orientation, x_max, y_max):
    if action.type == 'turn':
        old_orientation = orientation
        orientation *= action.value
    if action.type == 'move':
        for n in range(action.value):
            prev_pos = pos
            pos += orientation
            while board[pos] == ' ':
                if pos.real > x_max:
                    pos = 0 + 1j * int(pos.imag)
                elif pos.real < 0:
                    pos = x_max + 1j * int(pos.imag)
                elif pos.imag > y_max:
                    pos = int(pos.real) + 0j
                elif pos.imag < 0:
                    pos = int(pos.real) + y_max * 1j
                else:
                    pos += orientation
            if board[pos] == '.':
                continue
            elif board[pos] == '#':
                pos = prev_pos
            else:    
                raise RuntimeError("incorrect move")

    return pos,orientation

def get_start(board, x_max):
    for x in range(x_max):
        if board[x + 0j] == '.':
            return x + 0j

def part1(board, route):
    x_max, y_max = get_bounds(board)
    pos = get_start(board, x_max)
    orientation = 1 + 0j
    for action in route:
        pos, orientation = do_action(action, board, pos, orientation, x_max, y_max)
    return int(1000 * (pos.imag + 1) + 4 * (pos.real + 1) + orientation_value(orientation))

def do_action_2(action, board, pos, orientation):
    if action.type == 'turn':
        old_orientation = orientation
        orientation *= action.value
    if action.type == 'move':
        for n in range(action.value):
            prev_pos = pos
            prev_orientation = orientation
            pos += orientation
            if board[pos] == '.':
                continue
            elif board[pos] == '#':
                pos = prev_pos
            else:    
                pos, orientation = move_to_other_face(pos, orientation)
                if board[pos] == '#':
                    pos, orientation = prev_pos, prev_orientation

    return pos,orientation

def part2(board, route):
    x_max, y_max = get_bounds(board)
    pos = get_start(board, x_max)
    orientation = 1 + 0j
    for action in route:
        pos, orientation = do_action_2(action, board, pos, orientation)
    return int(1000 * (pos.imag + 1) + 4 * (pos.real + 1) + orientation_value(orientation))

def main(filename):
    board, route = read_input(filename)
    print(part1(board, route))
    print(part2(board, route))

if __name__ == '__main__':
    main('input' if len(sys.argv) == 1 else sys.argv[1])
