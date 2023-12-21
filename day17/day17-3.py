'''Aoc Day17 Part1
move the lava with minimum heat loss'''
import networkx as nx
from collections import defaultdict
import heapq, math

DEBUG = 5
#filename = 'input17.txt'
filename = 'test17-1.txt'
#filename = 'test17-2.txt'

with open(filename) as f:
    ls = f.read().strip().split('\n')

def addEdges(m, g):
    '''Given a matrix and a graph, add edges from all the nodes with
    correct weights'''
    for y in range(len(m)):
        for x in range(len(m[0])):
            cur = (y, x)
            if y > 0:
                g.add_edge(cur, (y-1, x), weight=int(m[y-1][x]))
            if y < len(m) - 1:
                g.add_edge(cur, (y+1, x), weight=int(m[y+1][x]))
            if x > 0:
                g.add_edge(cur, (y, x-1), weight=int(m[y][x-1]))
            if x < len(m[0]) - 1:
                g.add_edge(cur, (y, x+1), weight=int(m[y][x+1]))

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

def getShortList(g, start_list, dest_list, n, min_nodes):
    '''Given a graph, list of start nodes, a list of destination nodes, a
    number of paths to find and the min number of destination nodes, find
    the shortest pathes from a list of starting locations to a list of
    destination locations. Return a list of the shortest paths'''
    per_node = n
    found = []
    total_found = 0
    for start in start_list:
        for dest in dest_list:
            path_gen = nx.shortest_simple_paths(g, start, dest,
                                                weight='weight')
            node_num = 0
            for p in path_gen:
                if testPath(p) < 0:
                    w = nx.path_weight(g, p, weight='weight')
                    node_num += 1
                    total_found += 1
                    heapq.heappush(found, [w, (start, dest), p])
                if node_num >= per_node:
                    break
    # we now have a lot of paths, filter until we get the numbers we want
    paths = []
    num_added = 0
    num_nodes = dict()
    while (num_added < n or len(num_nodes) < min_nodes) and len(found) > 0:
        cur_path = heapq.heappop(found)
        heapq.heappush(paths, cur_path)
        num_added += 1
        num_nodes[cur_path[1]] = True
    return(paths)

def genDestList(m, step):
    '''Returns the diagonal coords at the requested step'''
    dest_list = []
    y = x = step
    dest_list.append((y, x))
    y += 1
    x -= 1
    while x > -1 and y < len(m):
        dest_list.append((y, x))
        y += 1
        x -= 1
    y = step - 1
    x = step + 1
    while x < len(m[0]) and y > -1:
        dest_list.append((y, x))
        y -= 1
        x += 1
    return(dest_list)

def addFilterTest(gl, cl, n):
    '''Add current paths to the matching start, check for too straight,
    return the best n paths as a dict by destination'''
    temp_sl = defaultdict(list)
    while len(cl) > 0:
        weight, start_stop, path = heapq.heappop(cl)
        cur_start, cur_dest = start_stop
        while len(gl[cur_start]) > 0:
            start_p = heapq.heappop(gl[cur_start])
            new_path = start_p[1][:-1] + path
        if testPath(new_path) < 0:
            heapq.heappush(temp_sl[cur_dest], [weight + start_p[0], new_path])
    # we should have a new list of valid starts, prune to n per dest
    new_sl = defaultdict(list)
    for node in temp_sl.keys():
        # put n from each node in list to return
        new_heap = []
        for i in range(n):
            if len(temp_sl[node]) > 0:
                heapq.heappush(new_heap, heapq.heappop(temp_sl[node]))
        new_sl[node] = new_heap
    return(new_sl)

NUM_PATHS = 20
NUM_NODES = 10
SLICE = 5
SLICE_PATHS = 10 # up to this number of paths per node
m = []
for l in ls:
    m.append([int(x) for x in l])
g = nx.DiGraph()
addEdges(m, g)
start_list = [(0, 0)]
good_paths = defaultdict(list)
heapq.heappush(good_paths[start_list[0]], [0, start_list])
step = SLICE
while step < len(m) and step < len(m[0]):
    dest_list = genDestList(m, step)
    cur_list = getShortList(g, start_list, dest_list, NUM_PATHS, NUM_NODES)
    good_paths = addFilterTest(good_paths, cur_list, SLICE_PATHS)
    start_list = list(good_paths.keys())
    step += SLICE
# only the last part to the end node left
dest_list = [(len(m) - 1, len(m[0]) - 1)]
cur_list = getShortList(g, start_list, dest_list, NUM_PATHS, NUM_NODES)
good_paths = addFilterTest(good_paths, cur_list, SLICE_PATHS)
best = good_paths[dest_list[0]]
p = heapq.heappop(best)
print("shortest path is", p[1], "with length", len(p[1])-1)
print("Path weight is", p[0])
