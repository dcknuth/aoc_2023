'''Aoc Day08 Part1
Find the number of steps to ZZZ'''

filename = 'input08.txt'
#filename = 'test08-1.txt'
#filename = 'test08-2.txt'
#filename = 'test08-3.txt'

with open(filename) as f:
    ls = f.read().strip().split('\n')

instructions = [0 if x == 'L' else 1 for x in ls[0]]
netw = dict()
for l in ls[2:]:
    node, dests = l.split(' = ')
    dests = list(dests.strip('()').split(', '))
    netw[node] = dests

cur_node = 'AAA'
i_pos = 0
steps = 0
while cur_node != 'ZZZ':
    cur_node = netw[cur_node][instructions[i_pos]]
    i_pos = (i_pos + 1) % len(instructions)
    steps += 1

print("Total number of steps to ZZZ is", steps)

# Part2 - go in parellel from nodes ending in A until on ones that end in Z
#  then get the LCM to get how long for all (too many without this)
from collections import Counter
import math
n_counts = Counter()
n_list = [n for n in netw.keys() if n[2] == 'A']
n_list = [[x, x] for x in n_list]
i_pos = 0
while len(n_list) > 0:
    new_list = []
    for source, current in n_list:
        cur_next = netw[current][instructions[i_pos]]
        if cur_next[2] == "Z":
            n_counts[source] += 1
        else:
            n_counts[source] += 1
            new_list.append([source, cur_next])
    i_pos = (i_pos + 1) % len(instructions)
    n_list = new_list

unique_steps = set(n_counts.values())
steps = math.lcm(*unique_steps)
print("Total number of steps to ZZZ is", steps)
