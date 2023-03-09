import sys
sys.path.append('/home/machina/bhoos/python/src/')

import random, math, time
from copy import deepcopy
from utils import Card
import numpy as np

all_cards = ['7H', '8H', 'QH', 'KH', 'TH', '1H', '9H', 'JH', '7D', '8D', 'QD', 'KD', 'TD', '1D', '9D', 'JD', '7C', '8C', 'QC', 'KC', 'TC', '1C', '9C', 'JC', '7S', '8S', 'QS', 'KS', 'TS', '1S', '9S', 'JS']

def get_neural_nets_play_card(cards):
    pass



def one_hot_encode(has_set_trump, probable_trumps, trump_revealed, cards_at_table, player_cards, opponent_cards, throwable_cards):
    # One Hot Encoding
    encoded = []
    for card in all_cards:
        vector = np.zeros(39)
        index = all_cards.index(card)
        vector[index] = 1
        #
        # [32] represent whether or not trump_set by player
        set_trump = has_set_trump
        vector[32] = set_trump
        #
        # [33] represent whether or not card could be trump
        probable_trump = card[-1] in probable_trumps
        vector[33] = probable_trump
        #
        # [34] feature represent whether or not trump is revealed
        # 1 is trump <player set trump> :: 0 maybe <player dont set trump>
        is_trump_revealed = trump_revealed
        # if is_trump_revealed:
        #     print(f'is_trump_revealed: {is_trump_revealed}')
        vector[34] = is_trump_revealed
        #
        # [35] card is at table
        at_table = card in cards_at_table
        vector[35] = at_table
        #
        # [36] card is held by player
        is_opponent_card = card in player_cards
        vector[36] = is_opponent_card
        #
        # [37] card is held by opponent
        is_opponent_card = card in opponent_cards
        vector[37] = is_opponent_card
        #
        # [38] represent whether or not it can be output
        throwable = True if card in throwable_cards else False
        vector[38] = throwable
        #
        encoded.append(vector)
    print(encoded)
    return encoded

def bhoos_compatible_play(body):#, start_time, n_simulations, DISCOUNT_FACTOR):
    player_cards = body['cards']
    # [32] represent whether or not trump_set by player
    has_set_trump = max(body['bidHistory'], key = lambda x:x[1])[0] == body["playerId"]
    # [33] represent whether or not card could be trump
    probable_trumps = ['C', 'D', 'H', 'S'] if not body['trumpSuit'] else [body['trumpSuit']]
    # card_could_be_trump = [card[-1] in probable_trumps for card in body['cards']]
    # [34] feature represent whether or not trump is revealed
    trump_revealed = True if body['trumpRevealed'] else False
    # [35] card is at table
    cards_at_table = [card for card in body['played']]
    #
    # [36] card is held by player
    player_cards = body['cards']
    #
    # [37] card is with opponent
    cards_already_played =  np.array([card[1] for card in body['handsHistory']]).reshape(-1, 1)
    opponent_cards = [card for card in all_cards if (card not in body['played']) and (card not in body['cards']) and (card not in cards_already_played)]
    # [38] represent whether or not it can be output
    did_reveal_trump_in_this_trick = body["trumpRevealed"] and body["trumpRevealed"]["playerId"] == body["playerId"] and body["trumpRevealed"]["hand"] - 1 == (len(body["handsHistory"]))
    throwable_cards = [str(card) for card in Card.throwableCards([Card(c[1], c[0]) for c in body["cards"] ], [Card(c[1], c[0]) for c in body["played"] ], did_reveal_trump_in_this_trick, body["trumpSuit"])]
    #
    encoded = one_hot_encode(has_set_trump, probable_trumps, trump_revealed, cards_at_table, player_cards, opponent_cards, throwable_cards)
    print(encoded)
    # best_card_to_throw = predict_neural_nets_play_card(encoded)
    # return all_cards[best_card_to_throw]
    # best_card_to_throw = get_play_card(body_converted, did_reveal_trump_in_this_trick, DISCOUNT_FACTOR, cards_not_played, n_simulations, body['average_reward_threshold'] if 'average_reward_threshold' in body.keys() else None)
    # response = {"card": str(best_card_to_throw)}

