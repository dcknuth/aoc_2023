'''AoC Day02'''

#filename = "test02.txt"
filename = "input02.txt"

with open(filename) as f:
    ls = f.read().strip().split('\n')

# Part 1
max_list = {'red':12, 'green':13, 'blue':14}
id_total = 0

for l in ls:
    game, cur_sets = l.split(': ')
    cur_id = int(game[5:])
    valid = True
    for cur_set in cur_sets.split('; '):
        for cubes in cur_set.split(', '):
            cur_num, cur_color = cubes.split()
            cur_num = int(cur_num)
            if cur_num > max_list[cur_color]:
                valid = False
                continue
    if valid:
        id_total += cur_id

print("Sum of valid IDs is", id_total)

# Part 2
total = 0
for l in ls:
    min_list = {'red':0, 'green':0, 'blue':0}
    game, cur_sets = l.split(': ')
    cur_id = int(game[5:])
    valid = True
    for cur_set in cur_sets.split('; '):
        for cubes in cur_set.split(', '):
            cur_num, cur_color = cubes.split()
            cur_num = int(cur_num)
            if cur_num > min_list[cur_color]:
                min_list[cur_color] = cur_num
    total += min_list['red'] * min_list['green'] * min_list['blue']

print("Power of minimums is", total)
