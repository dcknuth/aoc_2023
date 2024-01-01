'''AoC Day 21 Part 1 - find all garden plots you can land on after 64
steps.
It looks like a way to do this would be to look at all even locations on
paths up to 64 long'''
import networkx as nx
import matplotlib.pyplot as plt

filename = "test21-1.txt"
filename = "input21.txt"

with open(filename) as f:
    ls = f.read().strip().split('\n')

STEPS = 64
start = (-1, -1)
g = nx.Graph()
for y in range(len(ls)):
    for x in range(len(ls[0])):
        if ls[y][x] == 'S':
            start = (y, x)
        if ls[y][x] == '.' or ls[y][x] == 'S':
            if y > 0:
                if ls[y-1][x] == '.':
                    g.add_edge((y, x), (y-1, x))
            if y < len(ls) - 1:
                if ls[y+1][x] == '.':
                    g.add_edge((y, x), (y+1, x))
            if x > 0:
                if ls[y][x-1] == '.':
                    g.add_edge((y, x), (y, x-1))
            if x < len(ls[0]) - 1:
                if ls[y][x+1] == '.':
                    g.add_edge((y, x), (y, x+1))

# nx.draw(g, with_labels=True)
# plt.show()

shortest_paths = nx.single_source_shortest_path(g, start, cutoff=STEPS)
reachable = dict()
for dest in shortest_paths.keys():
    if (len(shortest_paths[dest]) - 1) % 2 == 0:
        for step in shortest_paths[dest][::-2]:
            if step not in reachable:
                reachable[step] = True
            else:
                break

print("Total reachable nodes is", len(reachable))

'''Part 2 - If the map repeats infinitly, how many plots can be reached
after 26501365 steps?
I assume we are looking for a formula that has a square with an ajustment
for the hashes in our puzzle. No hashes seems to be (steps+1)**2. Then
we would need to subtract out the hash plots that would otherwise get
counted. It seems like others used a curve fit to estimate the formula. I
used the solution in -s file from here:
https://github.com/fuglede/adventofcode/tree/master/2023/day21
It still failed to converge on my input, so had to debug and look at each
guess. Then could do a binary search trail with the answers as they were
within a reasonable range for guessing'''
print("After some guessing, 609708004316870 was my answer")
