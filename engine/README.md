# Running Code
source /home/nathan/Documents/machine_env/bin/activate
### test is commit label and playing 50 games
python3 Play.py UCB2_vs_UCB2_early_stop 500 train_data.pkl > test.out    : 50.8%

python3 Play.py v5_vs_v5_negative_reward__times.7 500 train_data.pkl > test.out    : 50.8%
python3 Play.py v5_vs_v5_negative_reward__times.7 500 train_data.pkl > test.out    : 50.8%


python3 Play.py threshold_.001v.00001_10000iters 300 train_data.pkl >> test.out    : 48.667
python3 Play.py threshold_.0001v.00001_10000iters 300 train_data.pkl >> test.out    : 49%
python3 Play.py threshold_.001v.0001 1000 > out.out train_data.pkl >> test3.out
python3 Play.py ucb2_against_self 5000 > out.out 


- random players: all players other except player

# Neural Networks
 ## Generate Data for neural nets:
    python3 Play.py train_data_test 1000 train_data.pkl > test.out

## Todo:
    1. Generate training data from monte-carlo self plays.
    2. Train a new model using that data.
    3. Evaluate the new model against the current best model. If the new model is better, then save it to replace the best model.
    4. Quit after a set number of iterations or if there hasn’t been any improvement for a while.
    5. Generate new training data from games where the current model plays against itself, exploration_rate=0.1
    # 6. Continue to train the current model with the newly generated data for a few epochs.
    7. Go to step 3.

# info:
    - first bidder is selected at random and have to bid at least 16
    - bid_winner sets the trump
    - term 'lte' -> less than or equals to 
    - term 'gte' -> greater than or equals to 
    - terms: "played" and "cards_at_table" are used synonymously
    - terms: "trick", "hand" are used synonymously
    - term: "round" is collection of 8 tricks/hands
    - players = ["A1", "B1", "A2", "B2"]
    - teams = ["A", "B"]      # first character of playerId
    - bid_value = -1 initially, 0 if pass, 28 if bid 28
    # bids are initially None
    # bids are zero if player passes
    # play function has variable: BID_WINNER -> Player(), BID_VALUE -> int {bid value of bid winner}
    # GamePlay class has variable: bid_value -> int {bid value of player}

# rules <gamePlay>:
    - 4 cards are dealt to each player
    - initial bidder must bid at least 16 initially and may pass later
    - bid diffender must bid equal to challenger
    - bid challenger must bid 1 more than defender
    - rest of 4 cards are dealt to each player
    - trump suit is set by the bid winner

    - each player plays one card starting from the bid winner
    - anticlockwise order
    - highest card wins the trick
    - trump suit is higher than all other suits

    - points of cards: {'J':3, '9':2, 'T':1, 'A':1, 'others':0} # where T is 10
    - order of cards: J, 9, T, A, K, Q, 8, 7

    # Reveal Trump
    - player can reveal trump if s/he cant follow the suit
        - If player revealed trump in current trick:
        - player must throw winning trump <if s/he has winning trump> or any trump card if s/he has trump card
    - or can throw any card of other suit
    
    # Scoring
    - sum of points obtained by tyeam > bid:
        - team wony the game
        - games_won += 1
        - win 6 games and win the match
    - sum of points obtained by team < bid:
        - team lost the game
        - games_won -= 1
        - lose 6 games and lose the match


# Todo?
* DQN?
    - 

* 5 tree:
    - expensive : requires more time and iterations
    - may not preserve order normal game proceeds

    - simplicity: easier to understand
    - debug: current implementation may be wrong

# Tried:
  * bid nural network
    - low accuracy<overfitting?>: 0.6%
    - Encode better?


## Record for bidding:
### dummy data
cards_before_bid = ['1S','9D','KH','KS']  # 4 cards
scores_obtained = [19, 11]   # 19 when player set trump and 11 when players team doesnot set trump


