'''Aoc Day13 Part1
find mirrored sections and total left columns for vertical matches and
100 times the rows above for horizontal matches'''

DEBUG = 5
filename = 'input13.txt'
#filename = 'test13-1.txt'

with open(filename) as f:
    ls = f.read().strip().split('\n')

# store each map as a set of rows and a set of columns
maps = []
i = 0
while i < len(ls):
    row_map = []
    col_map = []
    while i < len(ls) and ls[i] != '':
        row_map.append(ls[i])
        col_map.append([c for c in ls[i]])
        i += 1
    # make the col_map
    rotated_col_map = []
    for j in range(len(col_map[0])):
        temp_line = [col_map[k][j] for k in range(len(col_map)-1, -1, -1)]
        rotated_col_map.append(''.join(temp_line))
    maps.append([row_map, rotated_col_map])
    i += 1
# now the same function should work for either

def mirrorAt(m):
    '''Given a map, return the number of rows above the mirror point or
    zero if there are none'''
    for i in range(0, len(m) - 1):
        if m[i] == m[i+1]:
            found = True
            for x, j in enumerate(range(i+1, len(m))):
                if i - x > -1:
                    if m[i-x] != m[j]:
                        found = False
            if found:
                return(i + 1)
    return(0)

total = 0
for row_m, col_m in maps:
    total += mirrorAt(row_m) * 100 + mirrorAt(col_m)

print("Summary is", total)


# Part 2 - same thing, but fix an error in each mirror for a different match
def diff(r1, r2):
    '''see how many positions differ'''
    num_diff = sum([0 if r1[i] == r2[i] else 1 for i in range(len(r1))])
    return(num_diff)

def mirrorAt(m):
    '''Given a map, return the number of rows above the mirror point
    including exactly one fix or zero if there are none'''
    for i in range(0, len(m) - 1):
        if m[i] == m[i+1] or diff(m[i], m[i+1]) == 1:
            num_diff = 0
            for x, j in enumerate(range(i+1, len(m))):
                if i - x > -1:
                    num_diff += diff(m[i-x], m[j])
            if num_diff == 1:
                return(i + 1)
    return(0)

total = 0
for row_m, col_m in maps:
    total += mirrorAt(row_m) * 100 + mirrorAt(col_m)

print("Summary for part 2 is", total)
