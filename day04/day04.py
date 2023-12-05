'''AoC Day04 Part 1
Sum the points of each card'''

filename = 'input04.txt'
#filename = 'test04.txt'

with open(filename) as f:
    ls = f.read().strip().split('\n')

total = 0
for l in ls:
    card, numbers = list(map(str.strip, l.split(': ')))
    _, card_id = card.split()
    winning, my_nums = list(map(str.strip, numbers.split(' | ')))
    winning = winning.split()
    my_nums = my_nums.split()
    # find matches
    matches = set(winning) & set(my_nums)
    if len(matches) > 0:
        total += 2**(len(matches)-1)

print("Part1 point total is", total)


# Part2 winning copies of cards
from collections import Counter
cards = Counter()
for l in ls:
    card, numbers = list(map(str.strip, l.split(': ')))
    _, card_id = card.split()
    winning, my_nums = list(map(str.strip, numbers.split(' | ')))
    winning = winning.split()
    my_nums = my_nums.split()
    # find matches
    matches = set(winning) & set(my_nums)
    card_id = int(card_id)
    cards[card_id] += 1
    for x in range(card_id + 1, card_id + len(matches) + 1):
        cards[x] += cards[card_id]

# Now total up the cards
total = sum(cards.values())
print("Part2 point total is", total)
