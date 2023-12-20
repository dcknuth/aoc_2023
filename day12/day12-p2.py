'''Aoc Day12 Part2 - 5x both parts.
*** I cheated, looked up a solution and modified until I knew what it was
doing ***
We can no longer generate all the possibilities and check. So, we will need
to seperate out independant sections (at the dots) and add up'''

DEBUG = 5
filename = 'input12.txt'
#filename = 'test12-1.txt'

with open(filename) as f:
    ls = f.read().strip().split('\n')

long_records = []
for l in ls:
    s, contig = l.split()
    new_s = '?'.join([s for i in range(5)])
    new_contig = [int(n) for n in contig.split(',')] * 5
    long_records.append([new_s, new_contig])

total = 0
for s, contig_list in long_records:
    positions = {0: 1}
    for i, num_hashes in enumerate(contig_list):
        new_positions = {}
        for k, v in positions.items():
            hashes_remaining = sum(contig_list[i + 1:])
            remaining_space_slots = len(contig_list[i + 1:])
            chars_remaining = hashes_remaining + remaining_space_slots
            for n in range(k, len(s) - chars_remaining):
                if n + num_hashes - 1 < len(s) and \
                    '.' not in s[n:n + num_hashes]:
                    # there is some variablity left
                    if (i == len(contig_list) - 1 and \
                            '#' not in s[n + num_hashes:]) or \
                        (i < len(contig_list) - 1 and \
                            n + num_hashes < len(s) and \
                            s[n + num_hashes] != '#'):
                        if n + num_hashes + 1 in new_positions:
                            new_positions[n + num_hashes + 1] = \
                                new_positions[n + num_hashes + 1] + v
                        else:
                            new_positions[n + num_hashes + 1] = v
                if s[n] == '#':
                    break
        positions = new_positions
    total += sum(positions.values())

print("Total ways to complete is", total)