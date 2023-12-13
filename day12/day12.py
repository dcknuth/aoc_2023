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
    regex_str = s.replace('.', '\.')
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


# Part 2 - 5x both parts
long_records = []
for c in records:
    new_s = '?'.join([c[0] for i in range(5)])
    new_contig = []
    for i in range(5):
        new_contig.extend(c[2].copy())
    long_records.append([new_s, new_s.strip('.'), new_contig])
total = 0

for r in long_records:
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

print("Total possible configs for part 2 is", total)