### pseudocode
random_cards = get_4_random_cards()
score1 = Play(random_cards, set_trump = True)
score2 = Play(random_cards, set_trump = False)

## Actual Data
cards_before_bid = [[], [], ...]
set_trump = [True, False, False, ...]
scores = [15, 13, ...]

### Questions
* if friend won the bid, vast scores difference than if opponent won, should we store if friend won or not?
  - In the match, there is no way of telling if friend will win the bid, so we have no use of that data.

## Record for playing
won_bid = True / False
cards_before_play = ['1S','9D','KH','KS', '2S','TD','1H','1S']  # 8 cards
HandsHistory = [[]]
scores_obtained = 21


### train data
--------------------------------- train_data --------------------
{'A1': {'bid': 0, 'won': 14, 'initial_cards': ['JH', '8D', 'QC', '7D'], 'final_cards': ['JH', '8D', 'QC', '7D', 'TC', 'QD', '1H', '1D'], 'set_trump': True, 'num_simulations': 1000, 'is_random_player': False}, 'A2': {'bid': 0, 'won': 14, 'initial_cards': ['QS', '9C', 'JD', '7S'], 'final_cards': ['QS', '9C', 'JD', '7S', 'JC', '9H', '9D', 'TD'], 'set_trump': False, 'num_simulations': 1000, 'is_random_player': False}, 'B1': {'bid': 0, 'won': 14, 'initial_cards': ['8H', '9S', '1C', 'JS'], 'final_cards': ['8H', '9S', '1C', 'JS', 'KD', '7H', '7C', 'QH'], 'set_trump': False, 'num_simulations': 1000, 'is_random_player': True}, 'B2': {'bid': 0, 'won': 14, 'initial_cards': ['KC', '1S', 'KS', 'KH'], 'final_cards': ['KC', '1S', 'KS', 'KH', '8S', 'TH', '8C', 'TS'], 'set_trump': False, 'num_simulations': 1000, 'is_random_player': True}, 'handsHistory': [['A1', ['JH', 'QH', '9H', 'TH'], 'A1'], ['B2', ['7D', 'KD', '9D', 'TS'], 'A1'], ['A2', ['8C', 'TC', '1C', '9C'], 'B2'], ['B1', ['QS', 'KS', '8D', '9S'], 'A2'], ['B1', ['JS', '7S', '8S', '1D'], 'B1'], ['A2', ['7C', 'JC', 'KC', 'QC'], 'B1'], ['A2', ['TD', 'KH', 'QD', '8H'], 'A2'], ['B2', ['JD', '1S', '1H', '7H'], 'A2']]}



