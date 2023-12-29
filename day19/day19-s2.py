'''This was another attempt to copy a solution and was able to run without
error, but took about an hour. It's from 4HbQ on the solution thread here:
https://www.reddit.com/r/adventofcode/comments/18ltr8m/2023_day_19_solutions/
Interestingly, I started and then gave up on a solution using lambdas due
to the difficulty of debugging them with VS Code. The length of the run
also explains the other solution's desire to use Numba'''
import re

filename = 'input19.txt'
flows, parts = open(filename).read().split('\n\n')

A_ = lambda: 1 + x+m+a+s
R_ = lambda: 1
S_ = 0

exec(flows.replace(':', ' and ').
           replace(',', '_() or ').
           replace('{', '_ = lambda: ').
           replace('}', '_()'))

exec(parts.replace(',', ';').
           replace('{', '').
           replace('}', ';S_+=in_()-1'))

print(S_)

splits = {c: [0, 4000] for c in 'xmas'}

for c,o,v in re.findall(r'(\w+)(<|>)(\d+)', flows):
    splits[c].append(int(v)-(o=='<'))

ranges = lambda x: [(a,a-b) for a,b in zip(x[1:], x)]
X,M,A,S = [ranges(sorted(splits[x])) for x in splits]

C = 0
for x,dx in X:
    for m,dm in M:
        for a,da in A:
            for s,ds in S:
                C += dx * dm * da * ds * bool(in_()-1)

print(C)
