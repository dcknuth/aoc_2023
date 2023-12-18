'''Aoc Day12 Part1
count up valid spring arrangements'''
import re
from itertools import product

DEBUG = 3
#filename = 'input12.txt'
filename = 'test12-1.txt'

with open(filename) as f:
    ls = f.read().strip().split('\n')

records = []
for l in ls:
    group, num_contig = l.split()
    num_contig = list(map(int, [n for n in num_contig.split(',')]))
    records.append([group, group.strip('.'), num_contig])

def genPossible(c_list, l):
    '''Generate all of the possible configurations of the contigious list
    given the total length needed'''
    hash_length = sum(c_list)
    dots_needed = l - hash_length
    d_frontback = dots_needed - (len(c_list) - 1)
    d_between = dots_needed - (len(c_list) - 2)
    sections = []
    dot_options_fb = []
    d_opts_between = []
    for x in range(d_frontback + 1):
        dot_options_fb.append('.' * x)
    for x in range(1, d_between + 1):
        d_opts_between.append('.' * x)
    # make start, all the hashes and seperators and the end
    sections.append(dot_options_fb)
    for c in c_list:
        sections.append(['#' * c])
        sections.append(d_opts_between)
    sections.pop() # get rid of the extra between
    sections.append(dot_options_fb)
    # now we should be ready be enumerate possibilities
    possible = []
    for x in product(*sections):
        s = ''.join(x)
        if DEBUG > 4:
            print(s)
        if len(s) == l:
            possible.append(s)
    return(possible)

def numMatches(s, l):
    '''Given a string and a possible match list, find the number of matches
    and return it'''
    # change string to a regex
    regex_str = s.replace('.', r'\.')
    if DEBUG > 2:
        print(f"Reg string for {s} is {regex_str}")
    regex_str = regex_str.replace('?', '.')
    if DEBUG > 2:
        print(f"Without ? for {s} is {regex_str}")
    pattern = re.compile(regex_str)
    count = 0
    for x in l:
        if pattern.match(x):
            count += 1
    return(count)

total = 0
for r in records:
    candidates = genPossible(r[2], len(r[1]))
    if DEBUG > 4:
        print(candidates)
    if DEBUG > 3:
        print("For", r[1], len(candidates), "are possible")
        print(candidates)
    n = numMatches(r[1], candidates)
    if DEBUG > 2:
        print("For", r[1], "there are", n, "matches")
    total += n

print("\n\nTotal possible configs for part 1 is", total)


'''Part 2 - 5x both parts.
We can no longer generate all the possibilities and check. So, we will need
to seperate out independant sections (the parts with at least 2 dots or
perfect matches could break these up) and then use our old solution if
small enough or use the combinations with repetition formula if not'''
def partStr(s):
    '''Given a string, break the string up at each dot and return a new list
    of strings'''
    str_list = []
    seperated = s.split('.')
    for cur_s in seperated:
        if len(cur_s) != 0:
            str_list.append(cur_s)
    return(str_list)

long_records = []
for c in records:
    new_s = '?'.join([c[0] for i in range(5)])
    new_contig = []
    for i in range(5):
        new_contig.extend(c[2].copy())
    long_records.append([partStr(new_s), new_contig])
total = 0

import math
def C(n, k):
    '''Compute the binomial'''
    bc = math.factorial(n) / (math.factorial(k) * math.factorial(n-k))
    return(round(bc))

def computeOptions(s, groups):
    '''Given the total length and the groups, figure out the vaiable
    sections and use the frmula to compute avalible options'''
    # number of hashes and dots needed at the minimum
    manditory = sum(groups) + (len(groups) - 1)
    flexible = len(s) - manditory
    slots_for_dots = len(groups) + 1
    options = C(flexible + (slots_for_dots -1), slots_for_dots - 1)
    return(options)

print("ops", computeOptions('?#?#?#?#?#?#?#?', [1,3,1,6]))

def solveRecord(r):
    '''Solve a base case and remove if possible or split and call again.
    Return the final result after recursion'''
    if len(r) == 1:
        computeOptions(total, fixed)
    for s in r[0]:
        pass



# where n is the number of free dots to place and r is the number of possible
#  areas they can be put we can use combinations with repetition and
#  binomial coefficient:
# (n+(r-1))! / (r! * ((n+(r-1))-r)!)
# for areas that we can get to all question marks
# n = section length - number of known parts needed
#  (sum(hash lengths) + (num hash sections - 1)
# r = num hash sections + 1


print("Total possible configs for part 2 is", total)