body = {'playerId': 'A2', 'playerIds': ['A1', 'B1', 'A2', 'B2'], 'timeRemaining': 1500, 'teams': [{'players': ['A1', 'A2'], 'bid': 17, 'won': 0}, {'players': ['B1', 'B2'], 'bid': 0, 'won': 4}], 'cards': ['JS', 'TS', 'KH', '9C', 'JD', '7D', '8D'], 'bidHistory': [['A1', 16], ['B1', 17], ['A1', 17], ['B1', 0], ['A2', 0], ['B2', 0]], 'played': ['9S', '1S', '8S'], 'handsHistory': [['A1', ['7H', '1H', '8H', 'JH'], 'B2'], ['A1', ['7H', '1H', '8H', 'JH'], 'B2']], 'trumpSuit': False, 'trumpRevealed': False}
bhoos_compatible_play(body)
from utils import load_pickle

# -----------------------
# Data pre-processing
# -----------------------
import sys
sys.path.append('/home/machina/bhoos/python/src')
from utils import load_pickle

pickled_data = load_pickle()
data = []
encoded = []

# back-propagate the reward <discount-factor: 0.3>
for d in pickled_data:
    for player_id in d.keys():
        if player_id == 'handsHistory':
            continue
        data_temp = d[player_id]['neuralHistory'].copy()
        reversed_data = reversed(d[player_id]['neuralHistory'])
        reward = 0
        for a1_data in reversed_data:
            data_temp[data_temp.index(a1_data)]['reward'] += 0.3 * reward
            reward = data_temp[n]['reward']
        data.extend(data_temp)
    
    # data.extend(d['B1']['neuralHistory'])
    # data.extend(d['A2']['neuralHistory'])
    # data.extend(d['B2']['neuralHistory'])

# Back-propagate reward


for d in data:
    encoded.append(one_hot_encode(d['has_set_trump'], d['probable_trumps'], d['trump_revealed'], d['cards_at_table'], d['cards_at_hand'], d['opponent_cards'], d['throwable_cards']))

encoded = np.array(encoded)
rewards = np.array([d['reward'] for d in data])

# train-test split
X_train = encoded
y_train = rewards

from sklearn.preprocessing import train_test_split
X_train, X_val, y_train, y_val = train_test_split(encoded, rewards, test_size=0.2, random_state=42)


print(encoded.shape)
'''
# -------------------------------------------------------
# Test: can find 0 and 1 at lealt in one encoded index
# -------------------------------------------------------
found1 = []
found0 = []
for i in range(39):
    for en in encoded:
        for e in en:
            # print(e[0])
            # if e.shape != (39, ):
            #     print(e[i])
            if e[i] == 1.0:
                found1.append(i)
            if e[i] == 1.0:
                found0.append(i)

len(list(set(found0)))  # 39
len(list(set(found1)))  # 39

# one_hot_encode(data[0]['A1']['neuralHistory'][0]['has_set_trump'], data[0]['A1']['neuralHistory'][0]['probable_trumps'], data[0]['A1']['neuralHistory'][0]['trump_revealed'], data[0]['A1']['neuralHistory'][0]['cards_at_table'], data[0]['A1']['neuralHistory'][0]['opponent_cards'], data[0]['A1']['neuralHistory'][0]['throwable_cards'])

# Test: pickle only storing first card of players cards
for d in data:
    if len(d['cards_at_hand']) != 1:
        print(d['cards_at_hand'])
        

# Test
for i in data:
    if len(i['cards_at_hand']) !=8: 
        print(i)


# ------------------------------------
# Test: count based on cards at hand
# ------------------------------------
count = {}
for d in data:
    len_cards_at_hand = len(d['cards_at_hand'])
    if len_cards_at_hand in count.keys():
        count[len_cards_at_hand] += 1
    else:
        count[len_cards_at_hand] = 1
'''
# ------------------------------------
# model
# ------------------------------------
import random
import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense

# Define a function to generate random training data
# def generate_training_data(num_samples):
#     # Generate random input data
#     X = np.random.rand(num_samples, 32*39)
#     # Generate random target data
#     y = np.random.randint(2, size=(num_samples, 1))
#     return X, y

'''
1. Generate training data from monte-carlo self plays.
2. Train a new model using that data.
3. Evaluate the new model against the current best model. If the new model is better, then save it to replace the best model.
4. Quit after a set number of iterations or if there hasn’t been any improvement for a while.
5. Generate new training data from games where the current model plays against itself, exploration_rate=0.1
# 6. Continue to train the current model with the newly generated data for a few epochs.
7. Go to step 3.

Todo:
- encode better
- better neural network
- early stopping
- discounted backword reward from end_game instead of eposodic
'''

