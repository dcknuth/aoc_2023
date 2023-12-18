'''Aoc Day17 Part1
move the lava with minimum heat loss'''
import networkx as nx

DEBUG = 5
#filename = 'input17.txt'
filename = 'test17-1.txt'
#filename = 'test17-2.txt'

with open(filename) as f:
    ls = f.read().strip().split('\n')

def addEdges(sy, sx, sm, sg):
    '''Given a start y index, a start x index, the input matrix and a
     graph, add edges from all the nodes with correct weights'''
    for y in range(len(sm)):
        for x in range(len(sm[0])):
            cur = (sy+y, sx+x)
            if y > 0:
                sg.add_edge(cur, (sy+(y-1), sx+x), weight=int(sm[y-1][x]))
            if y < len(sm) - 1:
                sg.add_edge(cur, (sy+y+1, sx+x), weight=int(sm[y+1][x]))
            if x > 0:
                sg.add_edge(cur, (sy+y, sx+(x-1)), weight=int(sm[y][x-1]))
            if x < len(sm[0]) - 1:
                sg.add_edge(cur, (sy+y, sx+x+1), weight=int(sm[y][x+1]))

def testPath(p):
    '''Given a path, return the path index where there are five consecutive
    y or x values in a row (straight for five nodes/4 steps), otherwise
    return -1'''
    for i, cur in enumerate(p):
        if i > 3:
            if cur[0] == p[i-1][0] and cur[0] == p[i-2][0] and \
                cur[0] == p[i-3][0] and cur[0] == p[i-4][0]:
                return(i)
            if cur[1] == p[i-1][1] and cur[1] == p[i-2][1] and \
                cur[1] == p[i-3][1] and cur[1] == p[i-4][1]:
                return(i)
    return(-1)

# Find the shortest, then make the weight very high at any fifth straight
#  step and solve again
HEAVY = 1000
m = []
for l in ls:
    m.append([int(x) for x in l])
g = nx.DiGraph()
addEdges(0, 0, m, g)
found = False
while not found:
    p = nx.shortest_path(g, (0, 0), (len(m)-1, len(m[0])-1), weight='weight')
    too_straight = testPath(p)
    if too_straight < 0:
        found = True
    else:
        # TODO add a bunch of weight to the last node in the straight
        g.add_edge(p[too_straight-1], p[too_straight], weight=HEAVY)

print("shortest path is", p, "with length", len(p)-1)
print("Path weight is", nx.path_weight(g, p, weight='weight'))
