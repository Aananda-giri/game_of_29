'''
# Space complexity : 1.6GB
cards: [c_trump, d_trump, h_trump, s_trump, None_trump]

possible nodes: 32C8 + 32C7 + 32C6 + 32C5 + 32C4 + 32C3 + 32C2 + 32C1 = 15, 033, 204
possible value for each node: 9 : <TrumpRevealed:C, D, H, S>, <Set_But_Not_Revealed: C, D, H, S>, Trump not revealed

'''
# ----------------------------
# Complexity
# ----------------------------

import random
import json
import pickle
import itertools
import sys
sys.path.append('/home/machina/bhoos/python/src/')
from utils import Card

def dump_pickle(data, filename='train_data.pkl'):
       if filename == None or filename == False:
           filename = 'train_data.pkl'
       # Open the file in append mode
       with open(filename, 'ab') as f:
              # Append the data to the file
              pickle.dump(data,f)

def load_pickle(filename='train_data.pkl'):
        #To load from pickle file
        data = []
        with open(filename, 'rb') as fr:
              try:
                     while True:
                            data.append(pickle.load(fr))
              except EOFError:
                     pass
        # print(data)
        return data

all_cards = [str(card) for card in Card.get_all_cards()]
len = 0
for i in range(1,9):
    cards = [{tuple(i):[100/33 for _ in range(9)]} for i in itertools.combinations(all_cards, i)]
    dump_pickle(cards, 'comb_data.pkl')
    del cards
    print('dump ', i)

# ----------------------------
# Simple Code
# ----------------------------
