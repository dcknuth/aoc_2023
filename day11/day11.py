'''Aoc Day11 Part1
add some expansion rows and columns, then sum the Manhatten distances'''
import numpy as np

DEBUG = 4
filename = 'input11.txt'
#filename = 'test11-1.txt'

with open(filename) as f:
    ls = f.read().strip().split('\n')

# make a list of lists that can be summed to find empty rows
m = []
for l in ls:
    m.append([0 if x == '.' else 1 for x in l])
# then a numpy array
a = np.array(m)
# add the empty columns then rows
def addColumnsRows(a):
    '''Takes in the original array and adds the needed columns and rows'''
    # first columns
    cur = 0
    while cur < a.shape[1]:
        if sum(a[:,cur]) == 0:
            zero_column = np.zeros((a.shape[0], 1), dtype=int)
            a = np.concatenate([a[:,:cur+1], zero_column, a[:,cur+1:]], axis=1)
            cur += 2
        else:
            cur += 1
    # now rows
    cur = 0
    while cur < a.shape[0]:
        if sum(a[cur,:]) == 0:
            zero_row = np.zeros((1, a.shape[1]), dtype=int)
            a = np.concatenate([a[:cur+1,:], zero_row, a[cur+1:,:]])
            cur += 2
        else:
            cur += 1
    return(a)

if DEBUG > 4:
    print("Shape before", a.shape)
    print(a)
a = addColumnsRows(a)
if DEBUG > 4:
    print("Shape after", a.shape)
    print(a)

# get the planet locations
rows, cols = np.where(a == 1)
if DEBUG > 4:
    print(rows, "\n", cols)
# now calculate all the distances and add them up
total = 0
for i in range(len(rows)-1):
    total += sum(abs(rows[i+1:] - rows[i])) + sum(abs(cols[i+1:] - cols[i]))
print("Total sum of all distances is", total)


'''Part2 - each added blank row should instead be to replace by 1,000,000.
We can add an array for the expansion rows and one for the expansion
columns and then add the correct number of millions for each distance'''
a = np.array(m)
expand_row = np.array(a.sum(axis=1) == 0, dtype=int)
expand_col = np.array(a.sum(axis=0) == 0, dtype=int)

# now the same walk with the added amount needed for each
mb = 1000000
rows, cols = np.where(a == 1)
total = 0
for i in range(len(rows)-1):
    sub_total = 0
    for r, c in zip(rows[i+1:], cols[i+1:]):
        lr = rows[i] if rows[i] < r else r
        hr = rows[i] if rows[i] > r else r
        erows = expand_row[lr:hr].sum()
        sub_total += abs(r-rows[i]) + mb * erows - erows
        lc = cols[i] if cols[i] < c else c
        hc = cols[i] if cols[i] > c else c
        ecols = expand_col[lc:hc].sum()
        sub_total += abs(c-cols[i]) + mb * ecols - ecols
    total += sub_total
print("Total sum of all distances is", total)
