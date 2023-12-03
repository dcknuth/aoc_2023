'''AoC Day03'''
import re
from collections import defaultdict

DEBUG = 4
filename = 'input03.txt'
#filename = 'test03.txt'

with open(filename) as f:
    ls = f.read().strip().split('\n')

# walk the matrix looking for anything that is not a number or a '.'
# for y, l in enumerate(ls):
#     for x, c in enumerate(l):
#         if c != '.' and not c.isdigit():
            # we have a symbol
            # now need to figure out how to pu

def symbolMatch(m, y, start_x, n):
    '''Given the matrix, the row number and the number, find if there are
    any symbols near the number and return the symbol.
    Numbers can appear multiple times in the line. Assuming they will only
    match one symbol'''
    start = m[y].find(n, start_x)
    end = start + len(n)
    if end < len(m[y]) - 1:
        end += 1
    if start > 0:
        start -= 1
    # look one row up
    if y > 0:
        search_here = m[y-1][start:end]
        sym = re.findall(r'[^\d\.]', search_here)
        if len(sym) == 1:
            return(sym[0])
        if len(sym) > 1:
            print("Violated the assumption that only one symbol is next to",
                  "a number")
    # look at this row
    search_here = m[y][start:end]
    sym = re.findall(r'[^\d\.]', search_here)
    if len(sym) == 1:
        return(sym[0])
    if len(sym) > 1:
        print("Violated the assumption that only one symbol is next to",
                "a number")
    # look down a row
    if y < len(ls) - 1:
        search_here = m[y+1][start:end]
        sym = re.findall(r'[^\d\.]', search_here)
        if len(sym) == 1:
            return(sym[0])
        if len(sym) > 1:
            print("Violated the assumption that only one symbol is next to",
                  "a number")
    # didn't find a symbol
    return(False)

sym_dict = defaultdict(list)
# it seems all the numbers are laid out horizontally and seem to just match
#  one symbol. Let's find each number and see if there is a symbol next to it
for y, l in enumerate(ls):
    line_pns = []
    numbers = re.findall(r'\d+', l)
    if DEBUG > 4:
        print("In line", l, "found these numbers", numbers)
    # since numbers can appear multiple times in a line, need to also
    #  pass a starting position for the current number
    current_pos = 0
    for num in numbers:
        sym = symbolMatch(ls, y, current_pos, num)
        if sym:
            sym_dict[sym].append(int(num))
            line_pns.append(':'.join([sym, num]))
        current_pos = l.find(num, current_pos) + (len(num) - 1)
    if DEBUG > 3:
        print(y, ','.join(line_pns))

# we should now have all the numbers and can add them up
total = 0
for num_list in sym_dict.values():
    total += sum(num_list)
print("Sum of all numbers near a symbol is", total)

# Part 2
# Putting the numbers in a list based on the symbol didn't help us, so
#  we will have to walk the list again and make a different dict
gear_dict = defaultdict(list)

def findGears(m, y, start_x, n):
    '''Given the matrix, the row number and the number, find if there are
    any '*' symbols near the number and return the y,x position in a list.
    Numbers can appear multiple times in the line. Assuming they will only
    match one symbol'''
    start = m[y].find(n, start_x)
    end = start + len(n)
    if end < len(m[y]) - 1:
        end += 1
    if start > 0:
        start -= 1
    # look one row up
    if y > 0:
        search_here = m[y-1][start:end]
        pos = search_here.find('*')
        if pos > -1:
            return([y-1,start+pos])
    # look at this row
    search_here = m[y][start:end]
    pos = search_here.find('*')
    if pos > -1:
        return([y,start+pos])
    # look down a row
    if y < len(ls) - 1:
        search_here = m[y+1][start:end]
        pos = search_here.find('*')
        if pos > -1:
            return([y+1,start+pos])
    # didn't find a symbol
    return(False)

for y, l in enumerate(ls):
    numbers = re.findall(r'\d+', l)
    if DEBUG > 4:
        print("In line", l, "found these numbers", numbers)
    # since numbers can appear multiple times in a line, need to also
    #  pass a starting position for the current number
    current_pos = 0
    for num in numbers:
        gear_yx = findGears(ls, y, current_pos, num)
        if gear_yx :
            gear_dict[','.join(map(str, gear_yx))].append(int(num))
        current_pos = l.find(num, current_pos) + (len(num) - 1)

# Now we should be able to do our sum
total = 0
for key in gear_dict.keys():
    if len(gear_dict[key]) == 2:
        total += gear_dict[key][0] * gear_dict[key][1]
print("The sum of the ratios is", total)
