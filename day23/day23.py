# -*- coding: utf-8 -*-
'''AoC Day 23 Part 1 - longest hike without using the same tile'''
import networkx as nx
import matplotlib.pyplot as plt

filename = "input23.txt"
#filename = "test23-1.txt"

with open(filename) as f:
    ls = f.read().strip().split('\n')

g = nx.DiGraph()
for y, l in enumerate(ls):
    for x, c in enumerate(l):
        if c != '#':
            if c == '.':
                if y > 0:
                    if ls[y-1][x] != 'v' and ls[y-1][x] != '#':
                        g.add_edge((y, x), (y-1, x))
                if y < len(ls) - 1:
                    if ls[y+1][x] != '^' and ls[y+1][x] != '#':
                        g.add_edge((y, x), (y+1, x))
                if x > 0:
                    if ls[y][x-1] != '>' and ls[y][x-1] != '#':
                        g.add_edge((y, x), (y, x-1))
                if x < len(ls[0]) - 1:
                    if ls[y][x+1] != '<' and ls[y][x+1] != '#':
                        g.add_edge((y, x), (y, x+1))
            elif c == '^':
                if y > 0:
                    if ls[y-1][x] != 'v' and ls[y-1][x] != '#':
                        g.add_edge((y, x), (y-1, x))
            elif c == 'v':
                if y < len(ls) - 1:
                    if ls[y+1][x] != '^' and ls[y+1][x] != '#':
                        g.add_edge((y, x), (y+1, x))
            elif c == '<':
                if x > 0:
                    if ls[y][x-1] != '>' and ls[y][x-1] != '#':
                        g.add_edge((y, x), (y, x-1))
            elif c == '>':
                if x < len(ls[0]) - 1:
                    if ls[y][x+1] != '<' and ls[y][x+1] != '#':
                        g.add_edge((y, x), (y, x+1))
            else:
                print(f"Error: In cell type with {c}")

# nx.draw(g, with_labels=True)
# plt.show()

source_x = ls[0].find('.')
source = (0, source_x)
dest_x = ls[-1].find('.')
dest = (len(ls) - 1, dest_x)

all_paths = list(nx.all_simple_paths(g, source, dest))
all_lenghts = list(map(len, all_paths))
all_lenghts.sort()
print("The longest, valid path is", all_lenghts[-1] - 1, "long")


'''Part 2 - You can treat directional slopes as normal. Now what is the
longest hike?'''
g2 = nx.Graph()
for y, l in enumerate(ls):
    for x, c in enumerate(l):
        if c != '#':
            if y > 0:
                if ls[y-1][x] != '#':
                    g2.add_edge((y, x), (y-1, x))
            if y < len(ls) - 1:
                if ls[y+1][x] != '#':
                    g2.add_edge((y, x), (y+1, x))
            if x > 0:
                if ls[y][x-1] != '#':
                    g2.add_edge((y, x), (y, x-1))
            if x < len(ls[0]) - 1:
                if ls[y][x+1] != '#':
                    g2.add_edge((y, x), (y, x+1))

all_paths2 = nx.all_simple_paths(g2, source, dest)
longest = 0
for cur_path in all_paths2:
    if len(cur_path) > longest:
        longest = len(cur_path)
        print("New longest found of", longest - 1)
print("The longest path is now", longest - 1, "long")
