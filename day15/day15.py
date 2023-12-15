'''Aoc Day15 Part1
find HASH value of my string'''

DEBUG = 4
hash_str = 'HASH'
#filename = 'test15-1.txt'
filename = 'input15.txt'

with open(filename) as f:
    l = f.read().strip().split(',')

def hashIt(s):
    '''Takes a string, does the instructed steps on it and returns the
    hash number'''
    hval = 0
    for c in s:
        hval += ord(c)
        hval *= 17
        hval %= 256
    return(hval)

print("The hashed value of HASH is", hashIt(hash_str))

total = 0
for hs in l:
    total += hashIt(hs)

print("The sum of hash values is", total)


'''Part 2 - operate on the given sequence to get 256 sets of lenses. Then
add up the 'focusing power' of all the lenses. Will assume there are not
too many non-append list operations to just use a plain list for each
box'''
# set up our 'boxes'
boxes = [[] for i in range(256)]
# remember the focal lengths
focal_lens = dict()

def loadLens(boxes, i, fls):
    '''Given a set of boxes, an instruction and the focal length
    dictionary (fls), set the lens into the box and remember the fls'''
    if '-' in i:
        label = i[:-1]
        box = hashIt(label)
        if label in boxes[box]:
            boxes[box].remove(label)
            del fls[':'.join([str(box), label])]
    elif '=' in i:
        label, n = i.split('=')
        box = hashIt(label)
        if label in boxes[box]:
            fls[':'.join([str(box), label])] = n
        else:
            boxes[box].append(label)
            focal_lens[':'.join([str(box), label])] = n
    else:
        print("Error: Processing instruction", i)

def pBoxes(boxes, fls):
    '''Print the status of the boxes with the focal lenght for each
    lens'''
    for i, box in enumerate(boxes):
        if len(box) > 0:
            box_cont = []
            for label in box:
                fl = ':'.join([str(i), label])
                box_cont.append(' '.join([label, fls[fl]]))
                box_str = '[' + '] ['.join(box_cont) + ']'
            print(f"Box {i}: {box_str}")

for ins in l:
    loadLens(boxes, ins, focal_lens)
    if DEBUG > 4:
        print(f'After "{ins}":')
        pBoxes(boxes, focal_lens)
        print()

def calcPow(boxes, fls):
    '''Given the boxes and focal powers, return the total power'''
    total = 0
    for i, box in enumerate(boxes):
        for j, lens in enumerate(box):
            fl = int(fls[':'.join([str(i), lens])])
            total += (1 + i) * (j+1) * fl
    return(total)

t_pow = calcPow(boxes, focal_lens)
print("Total focusing power is", t_pow)
