'''Aoc Day18 Part2
how many cubic meters of lava can the lagoon hold? Use the modified
hex instructions. Part 1 runs to slow to keep waiting, so part2 is in
a new file and the part1 approch will no longer work as the segment
lengths are too long'''

DEBUG = 4
filename = 'input18.txt'
#filename = 'test18-1.txt'

with open(filename) as f:
    ls = f.read().strip().split('\n')

# we will want a vertice list to use with the Gauss Area formula
direction = {0:'R', 1:'D', 2:'L', 3:'U'}
p1_dir = {'R':(0,1), 'D':(-1, 0), 'L':(0,-1), 'U':(1,0)}
vectors = {0:(0,1), 1:(-1, 0), 2:(0,-1), 3:(1,0)}
v_list = [(0, 0)]
last_p = [0, 0]
p1_vlist = [(0, 0)]
p1_last_p = [0, 0]
for l in ls:
    d, n, color = l.split()
    p1_d = d
    p1_len = int(n)
    length = int(color[2:7], 16)
    d = int(color[-2])
    if DEBUG > 4:
        print(f"{color} = {direction[d]} {length}")
    vector = vectors[d]
    p1_vec = p1_dir[p1_d]
    new_y = last_p[0] + vector[0] * length
    p1_ny = p1_last_p[0] + p1_vec[0] * p1_len
    new_x = last_p[1] + vector[1] * length
    p1_nx = p1_last_p[1] + p1_vec[1] * p1_len
    v_list.append((new_y, new_x))
    p1_vlist.append((p1_ny, p1_nx))
    last_p[0] = new_y
    p1_last_p[0] = p1_ny
    last_p[1] = new_x
    p1_last_p[1] = p1_nx

def gaussArea(v_list):
    '''Take a list of verticies and return the contained area'''
    n = len(v_list) - 1
    area = 0
    for i in range(n):
        j = i + 1
        area += v_list[i][0] * v_list[j][1]
        area -= v_list[j][0] * v_list[i][1]
    return(abs(area) / 2)

# now we should be able to use the formula
area = gaussArea(v_list)
p1_area = gaussArea(p1_vlist)
print("The contained area is", area)
print("p1 area without thickness", p1_area)
# this is too low because of the thickness of the machine is one meter

def addThickness(v_list):
    '''The thickness is 1, so it's a little easier
    perimeter/2 + 1'''
    perim = 0
    n = len(v_list) - 1
    for i in range(n):
        dy = abs(v_list[i+1][0] - v_list[i][0])
        dx = abs(v_list[i+1][1] - v_list[i][1])
        perim += dy + dx
    return(perim / 2 + 1)

area = area + addThickness(v_list)
p1_area = p1_area + addThickness(p1_vlist)
print("The contained area including trench thickness is", area)
print("The p1 area including trench thickness is", p1_area)
