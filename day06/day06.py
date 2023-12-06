'''Aoc Day06 Part1
Find the lowest location number'''

DEBUG = 4
filename = 'input06.txt'
#filename = 'test06.txt'

with open(filename) as f:
    ls = f.read().strip().split('\n')

def findNumWins(time, record):
    '''Given a race duration and record, find the number of ways to win'''
    ways_to_win = 0
    for hold_t in range(1, time):
        if hold_t * (time - hold_t) > record:
            ways_to_win += 1
    return(ways_to_win)

_, races = ls[0].split(':')
races = [int(x) for x in races.strip().split()]
_, records = ls[1].split(':')
records = [int(x) for x in records.strip().split()]

total_ways_to_win = 1
for t, r in zip(races, records):
    total_ways_to_win *= findNumWins(t, r)
print("Total ways to win are", total_ways_to_win)

# Part 2 - one race, bigger numbers
from sympy import symbols, solve
import math
race_time = int(''.join(map(str, races)))
record = int(''.join(map(str, records)))
s = symbols('s')
inequality = s**2 - (race_time * s) + record < 0
hold_time = solve(inequality, s)
if DEBUG > 4:
    print(hold_time)
min_time = math.ceil(20464895 - 5*(8148220492397**0.5))
max_time = math.floor(5 * (8148220492397**0.5) + 20464895)
if DEBUG > 4:
    print("my_min_time", min_time, "min_result",
          min_time * (race_time - min_time), "max_result",
          max_time * (race_time - max_time), "record", record)
print("Ways to min in part 2 is", (max_time - min_time) + 1)
