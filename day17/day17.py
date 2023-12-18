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
            if y < len(sm):
                sg.add_edge(cur, (sy+y+1, sx+x), weight=int(sm[y+1][x]))
            if x > 0:
                sg.add_edge(cur, (sy+y, sx+(x-1)), weight=int(sm[y][x-1]))
            if x < len(sm[0]):
                sg.add_edge(cur, (sy+y, sx+x+1), weight=int(sm[y][x+1]))

def makeGraph(m, sy=0, sx=0, size=0):
    '''Given a matrix and a possible sub section, make a graph and load in
    edges. Return the sub-matrix and graph. We use a directed graph to use
    the weight given for the node we are moving to'''
    if size == 0:
        ey = len(m)
        ex = len(m[0])
    else:
        ey = sy + size
        ex = sx + size
    sm = []
    for y in m[sy:ey]:
        sm.append(m[y][sx:ex])
    sg = nx.DiGraph()
    addEdges(sy, sx, sm, sg)
    sub_range = ((sy, sx), (ey, ex)) # ey and ex are 1 past the final index
    return(sub_range, sg)

def goodPath(p):
    '''Given a path, return False if has five consecutive y or x values
    in a row (straight for five nodes/4 steps), otherwise, True'''
    for i, cur in enumerate(p):
        if i > 2:
            if cur[0] == p[i-1][0] and cur[0] == p[i-2][0] and \
                cur[0] == p[i-3][0]:
                return(False)
            if cur[1] == p[i-1][1] and cur[1] == p[i-2][1] and \
                cur[1] == p[i-3][1]:
                return(False)
    return(True)

# We are going to need to combine a breath and depth first search as
#  we can only finish about an 7x7 matrix quickly with the path checking
def solveSub(sg, sub_range, n_nodes, n_paths, start_l):
    '''Given a sub-graph, the minimum number of different nodes needed
    and a minimum number of paths needed and a list of start_nodes, return
    a dict of nodes with paths that have at least that number of different
    nodes and paths. Let's assume that we need to exit on the bottom or
    right of this sub-matrix (given by the sub_range)'''
    start, end = sub_range
    sy, sx = start
    ey, ex = end
    dest_paths = dict()
    for cur_y in range(sy, ey):
        cur_x = ex - 1
        shortest_paths = nx.shortest_simple_paths(sg, (1, 1),
                                              (len(m)-2,len(m[0])-2),
                                              weight='weight')
        # TODO dest_paths[(cur_y, cur_x)]
    

shortest_path = None
for p in shortest_paths:
    if goodPath(p):
        shortest_path = p
        break
print("shortest path is", shortest_path, "with length", len(shortest_path)-1)
