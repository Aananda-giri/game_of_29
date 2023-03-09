
# ============================================
# Problem
# ============================================
'''- provided 52 cards, find all possible combinations of 4 cards
- order matter: first card and (combination of second third and fourth card )
- order does not matter:  of second third and fourth card 
'''
# ============================================
# Conclusion
# ============================================
- dont save calculate_winner data : memory + more time than calculation
# ============================================
# Method2: combinations + permutations
# ============================================

import random
import json
import pickle
import itertools
import sys
sys.path.append('/home/machina/bhoos/python/src/')
from utils import Card

all = [str(card) for card in Card.get_all_cards()]
combinations = [i for i in itertools.combinations(all, 4)]

def rotate(lst):
    if type(lst) ==list:
        return lst[1:] + [lst[0]]
    else:
        # print(f'not list{type(lst)}')
        # print(type(first_el))
        return lst[1:] + tuple([lst[0]])

rotate(('TS', '1S', '9S', 'JS'))
# rotate(['1','2'])
# progress_bar
def progress_bar(current, total):
    print((current/total)*100)

combn = []
total_iters = len(combinations)
for n, comb in enumerate(combinations):
    # comb = ['1','2','3']
    # rotate(len(comb)-1) times
    rotations = [comb]
    for i in range(len(comb)-1):
        rotations.append(rotate(rotations[-1]))
    combn.extend(r for r in rotations)
    if n%100 == 0:
        progress_bar(n, total_iters)

print(f"initial combination: {total_iters}, final permutation: {len(combn)}")
print(f'total permutations: {len([i for i in itertools.permutations(all,4)])}')
# initial combination: 35960, final permutation: 143840     # *4
# total permutations: 863040

'''
# ============================================
# calculate winner indexes and win values
# ============================================
possible_trumps = ['C', 'D', 'H', 'S', None]
combn_dict = {('7H', '8H', 'QH', 'KH'): [(3, 0), (3, 0), (3, 0), (3, 0), (3, 0)]
{<cards> : [<C is trump> (winner_card, score), <D is trump> (winner_card, score), <H is trump>(winner_card, score), <S is trump> (winner_card, score), <None is trump>(winner_card, score)]}
e.g. {('7H', '8H', 'QH', 'KH'): [(3, 0), (3, 0), (3, 0), (3, 0), (3, 0)], ('7H', '8D', 'QH', 'KH'): [(3, 0), (1, 0), (3, 0), (3, 0), (3, 0)], ('7H', '8D', 'JH', 'KH'): [(2, 3), (1, 3), (2, 3), (2, 3), (2, 3)]}

<pickle-size>: 8.2 mb
<combinations>: 143840

<read_time>: 
    dict: 1.954078674316406e-05
    code: 1.6396045684814452e-05


import random
import numpy as np
position = random.randint(0, 143840)
random_el = list(combn_dict.keys())[position]

def from_dict():
    start_time = time.time()
    value = combn_dict[random_el]
    
    stop_time = time.time()
    return (stop_time - start_time) * 100

# d_trump = value[1]
# d_trump_win = d_trump[1]
# c_trump_win_card = d_trump[0]
# c_trump_win_score = d_trump[1]

times = []

for i in range(10000):
    times.append(from_dict())

print(f"average_time: {np.average(times)}") # 1.954078674316406e-05

# <calculation time>
import sys
sys.path.append('/home/machina/bhoos/python/src/')
from utils import Card

def from_calcn():
    played = random.sample(Card.get_all_cards(), 4)
    possible_trumps = ['C', 'D', 'H', 'S', None]
    trump_suit = random.choice(possible_trumps)
    trump_revealed = True if trump_suit != None else False
    start_time = time.time()
    winner_index, scores = Card.calculateWinnerIndex(played, trump_suit=trump_suit, trump_revealed=trump_revealed, show_win_score=True)
    stop_time = time.time()
    return (stop_time - start_time) * 100


times = []
for i in range(10000):
    times.append(from_dict())

print(f"average_time: {np.average(times)}") # 1.6396045684814452e-05

'''

possible_trumps = ['C', 'D', 'H', 'S', None]
combn_dict = {}
for cmb in combn:
    played = [Card(c[1],c[0]) for c in cmb]    # ['7H', '8D', 'JH', 'KH']
    scores = [Card.calculateWinnerIndex(played, trump_suit, True if trump_suit != None else False, True) for trump_suit in possible_trumps]
    scores_card_win = []
    for score in scores:
        winner_card = cmb[score[0]]
        win_score = score[1]
        scores_card_win.append((winner_card, win_score))
    combn_dict[tuple(str(card)for card in played)] = scores_card_win

