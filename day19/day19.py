#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import sys
from dataclasses import dataclass
from collections import namedtuple, deque, defaultdict

Cost = namedtuple('Cost', ['bot', 'ore', 'clay', 'obsidian'])

@dataclass
class Blueprint:
    bp_id: int
    ore: Cost
    clay: Cost
    obsidian: Cost
    geode: Cost

input_re = re.compile(r'Blueprint (?P<bp_id>\d+): Each ore robot costs (?P<ore_ore_cost>\d+) ore. Each clay robot costs (?P<clay_ore_cost>\d+) ore. Each obsidian robot costs (?P<obs_ore_cost>\d+) ore and (?P<obs_clay_cost>\d+) clay. Each geode robot costs (?P<geode_ore_cost>\d+) ore and (?P<geode_obs_cost>\d+) obsidian.')
def read_input(filename):
    blueprints = []
    for line in open(filename):
        d = input_re.match(line.strip()).groupdict()
        blueprints.append(
            Blueprint(bp_id=int(d["bp_id"]),
                      ore=Cost('ore', int(d["ore_ore_cost"]), 0, 0),
                      clay=Cost('clay', int(d["clay_ore_cost"]), 0, 0),
                      obsidian=Cost('obs', int(d["obs_ore_cost"]), int(d["obs_clay_cost"]), 0),
                      geode=Cost('geo', int(d["geode_ore_cost"]), 0, int(d["geode_obs_cost"])))
        )
    return blueprints

State = namedtuple('State', ['min', 'ore', 'clay', 'obs', 'geo', 'ore_bot', 'clay_bot', 'obs_bot', 'geo_bot'])
def quality(blueprint, minutes):
    max_ore_cost = max(blueprint.ore.ore, blueprint.clay.ore, blueprint.obsidian.ore, blueprint.geode.ore)
    max_clay_cost = max(blueprint.ore.clay, blueprint.clay.clay, blueprint.obsidian.clay, blueprint.geode.clay)
    max_obs_cost = max(blueprint.ore.obsidian, blueprint.clay.obsidian, blueprint.obsidian.obsidian, blueprint.geode.obsidian)


    best_geodes = defaultdict(int)
    initial_state = State(min=1, ore=0, clay=0, obs=0, geo=0, ore_bot=1, clay_bot=0, obs_bot=0, geo_bot=0)
    queue = deque([initial_state])
    max_geodes = 0
    seen = set()
    last_min = 0
    while queue:
        state = queue.popleft()
        #print(state)
        new_states = []
        if state.min > last_min:
            #print(state.min)
            last_min = state.min
        best_geodes[state.min] = max(state.geo_bot, best_geodes[state.min])
        # Seems a losing state
        if state.geo_bot + 2 < best_geodes[state.min] or state.geo_bot + 2 < best_geodes[state.min - 1]:
            continue
        # Spend to build
        for c in [blueprint.ore, blueprint.clay, blueprint.obsidian, blueprint.geode]:
            if c.bot == 'ore' and state.ore_bot >= max_ore_cost:
                continue
            if c.bot == 'clay' and state.clay_bot >= max_clay_cost:
                continue
            if c.bot == 'obs' and state.obs_bot >= max_obs_cost:
                continue

            if c.ore <= state.ore and c.clay <= state.clay and c.obsidian <= state.obs and (c.ore * 3 > state.ore or c.clay * 3 > state.clay or c.obsidian * 3 > state.obs):
                #print(f'could build {c.bot} bot')
                new_states.append(
                    State(state.min + 1, state.ore - c.ore, state.clay - c.clay, state.obs - c.obsidian, state.geo,
                          state.ore_bot + (c.bot == 'ore') , state.clay_bot + (c.bot == 'clay'), state.obs_bot + (c.bot == 'obs'), state.geo_bot + (c.bot == 'geo'))
                )
        # Don't build anything
        new_states.append(State(state.min + 1, state.ore, state.clay, state.obs, state.geo,
                  state.ore_bot, state.clay_bot, state.obs_bot, state.geo_bot))

        # Harvest
        for ns in new_states:
            # Push state
            nns = State(ns.min, ns.ore + state.ore_bot, ns.clay + state.clay_bot, ns.obs + state.obs_bot, ns.geo + state.geo_bot,  ns.ore_bot, ns.clay_bot, ns.obs_bot, ns.geo_bot)
            max_geodes = max(max_geodes, nns.geo)
            if nns.min <= minutes and not nns in seen:
                seen.add(nns)
                queue.append(nns)
    #print(blueprint.bp_id, max_geodes)
    return max_geodes

def part1(blueprints):
    return sum(bp.bp_id * quality(bp, minutes=24) for bp in blueprints)

def part2(blueprints):
    mul = 1
    for m in [quality(bp, minutes=32) for bp in blueprints]:
        mul *= m
    return mul

def main(filename):
    blueprints = read_input(filename)
    print(part1(blueprints))
    print(part2(blueprints[:3]))

if __name__ == '__main__':
    main('input' if len(sys.argv) == 1 else sys.argv[1])
