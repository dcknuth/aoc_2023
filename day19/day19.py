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

def accept(p):
    '''Tally the rating and return it'''
    return(sum(p))

def reject(p):
    return(0)

funcs['A'] = accept
funcs['R'] = reject

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
            funcs[name].append(lambda x: to_name if x[trait] < num else False)
        elif '>' in test:
            trait, post = test.split('>')
            num, to_name = post.split(':')
            trait = vals[trait]
            num = int(num)
            funcs[name].append(lambda x: to_name if x[trait] > num else False)
        else:
            funcs[name].append(lambda x: test)
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
    done = False
    while not done:
        func_list = funcs[workflow]
        next = None
        for f in func_list:
            n = f(p)
            if type(n) == int:
                return(n, None, None)
            if type(n) == str:
                return(-1, n, p)

total = 0
for p in parts.keys():
    total += runWF(p, funcs)