# Define the neural network model
def create_model():
    model = Sequential()
    model.add(Dense(128, activation='elu', input_shape=(32*39,)))
    model.add(Dense(384, activation='elu'))
    model.add(Dense(384, activation='elu'))
    model.add(Dense(256, activation='elu'))
    model.add(Dense(128, activation='elu'))
    model.add(Dense(32, activation='tanh'))
    model.compile(optimizer='adam', loss='binary_crossentropy')
    return model

# Define the number of iterations to run
num_iterations = 100

# Initialize a variable to keep track of the best model
best_model = None
best_accuracy = 0

# Loop through the number of iterations
for i in range(num_iterations):
    print("Iteration:", i)
    # Generate training data
    # X_train, y_train = generate_training_data(1000)
    # Create a new model
    model = create_model()
    # Train the model
    model.fit(X_train, y_train, epochs=10, batch_size=32, verbose=0)
    # Evaluate the model on a validation set
    val_loss, val_acc = model.evaluate(X_val, y_val, verbose=0)
    
    print("Validation Accuracy:", val_acc)
    # Save the model if its accuracy is better than the best so far
    if val_acc > best_accuracy:
        best_model = model
        best_accuracy = val_acc
    # Quit if there hasn't been any improvement for a while
    if i > 20 and val_acc <= best_accuracy:
        break
    # Generate new training data by having the model play against itself
    new_X, new_y = generate_self_play_data(best_model)
    # Continue to train the model with the newly generated data for a few epochs
    best_model.fit(new_X, new_y, epochs=5, batch_size=32, verbose=0)

# Save the best model
best_model.save('best_model.h5')

