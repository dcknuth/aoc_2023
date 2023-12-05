'''Aoc Day05 Part1
Find the lowest location number'''

DEBUG = 3
filename = 'input05.txt'
#filename = 'test05.txt'

with open(filename) as f:
    ls = f.read().strip().split('\n')

def convert(item, map_list):
    '''Given the item to convert to the next step and the map list needed to
    do so, return the next number'''
    for map in map_list:
        dest, source, length = map
        if item >= source and item <= source + length:
            # find index in source
            i = item - source
            # find value of same index in dest and return
            return(dest + i)
    # otherwise return the same value
    return(item)

# process our input to get a seed number list and a list of lists of maps
seeds = [int(x) for x in ls[0][7:].split()]
map_lists = []
line_num = 3
while line_num < len(ls):
    cur_maps = []
    while line_num < len(ls) and ls[line_num] != '':
        if ls[line_num][0].isdigit():
            cur_maps.append([int(x) for x in ls[line_num].split()])
        line_num += 1
    map_lists.append(cur_maps)
    line_num += 1

# copy our seeds list and update through all the stages
results = seeds.copy()
for map_list in map_lists:
    if DEBUG > 4:
        print("input for map step was", results)
    new_results = []
    for cur in results:
        new_results.append(convert(cur, map_list))
    results = new_results
    if DEBUG > 4:
        print("output for map step was", results)

results.sort()
print("Lowest final value is", results[0])


# Part 2 - the seeds: line is range start and length pairs
# let's convert from a start and length to a start and end
i = 0
seed_ranges = []
while i < len(seeds):
    pair = [seeds[i], seeds[i] + (seeds[i+1] - 1)]
    i += 2
    seed_ranges.append(pair)

def findOverlap(s1, e1, s2, e2):
    overlap = []
    non_overlap = []
    ol_start = max(s1, s2)
    ol_end = min(e1, e2)
    # is there overlap
    if ol_start <= ol_end:
        overlap = [ol_start, ol_end]
        # any non-overlapping?
        if s1 < ol_start:
            non_overlap.append([s1, ol_start-1])
        if e1 > ol_end:
            non_overlap.append([ol_end + 1, e1])
    return(overlap, non_overlap)

def convert2(input_range, map_list):
    '''Given an input_range and the map list for the current step, return a
    new list of ranges'''
    # A single range may become more than one range after processing
    in_range_list = [input_range.copy()]
    out_range_list = []
    while len(in_range_list) > 0:
        in_s, in_e = in_range_list.pop()
        found = False
        for map in map_list:
            dest, source, l = map
            ol, non_ol = findOverlap(in_s, in_e, source, source + (l - 1))
            if len(ol) > 0:
                found = True
                out_start = dest + (ol[0] - source)
                out_end = out_start + (ol[1] - ol[0])
                out_range_list.append([out_start, out_end])
                if len(non_ol) > 0:
                    in_range_list.extend(non_ol)
        if not found:
            out_range_list.append([in_s, in_e])
    return(out_range_list)

# run through the stages again
for map_list in map_lists:
    new_seed_ranges = []
    for cur in seed_ranges:
        new_seed_ranges.extend(convert2(cur, map_list))
    seed_ranges = new_seed_ranges
    if DEBUG > 3:
        print("output for map step was", seed_ranges)

seed_ranges.sort()
print("Lowest final value is", seed_ranges[0][0])
