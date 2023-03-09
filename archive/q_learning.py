'''import numpy as np
RANKS = ["J", "9", "A","T", "K", "Q", "8", "7"]
# trump_cards = ['TJ', 'T9', 'TA', 'TT', 'TK', 'TQ', 'T8', 'T7']      # ["T" + card for card in RANKS]
q_table = {}
for at_hand in RANKS:
    for at_table in RANKS:
        for trump in RANKS:
            q_table[at_hand, at_table, trump] = np.random.uniform(0, 10)

# lookup
throwables = []     # Throwable cards
to_throw = q_table(throwables, at_table, trump)
# code to compute conbination
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

def combination(n,r):
    return int(factorial(n) / (factorial(n-r) * factorial(r)))

import numpy as np
import pickle
q={}
for i in range(combination(16,8)):
    q[i] = np.random.uniform(0, 10)

pickle.dump(q, open("q_16c8.pkl", "wb"))   # 150.6 kb -> 12870 combinations

q={}
for i in range(combination(32,8)):
    q[i] = np.random.uniform(0, 10)

pickle.dump(q, open("q_32c8.pkl", "wb"))   # 140.3 mb -> 3365856 combinations
'''
"""
Q_table : 8 * 8 * 8 = 512 possible states
d0: possible cards @ hand
d1: possible cards @ table
d2: possible trump cards

how to pass possible opponent cards ?
d3: possible opponent cards
if we somehow did, we'd have : 8*8*8*8 possible combinations, so we may reduce them as:

7, 8, K, Q -> K
10, A -> A
9 -> 9
J -> J

we'd loose some information as: 'K' should have higher weight than '7'

"""

"""
Assume we have simple card game
cards = ['1', '2', '3', '4', '5', '6', '7', '8']
- np suite
- two players :: 4 cards each
- throw one at a time
- only throw rule :: throw larger to win
- player order: random
q_table:
state : card at table
action : card to throw  : throwable cards

"""
import random
import numpy as np
q_table={}
p1 = {}
p2 = {}
LEARNING_RATE = 0.1
DISCOUNT = 0.95
epsilon = 0.5
ITER = 1000
POINTS = [[],[]]
cards = [0, 1, 2, 3, 4, 5, 6, 7]
for at_table in cards:
    q_table[at_table] = [np.random.uniform(0, 10) for i in range(len(cards))]

# case for empty table
q_table[None] = [np.random.uniform(0, 10) for i in range(len(cards))]

class Player():
    def __init__(self, name, cards, random = False):
        self.name = name
        self.cards = cards
        self.points = 0
        self.random = random
        print(self.cards)
    def throw(self, at_table):
        if at_table == []:
            at_table = None
        else:
            at_table = at_table[-1]

        if self.random:
            to_throw = random.choice(self.cards) # throw card randomly
            self.cards.remove(to_throw) # remove card from hand
            return to_throw     # return card
        else:
            if random.random() < epsilon:
                to_throw = random.choice(self.cards)
                current_q = q_table[at_table][to_throw]
                max_future_q = max([ q_table[at_table][card] for card in self.cards ])
                self.cards.remove(to_throw) # remove card from hand
                # print(f"returning: {to_throw}, {at_table}, {current_q}, {max_future_q}")
                return to_throw, at_table, current_q, max_future_q  # To update new_q cause we don't know reward yet 
            else:
                to_throw = q_table[at_table].index(max([q_table[at_table][card] for card in self.cards])) # throw card with max q value
                # print("to_throw: ", to_throw)
                current_q = q_table[at_table][to_throw]
                max_future_q = max([ q_table[at_table][card] for card in self.cards ])
                self.cards.remove(to_throw) # remove card from hand
                # print(f"returning: {to_throw}, {at_table}, {current_q}, {max_future_q}")
                return to_throw, at_table, current_q, max_future_q  # To update new_q cause we don't know reward yet 

        
for i in range(ITER):
    random.shuffle(cards)
    p1 = Player('p1', cards[:4].copy())
    p2 = Player('p2', cards[4:].copy(), True)

    while p1.cards !=[] and p2.cards != []:
        players = [p2, p1]
        random.shuffle(players)  # random player order
        table = []       # clear table
        
        if players[0].random:
            # print(f"player0: {players[1]}")
            (to_throw1, at_table1, current_q1, max_future_q1) = players[1].throw(table)
            table.append(to_throw1)   # let them throw cards
            
            to_throw2 = players[0].throw(table)
            table.append(to_throw2)
        else:
            # print(f"player0: {players[0]}")
            (to_throw1, at_table1, current_q1, max_future_q1) = players[0].throw(table)
            table.append(to_throw1)   # let them throw cards

            to_throw2 = players[1].throw(table)
            table.append(to_throw2)
        # (to_throw2, at_table2, current_q2, max_future_q2) = players[1].throw(table)
        # table.append(to_throw2)   # let them throw cards

        
        reward2 = -1
        reward1 = -1
        # declare winner
        if table[0] > table[1]:
            players[0].points += 1
            reward1 = 1
        else:
            # p2 won
            players[1].points += 1
            
            reward2 = 1
        
        
        # updating q_value
        new_q1 = (1 - LEARNING_RATE) * current_q1 + LEARNING_RATE * (reward1 + DISCOUNT * max_future_q1)	# formula for updating q-value
        q_table[at_table1][to_throw1] = new_q1 # update q-table

        # new_q2 = (1 - LEARNING_RATE) * current_q2 + LEARNING_RATE * (reward2 + DISCOUNT * max_future_q2)	# formula for updating q-value
        # q_table[at_table2][to_throw2] = new_q2 # update q-table

    print(p1.points, p2.points)
    POINTS[0].append(p1.points)
    POINTS[1].append(p2.points)

# print(q_table)
print(POINTS[0], '\n\n')
print(POINTS[1], '\n\n')