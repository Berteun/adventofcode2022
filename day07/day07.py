#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pprint import pprint

def read_input():
    return open('input').readlines()


def get_current_path(dir_tree, current_dir):
    cur = dir_tree
    for name in current_dir:
        if not name in cur:
            cur[name] = {}
        cur = cur[name]
    return cur

def build_dir_tree(lines):
    current_dir = []
    dir_tree = {}
    working_dir = {}
    for l in lines:
        line = l.strip()
        if not line:
            continue
        if line.startswith('$'):
            prompt, command, *arg = line.split()
            if command == 'cd':
                if arg[0] == '/':
                    current_dir = []
                elif arg[0] == '..':
                    current_dir.pop()
                else:
                    current_dir.append(arg[0])
                working_dir = get_current_path(dir_tree, current_dir)
            else:
                pass
        elif line.startswith('dir'):
            _, dirname = line.split(' ')
            if not dirname in current_dir:
                working_dir[dirname] = {}
        else:
            size_str, file = line.split(' ')
            working_dir[file] = int(size_str)
    return dir_tree

def compute_sizes(dir_tree, path, all_dirs):
    size = 0
    for name in dir_tree:
        if isinstance(dir_tree[name], dict):
            size += compute_sizes(dir_tree[name], path + '.' + name, all_dirs)
        else:
            size += dir_tree[name]
    all_dirs[path] = size
    return size


def part1(inp):
    tree = build_dir_tree(inp)
    all_dirs = {}
    total_size = compute_sizes(tree, '', all_dirs)
    return(sum(v for v in all_dirs.values() if v < 100_000))

def part2(inp):
    tree = build_dir_tree(inp)
    all_dirs = {}
    total_size = compute_sizes(tree, '', all_dirs)

    total_space = 70_000_000
    needed_space = 30_000_000
    to_free = total_size - (total_space - needed_space)
    candidates = sorted((all_dirs[path], path) for path in all_dirs if all_dirs[path] >= to_free)
    return candidates[0][0]

def main():
    inp = read_input()
    print(part1(inp))
    print(part2(inp))

if __name__ == '__main__':
    main()
