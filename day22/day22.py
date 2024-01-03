'''AoC Day 22 Part 1 - how many bricks could be safely disintigrated?
'''
import heapq
from collections import Counter

DEBUG = 4
#filename = "test22-1.txt"
filename = "input22.txt"

with open(filename) as f:
    ls = f.read().strip().split('\n')

bricks = []
for l in ls:
    b1, b2 = l.split('~')
    x1, y1, z1 = map(int, b1.split(','))
    x2, y2, z2 = map(int, b2.split(','))
    if z1 < z2:
        heapq.heappush(bricks, [z1, y1, x1, z2, y2, x2])
    else:
        heapq.heappush(bricks, [z2, y2, x2, z1, y1, x1])
# All bricks should now be in the heap by lowest z value

def getBlocks(b):
    '''Take a brick and return the list of blocks that makes it'''
    block_list = []
    z1, y1, x1, z2, y2, x2 = b
    for z in range(z1, z2 + 1):
        if y1 < y2:
            small_y = y1
            big_y = y2
        else:
            small_y = y2
            big_y = y1
        for y in range(small_y, big_y + 1):
            if x1 < x2:
                small_x = x1
                big_x = x2
            else:
                small_x = x2
                big_x = x1
            for x in range(small_x, big_x + 1):
                block_list.append((z, y, x))
    return(block_list)

def downOne(bl):
    new_bl = []
    for b in bl:
        z, y, x = b
        new_bl.append((z-1, y, x))
    return(new_bl)

def settle(s_blocks, s_bricks, b):
    '''Move one brick down as far as it will go and record all block
    locations'''
    block_list = getBlocks(b)
    if DEBUG > 4:
        print(block_list)
    can_drop = True
    has_dropped = False
    while can_drop:
        test_list = downOne(block_list)
        for block in test_list:
            if block[0] < 1:
                can_drop = False
                break
            if block in s_blocks:
                can_drop = False
                break
        if can_drop:
            has_dropped = True
            block_list = test_list
            b[0] = b[0] - 1
            b[3] = b[3] - 1
    # we should be as far as this block can be dropped
    for block in block_list:
        s_blocks[block] += 1
    heapq.heappush(s_bricks, b)
    return(has_dropped)

settled_bricks = []
settled_blocks = Counter()
while len(bricks) > 0:
    brick = heapq.heappop(bricks)
    settle(settled_blocks, settled_bricks, brick)
# all the bricks should now be at their lowest possible positions

# check which bricks can be disintigrated
# we could remove bricks one at a time and see if any with a z one above
#  its high z would fall
from copy import deepcopy
def testRemove(sb, i, bl):
    '''Take the dict of settled blocks, a brick index and a z sorted brick
     list and see if this brick can be removed'''
    test_sb = deepcopy(sb)
    block_list = getBlocks(bl[i])
    for block in block_list:
        del(test_sb[block])
    bricks = deepcopy(bl)
    bricks.pop(i)
    removeable = True
    for brick in bricks:
        cur_sb = deepcopy(test_sb)
        block_list = getBlocks(brick)
        for block in block_list:
            del(cur_sb[block])
        blocks = getBlocks(brick)
        block_list = downOne(blocks)
        can_drop = True
        for block in block_list:
            if block[0] < 1:
                can_drop = False
                break
            if block in cur_sb:
                can_drop = False
                break
        if can_drop:
            return(False)
    return(removeable)
    
# make a plain, sorted list
sorted_bricks = []
while len(settled_bricks) > 0:
    brick = heapq.heappop(settled_bricks)
    sorted_bricks.append(brick)
# we have our sorted list
# test each brick
can_remove = 0
for i, test_brick in enumerate(sorted_bricks):
    if testRemove(settled_blocks, i, sorted_bricks):
        can_remove += 1
        print("Brick", test_brick, "can be removed")
    else:
        print("Brick", test_brick, "cannot be removed")

# It takes a long time to get here should optimize someday
print("Number of removable bricks is", can_remove)

'''Part2 - Find the number of bricks that fall for each removed and
sum them up'''
def countFalls(i, bl):
    '''Take a brick index and a z sorted brick list and return how many other
    bricks fall if this brick is removed'''
    bricks = deepcopy(bl)
    bricks.pop(i)
    new_sb = Counter()
    new_bl = []
    num_dropped = 0
    for brick in bricks:
        dropped = settle(new_sb, new_bl, brick)
        if dropped:
            num_dropped += 1
    return(num_dropped)

total_fallen = 0
for i, test_brick in enumerate(sorted_bricks):
    fallen = countFalls(i, sorted_bricks)
    print("Brick", test_brick, "caused", fallen, "falls")
    total_fallen += fallen
print("Total fallen bricks is", total_fallen)
