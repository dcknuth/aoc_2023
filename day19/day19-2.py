'''Aoc Day19 Part1
what is the sum of all ratings of all accepted parts?'''
from collections import defaultdict

DEBUG = 5
#filename = 'input19.txt'
filename = 'test19-1.txt'

with open(filename) as f:
    ls = f.read().strip().split('\n')

funcs = defaultdict(list)
parts = dict()
vals = {'x':0, 'm':1, 'a':2, 's':3}

i = 0
while ls[i] != '':
    name, instructions = ls[i].split('{')
    instructions = instructions[:-1].split(',')
    for test in instructions:
        if '<' in test:
            trait, post = test.split('<')
            num, to_name = post.split(':')
            trait = vals[trait]
            num = int(num)
            funcs[name].append((trait, '<', num, to_name))
        elif '>' in test:
            trait, post = test.split('>')
            num, to_name = post.split(':')
            trait = vals[trait]
            num = int(num)
            funcs[name].append((trait, '>', num, to_name))
        else:
            funcs[name].append((None, 'run', None, test))
    i += 1

# then the parts
i += 1
while i < len(ls):
    x, m, a, s = ls[i][1:-1].split(',')
    _, x = x.split('=')
    x = int(x)
    _, m = m.split('=')
    m = int(m)
    _, a = a.split('=')
    a = int(a)
    _, s = s.split('=')
    s = int(s)
    parts[(x, m, a, s)] = 0
    i += 1

def runWF(p, funcs):
    '''Given a part and the workflows directory, run to a result'''
    workflow = 'in'
    while True:
        func_list = funcs[workflow]
        next = None
        for trait, op, num, to_name in func_list:
            if op == '<' and p[trait] < num:
                next = to_name
                break
            elif op == '>' and p[trait] > num:
                next = to_name
                break
            else:
                next = to_name
        if next == 'A':
            return(sum(p))
        if next == 'R':
            return(0)
        workflow = next


total = 0
for p in parts.keys():
    total += runWF(p, funcs)
print("Total is", total)


'''Part 2 - considering just workflows, how many acceptable combinations
are there?
The following is a start, but I ended up cheating and needed two solutions
to get a working answer and the Python runtime was about an hour on the one
that worked'''
min_val = 1
max_val = 4000
from copy import deepcopy

def sepTrait(trait, op, num, min_max):
    '''Given a single trait rule, return 'in' and 'out' range sets'''
    cur_min, cur_max = min_max[trait]
    if op == '<':
        # no values for cur branch
        if cur_min >= num:
            return([], min_max)
        # fewer or same values left
        if cur_max >= num:
            new_in = deepcopy(min_max)
            new_in[trait][1] = num - 1
            if cur_min < num and num <= cur_max:
                new_out = deepcopy(min_max)
                new_out[trait][0] = num
            elif num > cur_max:
                new_out = []
            return(new_in, new_out)
        else:
            print("Error: In < of sepTrait")
    if op == '>':
        # no values left for cur branch
        if cur_max <= num:
            return([], min_max)
        # fewer or same values left
        if cur_min <= num:
            new_in = deepcopy(min_max)
            new_in[trait][0] = num + 1
            if cur_min < num and num >= cur_max:
                new_out = deepcopy(min_max)
                new_out[trait][1] = num
            elif num < cur_max:
                new_out = []
            return(new_in, new_out)
        else:
            print("Error: In > of sepTrait")
    else:
        print("Error: In sepTrait")

def createNext(cur_wf, active_wfs, accepted, rejected):
    name, range_list = cur_wf
    test_list = funcs[name]
    for trait, op, num, to_name in test_list:
        in_list = []
        out_list = []
        if op == '<' or op == '>':
            for r in range_list:
                cur_in, cur_out = sepTrait(trait, op, num, r)
                if len(cur_in) > 0:
                    in_list.append(cur_in)
                if len(cur_out) > 0:
                    out_list.append(cur_out)
            if to_name == 'A':
                accepted.append(in_list)
            elif to_name == 'R':
                rejected.append(in_list)
            else:
                active_wfs.append([to_name, in_list])
            range_list = out_list
        else:
            # handle default case
            if to_name == 'A':
                accepted.append(range_list)
            elif to_name == 'R':
                rejected.append(range_list)
            else:
                active_wfs.append([to_name, range_list])

start_set = [[min_val, max_val], [min_val, max_val], [min_val, max_val],
             [min_val, max_val]]
active_wfs = [['in', [start_set]]]
accepted = []
rejected = []
while len(active_wfs) > 0:
    cur_wf = active_wfs.pop()
    new_wf_list = createNext(cur_wf, active_wfs, accepted, rejected)

print("Accepted looks like", accepted)
print("Rejected looks like", rejected)