# ============================================================
# save winner indexes and win values for each possible card
# ============================================================
with open('node_scores.pkl', 'wb') as f:
    pickle.dump(combn_dict, f)

# load pickle
with open('node_scores.pkl', 'rb') as f:
    combn_dict2 = pickle.load(f)

# ----------------------------------------
# Method0: combinations + permutations
# ----------------------------------------
import random
import sys
sys.path.append('/home/machina/bhoos/python/src/')
from utils import Card

cards_at_table = []
cards_at_hand = random.sample(Card.get_all_cards(), 8)
cards_not_played = [card for card in Card.get_all_cards() if card not in cards_at_hand]

cards_at_hand = ['9D', 'TH', '7H', 'QS', '8H', '9S', 'JH', 'JC']
cards_not_played = ['QH', 'KH', '1H', '9H', '7D', '8D', 'QD', 'KD', 'TD', '1D', 'JD', '7C', '8C', 'QC', 'KC', 'TC', '1C', '9C', '7S', '8S', 'KS', 'TS', '1S', 'JS']

# Node is state of cards

# first throw
# player throws 1
# opponent throws n

# opponent throws n
# player throws 1
# opponent throws n

import random
import sys
sys.path.append('/home/machina/bhoos/python/src/')
from utils import Card
import itertools

all = [str(card) for card in Card.get_all_cards()]
permutations = [i for i in itertools.permutations(all, 4)]
to_remove = []

total_iters = len(permutations)
for n, perm in enumerate(permutations):
    second_through = perm[1:]
    perm_first = tuple(perm[0])
    perm_second_third = [i for i in itertools.permutations(second_through, 2)]
    _=[permutations.remove(i) for i in [perm_first + l for l in perm_second_third[1:]] if i in permutations]
    if n%100 == 0:
        progress_bar(n, total_iters)
    # to_remove.extend([perm_first + l for l in perm_second_third[1:]])


# ----------------------------------------
# get_winner and score: 
# ----------------------------------------
def get_winner(combination):
    winners_and_scores = []
    # trump is none
    winner, score = 'JS', 5    # JS is winning card , 5 is score
    winners_and_scores.append([winner, score])
    # 'C' is trump
    # 'D' is trump
    # 'H' is trump
    # 'S' is trump

    return {combination: winners_and_scores}

for c in combn:
    get_winner(c)




'''
# ----------------------------------------------------
# Problem:
# i have five numbers: ['1', '2', '3', '4', '5']
# i want permutations of length 3
# order of second and third number does not matter
# ----------------------------------------------------
# proof of concept:
permutations[0] = ('1', '2', '3')
second_third = ['2', '3']
perm_first = ['1']
perm_second_third = [['2', '3'] , ['3', '2']]
to_remove = []
to_remove.extend([perm_first + l for l in perm_second_third[1:]])

# ----------------------------------------
# Method1: permutations + combinations
# ----------------------------------------
# implementation:
numbers = ['1','2','3','4','5']
permutations = [i for i in itertools.permutations(numbers, 3)]
to_remove = []

for perm in permutations:
    second_through = perm[1:]
    perm_first = tuple(perm[0])
    perm_second_third = [i for i in itertools.permutations(second_through, 2)]
    [permutations.remove(i) for i in [perm_first + l for l in perm_second_third[1:]] if i in permutations]
    to_remove.extend([perm_first + l for l in perm_second_third[1:]])

# ----------------------------------------
# Method2: combinations + permutations
# ----------------------------------------
numbers = ['1','2','3','4','5']
combinations = [i for i in itertools.combinations(numbers, 3)]
to_remove = []

def rotate(lst):
    if type(lst) ==list:
        return lst[1:] + [lst[0]]
    else:
        print(f'not list{type(lst)}')
        # print(type(first_el))
        return lst[1:] + tuple([lst[0]])

# rotate(['1','2'])

combn = []
for comb in combinations:
    # comb = ['1','2','3']
    # rotate(len(comb)-1) times
    rotations = [comb]
    for i in range(len(comb)-1):
        rotations.append(rotate(rotations[-1]))
    combn.extend(r for r in rotations)

print(len(combn))
print([i for i in combn[0]])
'''

for perm in permutations_copy:
    second_through_last = perm[1:]
    perm_second_through = [pp for pp in itertools.permutations(second_through_last, 3)][1:]   # leave out first permutation
    [to_remove.append(tuple([perm[0]]) + p) for p in perm_second_through]

