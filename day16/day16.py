#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import itertools
from functools import cache
from dataclasses import dataclass
from typing import Dict,List

@dataclass
class Node:
    name: str
    flow_rate: int
    neighbours: List[str]
    dist_to_valves: Dict[str, int]

def read_input(filename):
    g = {}
    for l in open(filename):
        line = l.strip().split(' ')
        name = line[1]
        rate = int(line[4][5:-1])
        tunnels = [t.rstrip(',') for t in line[9:]]
        g[name] = Node(name, rate, tunnels, {})
    return g

def floyd_warshall(graph):
    nodes = list(graph.keys())
    dist = {}
    for node in graph.values():
        dist[(node.name,node.name)] = 0
        for nb in node.neighbours:
            dist[(node.name, nb)] = 1

    for k in nodes:
        for l in nodes:
            for m in nodes:
                if dist.get((l,m), 100) > dist.get((l,k), 100) + dist.get((k,m), 100):
                    dist[(l,m)] = dist[(l,k)] + dist[(k,m)]
    for source in graph:
        for target in graph:
            if source != target and (graph[source].flow_rate > 0 or source == 'AA') and graph[target].flow_rate > 0:
                graph[source].dist_to_valves[target] = dist[(source,target)]
    
def main(filename):
    graph = read_input(filename)
    floyd_warshall(graph)
    best_cache = {}
    valves = sum(1 for n in graph.values() if n.flow_rate > 0)

    @cache
    def solve(node, minutes, opened, recurse, max_open):
        if best_cache.get((node,opened,recurse), -1) > minutes:
            return 0
        else:
            best_cache[(node,opened,recurse)] = minutes

        if minutes <= 0 or len(opened) == max_open:
            if recurse:
                return solve('AA', 26, opened, False, max_open * 2)
            else:
                return 0

        if node not in opened and graph[node].flow_rate > 0:
            contribution = (minutes - 1) * graph[node].flow_rate
            max_flow = contribution + solve(node, minutes - 1, opened | {node}, recurse, max_open)
        else:
            max_flow = max((solve(nb, minutes - dist, opened, recurse, max_open) for (nb,dist) in graph[node].dist_to_valves.items() if not nb in opened), default=0)
        return max_flow 

    print(solve('AA', 30, frozenset(), False, valves))

    best_cache = {}
    print(solve('AA', 26, frozenset(), True, (valves + 1) // 2))

if __name__ == '__main__':
    main('input' if len(sys.argv) == 1 else sys.argv[1])
