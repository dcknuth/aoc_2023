'''Aoc Day07 Part1
Find the total card game winnings'''
from functools import total_ordering

DEBUG = 5
filename = 'input07.txt'
#filename = 'test07.txt'

with open(filename) as f:
    ls = f.read().strip().split('\n')

@total_ordering
class Card:
    '''Represents a single card with a kind and a value'''
    # Face sorting
    card_val = dict(zip(['2', '3', '4', '5', '6', '7', '8', '9',
                         'T', 'J', 'Q', 'K', 'A'], range(2, 15)))
    
    def __init__(self, kind):
        self.value = Card.card_val[kind]
        self.kind = kind
    
    def __eq__(self, other):
        return (self.value == other.value)
    def __lt__(self, other):
        return(self.value < other.value)
    
    def __str__(self):
        return(self.kind)

@total_ordering
class Hand:
    '''Represents a hand of five cards with the ability to be sorted,
    a bid value and a value for the hand type'''
    def __init__(self, hand_str, b):
        self.cards = []
        for c in hand_str:
            self.cards.append(Card(c))
        self.bid = b
        self.type = self.getType()
    
    def __str__(self):
        return(''.join([x.kind for x in self.cards]))
    
    def getType(self):
        # apply the puzzle rules to test first by the 7 types
        unique = set(list(str(self)))
        if len(unique) == 5: # high card
            return(0)
        if len(unique) == 4: # one pair
            return(1)
        if len(unique) == 1: # five of a kind
            return(6)
        matches = [str(self).count(x) for x in unique]
        matches.sort(reverse=True)
        if len(unique) == 3 and matches[0] == 2: # two pair
            return(2)
        if len(unique) == 3 and matches[0] == 3: # three of a kind
            return(3)
        if len(unique) == 2 and matches[0] == 3: # full house
            return(4)
        if len(unique) == 2 and matches[0] == 4: # four of a kind
            return(5)
        print("Error: in getType")

    def __eq__(self, other):
        # to be equal all cards would have to be the same and in the
        #  same order
        return(str(self) == str(other))
    def __lt__(self, other):
        if self.type != other.type:
            return(self.type < other.type)
        # need to test card by card in the original order
        for i in range(4):
            if self.cards[i] != other.cards[i]:
                return(self.cards[i] < other.cards[i])
        return(self.cards[4] < other.cards[4])


# We should be able to make a list of hands and sort them
hands = []
for l in ls:
    hand_str, bid = l.split()
    bid = int(bid)
    hands.append(Hand(hand_str, bid))
hands.sort()
total = 0
for i, hand in enumerate(hands):
    total += (i+1) * hand.bid
print("Total winnings are", total)


# Part2: new rules with jokers, but still find total winnings
@total_ordering
class Card:
    '''Represents a single card with a kind and a value'''
    # Face sorting
    card_val = dict(zip(['J', '2', '3', '4', '5', '6', '7', '8', '9',
                         'T', 'Q', 'K', 'A'], range(1, 14)))
    
    def __init__(self, kind):
        self.value = Card.card_val[kind]
        self.kind = kind
    
    def __eq__(self, other):
        return (self.value == other.value)
    def __lt__(self, other):
        return(self.value < other.value)
    
    def __str__(self):
        return(self.kind)

@total_ordering
class Hand:
    '''Represents a hand of five cards with the ability to be sorted,
    a bid value and a value for the hand type'''
    def __init__(self, hand_str, b):
        self.cards = []
        for c in hand_str:
            self.cards.append(Card(c))
        self.bid = b
        self.type = self.getType()
    
    def __str__(self):
        return(''.join([x.kind for x in self.cards]))
    
    def getType(self):
        # apply the puzzle rules to test first by the 7 types
        unique = set(list(str(self)))
        if len(unique) == 1: # five of a kind
            return(6)
        temp_type = 0
        if len(unique) == 5: # high card
            temp_type = 0
        elif len(unique) == 4: # one pair
            temp_type = 1
        else:
            matches = [str(self).count(x) for x in unique]
            matches.sort(reverse=True)
            if len(unique) == 3 and matches[0] == 2: # two pair
                temp_type = 2
            elif len(unique) == 3 and matches[0] == 3: # three of a kind
                temp_type = 3
            elif len(unique) == 2 and matches[0] == 3: # full house
                temp_type = 4
            elif len(unique) == 2 and matches[0] == 4: # four of a kind
                temp_type = 5
        j_num = ''.join(str(self)).count('J')
        if j_num == 0:
            return(temp_type)
        if (j_num == 1 and (temp_type == 0 or temp_type == 5)) or \
            (j_num == 4 and temp_type == 5):
            return(temp_type + 1)
        if (j_num == 1 and (temp_type == 1 or temp_type == 3)) or \
            (j_num == 2 and (temp_type == 1 or temp_type == 4)) or \
            (j_num == 3 and (temp_type == 4 or temp_type == 3)) or \
            (j_num == 1 and temp_type == 2):
            return(temp_type + 2)
        if (j_num == 2 and temp_type == 2):
            return(temp_type + 3)
        print("Error: in getType")

    def __eq__(self, other):
        # to be equal all cards would have to be the same and in the
        #  same order
        return(str(self) == str(other))
    def __lt__(self, other):
        if self.type != other.type:
            return(self.type < other.type)
        # need to test card by card in the original order
        for i in range(4):
            if self.cards[i] != other.cards[i]:
                return(self.cards[i] < other.cards[i])
        return(self.cards[4] < other.cards[4])


# after some redefining, we should again be able to make a list of hands
#  and sort them
hands = []
for l in ls:
    hand_str, bid = l.split()
    bid = int(bid)
    hands.append(Hand(hand_str, bid))
hands.sort()
total = 0
for i, hand in enumerate(hands):
    total += (i+1) * hand.bid
print("Total winnings are", total)
