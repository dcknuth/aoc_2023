'''Aoc Day18 Part1
how many cubic meters of lava can the lagoon hold?'''

DEBUG = 4
filename = 'input18.txt'
#filename = 'test18-1.txt'

with open(filename) as f:
    ls = f.read().strip().split('\n')

def pMap(m):
    for r in m:
        print(''.join(r))
    print()

digging = {'U':(-1, 0), 'R':(0,1), 'D':(1,0), 'L':(0,-1)}
def addMeter(m, d, p):
    '''Given the current matrix, a direction to dig a meter and the current
    position, dig the next meter and adjust the matrix as needed. Return
    the new position'''
    cur_y, cur_x = p
    # add a row on the top
    if cur_y + d[0] < 0:
        new_row = ['.' for x in m[0]]
        m.insert(0, new_row)
        m[0][cur_x] = '#'
        return([0, cur_x])
    # add a row on the bottom
    if cur_y + d[0] >= len(m):
        new_row = ['.' for x in m[0]]
        m.append(new_row)
        m[cur_y + d[0]][cur_x] = '#'
        return([cur_y + d[0], cur_x + d[1]])
    # add a column in front
    if cur_x + d[1] < 0:
        for r in m:
            r.insert(0, '.')
        m[cur_y][0] = '#'
        return([cur_y, 0])
    # add a column at the end
    if cur_x + d[1] >= len(m[0]):
        for r in m:
            r.append('.')
        m[cur_y + d[0]][cur_x + d[1]] = '#'
        return([cur_y, cur_x + d[1]])
    # any other move
    m[cur_y + d[0]][cur_x + d[1]] = '#'
    return([cur_y + d[0], cur_x + d[1]])

m = [['#',],]
cur_pos = [0, 0]
for l in ls:
    d, n, color = l.split()
    d = digging[d]
    n = int(n)
    color = color.strip('()')
    for i in range(n):
        cur_pos = addMeter(m, d, cur_pos)

if DEBUG > 4:
    pMap(m)

def fillMap(m):
    for y, r in enumerate(m):
        walls = 0
        counting = True
        for x, c in enumerate(r):
            if c == '#' and counting:
                walls += 1
                counting = False
            if c == '.' and walls % 2 == 1:
                counting = True
                m[y][x] = '#'

if DEBUG > 4:
    fillMap(m)

meters = 0
for r in m:
    meters += ''.join(r).count('#')
print("Total meters is", meters)
