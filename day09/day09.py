'''Aoc Day09 Part1
Find the sum of the forward extrapolation'''

DEBUG = 4
filename = 'input09.txt'
#filename = 'test09-1.txt'

with open(filename) as f:
    ls = f.read().strip().split('\n')

def toZero(h):
    '''Take in a sequence of ints and find differences until all 0s.
    Then return the list of lists that gets there'''
    to_zero = []
    local_h = h.copy()
    done = False
    while not done:
        if DEBUG > 4:
            s = ''
            for n in local_h:
                s = s + f'{n:<5}'
            print(s.center(30, ' '))
        to_zero.append(local_h)
        n_unique = list(set(local_h))
        if len(n_unique) == 1 and n_unique[0] == 0:
            done = True
            break
        new_list = []
        for i, n in enumerate(local_h):
            new_list.append(local_h[i+1] - local_h[i])
            if i > len(local_h) - 3:
                break
        local_h = new_list
    return(to_zero)

def findNext(tz):
    '''Given the "to zero" list of lists, return the next value in the
    first sequence'''
    next = 0
    for i in range(len(tz)-1, 0, -1):
        next += tz[i-1][-1]
    return(next)

total = 0
for l in ls:
    cur_to_zero = toZero([int(x) for x in l.split()])
    if DEBUG > 4:
        print(findNext(cur_to_zero))
    total += findNext(cur_to_zero)

print("The sum of the continued sequences is", total)

# Part2 - instead of going forward by one, extrapolate back by one
def findPrev(tz):
    '''Given the "to zero" list of lists, return the next value in the
    first sequence'''
    prev = 0
    for i in range(len(tz)-1, 0, -1):
        prev = tz[i-1][0] - prev
    return(prev)

total = 0
for l in ls:
    cur_to_zero = toZero([int(x) for x in l.split()])
    if DEBUG > 4:
        print(findPrev(cur_to_zero))
    total += findPrev(cur_to_zero)

print("The sum of the continued sequences is", total)