'''
        # Data Format Stored in pickle file
        neuralHistory = [{
            neuralHistory['trump_revealed']
            neuralHistory['cards_at_table']
            neuralHistory[player.id]['opponent_cards']
            neuralHistory[player.id]['has_set_trump']
            neuralHistory[player.id]['probable_trumps']
            neuralHistory[player.id]['throwable_cards']
            neuralHistory[player.id]['thrown']
            neuralHistory[player.id]['throwable_cards']
            neuralHistory[player.id]['revealed_trump_in_this_trick']
            neuralHistory[trick_winner.id]['reward']
            neuralHistory[ordered_players[(trick_winner_index + 2)%4].id]['reward_partner_won']
        }, {...}]

        * example data
        {'A1': {'bid': 16, 'won': 0, 'initial_cards': ['JS', 'TC', 'QD', '7S'], 'final_cards': ['JS', 'TC', 'QD', '7S', 'KH', 'TH', '1S', 'JC'], 'set_trump': True, 'num_simulations': 10000, 'is_random_player': False, 'neuralHistory': [{'reward': 0, 'reward_partner_won': 0, 'trump_revealed': False, 'cards_at_table': [], 'opponent_cards': ['KD', '9S', '1H', 'KS', '8D', 'QS', 'QH', 'JD', '8C', '7H', '9D', 'TD', '7D', '7C', '1D', '9C', '9H', '1C', 'KC', 'TS', 'JH', '8S', 'QC', '8H'], 'has_set_trump': True, 'probable_trumps': ['S'], 'throwable_cards': ['JS', 'TC', 'QD', '7S', 'KH', 'TH', '1S', 'JC'], 'thrown': 'TC', 'revealed_trump_in_this_trick': False}]}, 'A2': {'bid': 0, 'won': 0, 'initial_cards': ['8C', '7H', '9D', 'TD'], 'final_cards': ['8C', '7H', '9D', 'TD', '7D', '7C', '1D', '9C'], 'set_trump': False, 'num_simulations': 10000, 'is_random_player': False, 'neuralHistory': [{'reward': 0, 'reward_partner_won': 0, 'trump_revealed': False, 'cards_at_table': ['TC', 'QH'], 'opponent_cards': ['JS', 'QD', '7S', 'KH', 'TH', '1S', 'JC', 'KD', '9S', '1H', 'KS', '8D', 'QS', 'JD', '9H', '1C', 'KC', 'TS', 'JH', '8S', 'QC', '8H'], 'has_set_trump': False, 'probable_trumps': ['C', 'D', 'H', 'S'], 'throwable_cards': ['8C', '7C', '9C'], 'thrown': '8C', 'revealed_trump_in_this_trick': False}]}, 'B1': {'bid': 0, 'won': 2, 'initial_cards': ['KD', '9S', '1H', 'KS'], 'final_cards': ['KD', '9S', '1H', 'KS', '8D', 'QS', 'QH', 'JD'], 'set_trump': False, 'num_simulations': 10000, 'is_random_player': False, 'neuralHistory': [{'reward': 0, 'reward_partner_won': 2, 'trump_revealed': False, 'cards_at_table': ['TC'], 'opponent_cards': ['JS', 'QD', '7S', 'KH', 'TH', '1S', 'JC', '8C', '7H', '9D', 'TD', '7D', '7C', '1D', '9C', '9H', '1C', 'KC', 'TS', 'JH', '8S', 'QC', '8H'], 'has_set_trump': False, 'probable_trumps': ['C', 'D', 'H', 'S'], 'throwable_cards': ['KD', '9S', '1H', 'KS', '8D', 'QS', 'QH', 'JD'], 'thrown': 'QH', 'revealed_trump_in_this_trick': False}]}, 'B2': {'bid': 0, 'won': 2, 'initial_cards': ['9H', '1C', 'KC', 'TS'], 'final_cards': ['9H', '1C', 'KC', 'TS', 'JH', '8S', 'QC', '8H'], 'set_trump': False, 'num_simulations': 10000, 'is_random_player': False, 'neuralHistory': [{'reward': 2, 'reward_partner_won': 0, 'trump_revealed': False, 'cards_at_table': ['TC', 'QH', '8C'], 'opponent_cards': ['JS', 'QD', '7S', 'KH', 'TH', '1S', 'JC', 'KD', '9S', '1H', 'KS', '8D', 'QS', 'JD', '7H', '9D', 'TD', '7D', '7C', '1D', '9C'], 'has_set_trump': False, 'probable_trumps': ['C', 'D', 'H', 'S'], 'throwable_cards': ['1C', 'KC', 'QC'], 'thrown': '1C', 'revealed_trump_in_this_trick': False}]}, 'handsHistory': [['B2', ['TC', 'QH', '8C', '1C'], 'B2']]}

        play_data_neural = {
        'A' : {
            player_cards: [<player-cards>],
            player_set_trump: True/False,

            
            probable_trumps: [['C', 'D', 'H', 'S']*8],
            trump_revealed: [True/False]*8,
            
            cards_at_table: [[<cards-at-table>]*8],
            card_is_with_opponent: [[<cards-with-opponent>]*8],
            cards_already_played: [[<cards-already-played>]*8],
            opponent_cards = [[<opponents-cards>] * 8],
            did_reveal_trump_in_this_trick = [True/False]*8,
            
            throwable_cards: [<card>] * 8,
            thrown: [<card>] * 8,
            reward: [<trick-reward>] * 8,
            },
        'B' : {...}
        }
        player_cards = body['cards']
        # [32] represent whether or not trump_set by player
        player_set_trump = max(body['bidHistory'], key = lambda x:x[1])[0] == body["playerId"]
        # [33] represent whether or not card could be trump
        probable_trumps = ['C', 'D', 'H', 'S'] if not body['trumpSuit'] else [body['trumpSuit']]
        # card_could_be_trump = [card[-1] in probable_trumps for card in body['cards']]
        # [34] feature represent whether or not trump is revealed
        trump_revealed = True if body['trumpRevealed'] else False
        # [35] card is at table
        cards_at_table = [card for card in body['played']]
        # [36] card is with opponent
        all_cards = ['7H', '8H', 'QH', 'KH', 'TH', '1H', '9H', 'JH', '7D', '8D', 'QD', 'KD', 'TD', '1D', '9D', 'JD', '7C', '8C', 'QC', 'KC', 'TC', '1C', '9C', 'JC', '7S', '8S', 'QS', 'KS', 'TS', '1S', '9S', 'JS']
        cards_already_played =  np.array([card[1] for card in body['handsHistory']]).reshape(-1, 1)
        opponent_cards = [card for card in all_cards if (card not in body['played']) and (card not in body['cards']) and (card not in cards_already_played)]
        # [37] represent whether or not it can be output
        did_reveal_trump_in_this_trick = body["trumpRevealed"] and body["trumpRevealed"]["playerId"] == body["playerId"] and body["trumpRevealed"]["hand"] - 1 == (len(body["handsHistory"]))
        throwable_cards = [str(card) for card in Card.throwableCards([Card(c[1], c[0]) for c in body["cards"] ], [Card(c[1], c[0]) for c in body["played"] ], did_reveal_trump_in_this_trick, body["trumpSuit"])]


'''