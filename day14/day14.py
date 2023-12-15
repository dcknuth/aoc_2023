'''Aoc Day14 Part1
count up north rock load'''

DEBUG = 4
filename = 'input14.txt'
#filename = 'test14-1.txt'

with open(filename) as f:
    ls = f.read().strip().split('\n')

m = []
for l in ls:
    m.append(list(l))

def moveNorth(m):
    '''Move all the rolling rocks as far North as they will go'''
    for y in range(1, len(m)):
        for x, c in enumerate(m[y]):
            new_y = -1
            if c == 'O':
                for dy in range(y-1, -1, -1):
                    if m[dy][x] == '.':
                        new_y = dy
                    else:
                        break
            if new_y != -1:
                m[new_y][x] = 'O'
                m[y][x] = '.'

moveNorth(m)

def calcLoad(m):
    '''Give a loading pattern, return the total load'''
    total_load = 0
    for y, r in enumerate(m):
        row_val = len(m) - y
        for x, c in enumerate(m[y]):
            if c == 'O':
                total_load += row_val
    return(total_load)

total = calcLoad(m)
print("Total load on the north support beams is", total)


''' Part 2 - tilt N, W, S, E and then calculate the north load after
1,000,000,000 cycles'''
m = []
for l in ls:
    m.append(list(l))

# I imagine we will find a loop, but first do each move
def moveWest(m):
    '''Move all the rolling rocks as far West as they will go'''
    for y, r in enumerate(m):
        for x, c in enumerate(r):
            new_x = -1
            if x == 0:
                continue
            if c == 'O':
                for dx in range(x-1, -1, -1):
                    if m[y][dx] == '.':
                        new_x = dx
                    else:
                        break
            if new_x != -1:
                m[y][new_x] = 'O'
                m[y][x] = '.'

def moveSouth(m):
    '''Move all the rolling rocks as far South as they will go'''
    for y in range(len(m)-2, -1, -1):
        for x, c in enumerate(m[y]):
            new_y = -1
            if c == 'O':
                for dy in range(y+1, len(m)):
                    if m[dy][x] == '.':
                        new_y = dy
                    else:
                        break
            if new_y != -1:
                m[new_y][x] = 'O'
                m[y][x] = '.'

def moveEast(m):
    '''Move all the rolling rocks as far East as they will go'''
    for y in range(len(m)):
        for x in range(len(m[0])-2, -1, -1):
            new_x = -1
            if m[y][x] == 'O':
                for dx in range(x+1, len(m[0])):
                    if m[y][dx] == '.':
                        new_x = dx
                    else:
                        break
            if new_x != -1:
                m[y][new_x] = 'O'
                m[y][x] = '.'

def doCycle(m):
    '''Given a map, Do a cycle'''
    moveNorth(m)
    moveWest(m)
    moveSouth(m)
    moveEast(m)

# Let's go until we see the same exact config reappear and then use that
# as a loop that will get us to 1B
from collections import defaultdict
map_states = defaultdict(int)
l_list = []
loop_index = -1
loop_len = -1
total_cycles = 1000000000
for i in range(total_cycles):
    doCycle(m)
    load = calcLoad(m)
    m_state = ''
    for r in m:
        m_state = m_state + ''.join(r)
    if map_states[m_state] > 0:
        print("Found loop")
        loop_index = map_states[m_state] - 1
        loop_len = i - loop_index
        break
    map_states[m_state] = i + 1
    l_list.append(load)

num_loops = (total_cycles - (loop_index + 1)) // loop_len
last_loop_num = (loop_index+1) + num_loops * loop_len
last_load = l_list[loop_index + (total_cycles-last_loop_num)]
print("Last load north after 1B cycles is", last_load)
