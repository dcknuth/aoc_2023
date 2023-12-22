'''Aoc Day18 Part1
how many cubic meters of lava can the lagoon hold?'''

DEBUG = 5
filename = 'input18.txt'
#filename = 'test18-1.txt'

with open(filename) as f:
    ls = f.read().strip().split('\n')

def pMap(m):
    for r in m:
        print(''.join(r))
    print()

digging = {'U':(-1, 0), 'R':(0,1), 'D':(1,0), 'L':(0,-1)}
def addMeter(m, sc, d, p):
    '''Given the current matrix, the start coords, a direction to dig a meter
    and the current position, dig the next meter and adjust the matrix and
    start coordinates as needed. Return the new position'''
    cur_y, cur_x = p
    # add a row on the top
    if cur_y + d[0] < 0:
        new_row = ['.' for x in m[0]]
        m.insert(0, new_row)
        m[0][cur_x] = '#'
        sc[0] += 1
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
        sc[1] += 1
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

def makeLoop(ld, sc, steps):
    '''Given the line dict, start and the list of steps, add all the lines'''
    cur_y, cur_x = sc
    color = ''
    for l in steps:
        d, n, color = l.split()
        d = digging[d]
        n = int(n)
        color = color.strip('()')
        new_y = cur_y + d[0] * n
        new_x = cur_x + d[1] * n
        ld[((cur_y, cur_x), (new_y, new_x))] = color
        cur_y = new_y
        cur_x = new_x
    # the last step lands on the starting square, so don't need this
    #ld[((cur_y, cur_x), (sc[0], sc[1]))] = color

def crosses(p, o, s1, s2):
   '''Take a point, the origin and a line segment from our loop path.
   Since we will always have segments that are horizontal or vertical
   testing with a diagonal, we should not have to worry about
   colinear lines'''
   def ccw(a, b, c):
       return((c[0] - a[0]) * (b[1] - a[1]) > (b[0] - a[0]) * (c[1] - a[1]))
   
   return(ccw(p, s1, s2) != ccw(o, s1, s2) and \
          ccw(p, o, s1) != ccw(p, o, s2))

def fillMap(m, line_list):
    '''Fills in the lagoon and returns a total area count'''
    test_point = (1, -1) # a point outside loop
    total = 0
    for y in range(0, len(m)):
        for x in range(0, len(m[0])):
            if m[y][x] == '#':
                total += 1
            elif m[y][x] == '.':
                cross_count = 0
                for seg in line_list.keys():
                    if crosses(test_point, (-y, x),
                                (-seg[0][0], seg[0][1]),
                                (-seg[1][0], seg[1][1])):
                        cross_count += 1
                if cross_count % 2 == 1:
                    total += 1
                    m[y][x] = '#'
    return(total)

m = [['#',],]
start_pos = [0, 0]
cur_pos = [0, 0]
for l in ls:
    d, n, color = l.split()
    d = digging[d]
    n = int(n)
    color = color.strip('()')
    for i in range(n):
        cur_pos = addMeter(m, start_pos, d, cur_pos)

if DEBUG > 4:
    with open("dig_map.txt", 'w') as f:
        for r in m:
            f.write(f"{''.join(r)}\n")

meters = 0
for r in m:
    meters += ''.join(r).count('#')
print("Total meters is", meters)

line_list = dict()
makeLoop(line_list, start_pos, ls)
total_area = fillMap(m, line_list)

if DEBUG > 4:
    with open("dig_map.txt", 'w') as f:
        for r in m:
            f.write(f"{''.join(r)}\n")

print("Total area after digging out it", total_area)
