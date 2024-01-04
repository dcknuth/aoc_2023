'''AoC Day25 Part1 - remove three wires to create two groups'''
import networkx as nx
import matplotlib.pyplot as plt

#filename = "test25-1.txt"
filename = "input25.txt"

with open(filename) as f:
    ls = f.read().strip().split('\n')

# Maybe we can load into networkx and just do a large print and visually
#  spot the three connections?
g = nx.Graph()
for l in ls:
    n1, node_list = l.split(': ')
    node_list = node_list.split()
    for node in node_list:
        g.add_edge(n1, node)

# nx.draw(g, with_labels=True)
# plt.show()
# That worked oddly well. The three connections are:
# jmn - zfk
# kdc - pmn
# grd - hvm

g.remove_edge('jmn', 'zfk')
g.remove_edge('kdc', 'pmn')
g.remove_edge('grd', 'hvm')

# Now a test print
# nx.draw(g, with_labels=True)
# plt.show()
# Yep, seems to have split in two

# Then maybe use single source shortest for a node in each group and see what
#  the size is
g1 = nx.single_source_shortest_path(g, 'jmn')
g2 = nx.single_source_shortest_path(g, 'zfk')
size_group1 = 0
size_group2 = 0
for p in g1:
    size_group1 += 1
for p in g2:
    size_group2 += 1
print("Product of the two group sizes is", size_group1 * size_group2)
