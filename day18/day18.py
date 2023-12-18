'''Aoc Day18 Part1
how many cubic meters of lava can the lagoon hold?'''

DEBUG = 5
#filename = 'input18.txt'
filename = 'test18-1.txt'

with open(filename) as f:
    ls = f.read().strip().split('\n')

digging = {'U':(-1, 0), 'R':(0,1), 'D':(1,0), 'L':(-1,0)}
def addMeter(m, d):
    '''Given the current matrix, a direction to dig a meter and the current
    position, dig the next meter and adjust the matrix as needed. Return
    the new position'''
    pass

