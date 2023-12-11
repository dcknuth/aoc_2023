'''Aoc Day10 Part1
Find the farthest node in the loop'''
import networkx as nx

DEBUG = 5
filename = 'input10.txt'
#filename = 'test10-1.txt'
#filename = 'test10-2.txt'
#filename = 'test10-3.txt'
#filename = 'test10-4.txt'
#filename = 'test10-5.txt'
up = "7F|"
down = "LJ|"
left = "LF-"
right = "J7-"

with open(filename) as f:
    ls = f.read().strip().split('\n')

# Let's make sure there are '.'s around the edge so we don't have to do
#  edge case checks and turn the input into a 2D matrix
m = [['.' for x in range(len(ls[0]) + 2)]]
for l in ls:
    cur = ['.']
    for c in l:
        cur.append(c)
    cur.append('.')
    m.append(cur)
m.append(['.' for x in range(len(ls[0]) + 2)])

def connect(y, x, m, g):
    '''Given coordinates, the input matrix and the graph look for and add
    edges from the current node'''
    cur = m[y][x]
    if cur == '.':
        return()
    if cur == '|':
        if m[y-1][x] in up:
            g.add_edge((y, x), (y-1, x))
        if m[y+1][x] in down:
            g.add_edge((y, x), (y+1, x))
    elif cur == '-':
        if m[y][x-1] in left:
            g.add_edge((y, x), (y, x-1))
        if m[y][x+1] in right:
            g.add_edge((y, x), (y, x+1))
    elif cur == 'L':
        if m[y-1][x] in up:
            g.add_edge((y, x), (y-1, x))
        if m[y][x+1] in right:
            g.add_edge((y, x), (y, x+1))
    elif cur == 'J':
        if m[y-1][x] in up:
            g.add_edge((y, x), (y-1, x))
        if m[y][x-1] in left:
            g.add_edge((y, x), (y, x-1))
    elif cur == '7':
        if m[y+1][x] in down:
            g.add_edge((y, x), (y+1, x))
        if m[y][x-1] in left:
            g.add_edge((y, x), (y, x-1))
    elif cur == 'F':
        if m[y+1][x] in down:
            g.add_edge((y, x), (y+1, x))
        if m[y][x+1] in right:
            g.add_edge((y, x), (y, x+1))

def replaceStart(y, x, m):
    '''Given the coordinates of the start and the matrix, replace with the
    correct pipe'''
    if m[y-1][x] in up and m[y+1][x] in down:
        m[y][x] = '|'
    elif m[y][x-1] in left and m[y][x+1] in right:
        m[y][x] = '-'
    elif m[y-1][x] in up and m[y][x+1] in right:
        m[y][x] = 'L'
    elif m[y-1][x] in up and m[y][x-1] in left:
        m[y][x] = 'J'
    elif m[y+1][x] in down and m[y][x-1] in left:
        m[y][x] = '7'
    elif m[y+1][x] in down and m[y][x+1] in right:
        m[y][x] = 'F'
    else:
        print("Error: Did not find a replacement for Start")

# make a graph and load in edges. Also set and deal with the start
start = [0,0]
g = nx.Graph()
for y in range(1, len(m) - 1):
    for x in range(1, len(m[0]) - 1):
        if m[y][x] == 'S':
            start[0] = y
            start[1] = x
            replaceStart(y, x, m)
        connect(y, x, m, g)

shortest_lengths = nx.single_source_dijkstra_path_length(g, tuple(start))
lengths = list(shortest_lengths.values())
lengths.sort()
print("Farthest point is", lengths[-1], "steps away")


# Part 2 - see if non-loop points are inside of the loop
# Will try to use the fact that points inside will cross the loop an
#  odd number of times to get to a known outside point
def crosses(p, o, s1, s2):
   '''Take a point, the origin and a line segment from our loop path.
   Since we will always have segments that are horizontal or vertical
   testing with a diagonal, we should not have to worry about
   colinear lines'''
   def ccw(a, b, c):
       return((c[0] - a[0]) * (b[1] - a[1]) > (b[0] - a[0]) * (c[1] - a[1]))
   
   return(ccw(p, s1, s2) != ccw(o, s1, s2) and \
          ccw(p, o, s1) != ccw(p, o, s2))

# get all the line segments of the loop and also load a dict of them for
#  faster lookup of things not in the loop
line_segments = []
loop_nodes = dict()
start_node = tuple(start)
loop_nodes[start_node] = True
cur_node = start_node
next_node = list(g.neighbors(start_node))[0]
while next_node != start_node:
    loop_nodes[next_node] = True
    line_segments.append((cur_node, next_node))
    last_node = cur_node
    cur_node = next_node
    for n in g.neighbors(cur_node):
        if n != last_node:
            next_node = n
            break
line_segments.append((cur_node, next_node))
if DEBUG > 4:
    print("List of line segments is:", line_segments)

# look for non-loop points, test if each is in or out and count them
if DEBUG > 3:
    check_m = [x.copy() for x in m]
origin = (0, 0) # the origin is outside the way we created the matrix
total = 0
for y in range(1, len(m) - 1):
    for x in range(1, len(m[0]) - 1):
        if m[y][x] == '.' or (y, x) not in loop_nodes:
            cross_count = 0
            for seg in line_segments:
                if crosses(origin, (-y, x),
                           (-seg[0][0], seg[0][1]), (-seg[1][0], seg[1][1])):
                    cross_count += 1
            if cross_count % 2 == 1:
                total += 1
                if DEBUG > 3:
                    check_m[y][x] = 'I'
if DEBUG > 3:
    for row in check_m:
        print(''.join(row))
print("Number of empty spaces inside the loop is", total)