### handsHistory : [[<p0:first_thrower>, [c0, c1, c2, c3], <p1: winner>]
 
 [[<Api.Player object at 0x7f9c23731750>, [<utils.Card object at 0x7f9c22abbc10>, <utils.Card object at 0x7f9c22aba4d0>, <utils.Card object at 0x7f9c22abb790>, <utils.Card object at 0x7f9c22aba710>], <Api.Player object at 0x7f9c23731750>], [<Api.Player object at 0x7f9c23731b50>, [<utils.Card object at 0x7f9c22abb650>, <utils.Card object at 0x7f9c22abab10>, <utils.Card object at 0x7f9c22abbb10>, <utils.Card object at 0x7f9c22abad50>], <Api.Player object at 0x7f9c23731750>], [<Api.Player object at 0x7f9c23731750>, [<utils.Card object at 0x7f9c22abb190>, <utils.Card object at 0x7f9c22a8cf50>, <utils.Card object at 0x7f9c22abb610>, <utils.Card object at 0x7f9c22a8ce50>], <Api.Player object at 0x7f9c23731b50>], [<Api.Player object at 0x7f9c23731750>, [<utils.Card object at 0x7f9c22abbad0>, <utils.Card object at 0x7f9c22aba410>, <utils.Card object at 0x7f9c22abaa50>, <utils.Card object at 0x7f9c22aba590>], <Api.Player object at 0x7f9c23731750>], [<Api.Player object at 0x7f9c23732650>, [<utils.Card object at 0x7f9c22bed4d0>, <utils.Card object at 0x7f9c22aba0d0>, <utils.Card object at 0x7f9c22ab9910>, <utils.Card object at 0x7f9c22aba290>], <Api.Player object at 0x7f9c23731750>], [<Api.Player object at 0x7f9c23732650>, [<utils.Card object at 0x7f9c22aba1d0>, <utils.Card object at 0x7f9c22abaa10>, <utils.Card object at 0x7f9c22ab9f90>, <utils.Card object at 0x7f9c22abb8d0>], <Api.Player object at 0x7f9c23732650>], [<Api.Player object at 0x7f9c23731750>, [<utils.Card object at 0x7f9c22a8cfd0>, <utils.Card object at 0x7f9c22ac3f90>, <utils.Card object at 0x7f9c22ab9a10>, <utils.Card object at 0x7f9c22ac3a10>], <Api.Player object at 0x7f9c23732650>], [<Api.Player object at 0x7f9c237322d0>, [<utils.Card object at 0x7f9c22ac2b10>, <utils.Card object at 0x7f9c22abae10>, <utils.Card object at 0x7f9c22ac3f50>, <utils.Card object at 0x7f9c22aba350>], <Api.Player object at 0x7f9c23731750>]]

### teams
 {'A': {'won': 17, 'bid': 16, 'round_points': 1, 'players': [<Api.Player object at 0x7f9c23731750>, <Api.Player object at 0x7f9c23731b50>]}, 'B': {'won': 11, 'bid': -1, 'round_points': 0, 'players': [<Api.Player object at 0x7f9c237322d0>, <Api.Player object at 0x7f9c23732650>]}}

### BID_RESULTS
 {'bid_winner': <Api.Player object at 0x7fe0ebf31e90>, 'bid_value': 17, 'bid_history': [['A1', 16], ['B1', 0], ['A2', 0], ['B2', 17], ['A1', 0]], 'initial_cards': {'A1': ['JS', '8D', '9H', 'TD'], 'B1': ['KD', 'TH', '7H', '9S'], 'A2': ['8C', 'TS', 'QH', 'JC'], 'B2': ['KS', '1H', '8S', '9D']}}

### bidHistory
 [['A1', 16], ['B1', 0], ['A2', 0], ['B2', 0]] 

x_train.append(random_cards)
y_train.append([score1, score2])
- store cards, scores, player_set_Trump <bool> at file: bid_data.pickle to train for bidding
 - correlation between the cards and the score
 - time distribution
 - score board
 - match variables
 - seperate player and dealer
 - random player

 

 * if we revealed the trump in this round and the winning card is trump, there are two cases
        # 1. If the opponent is winning the hand, then you must throw the winning card of the trump suit against your opponent's card.
        # 2. If your partner is winning the hand, then you could throw any card of trump suit since your team is only winning the hand.

# done
       - Engine Score Board
       - nullify game if: no trump revealed, 



- stats is saved at scores.csv
- cards, scores, set Trump are scored at file: bid_data.pickle to train for bidding

# Rules:
 * don't reveal trump is friend is winning



# To append to a pickle file
import pickle
def save_pickle(filename='train_data.pkl', data):
       # Open the file in append mode
       with open(filename, 'ab') as f:
              # Append the data to the file
              pickle.dump(data,f)

def read_pickle(filename):
       #To load from pickle file
       data = []
       with open(filename, 'rb') as fr:
              try:
                     while True:
                            data.append(pickle.load(fr))
              except EOFError:
                     pass
       print(data)

save('test.pkl', {1:2})
read_pickle('test.pkl')
save('test.pkl', {3:4})
read_pickle('test.pkl')

## Missing in Bhoos implementation
- set Joker as trump
- Marrige rule
- 