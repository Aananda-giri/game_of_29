def progress_bar(current, total):
    """
    This function prints a progress bar.
    """
    percent = current / total
    arrow = '-' * int(round(percent * 20) - 1) + '>'
    spaces = ' ' * (20 - len(arrow))
    print('Progress: [{0}] {1}%'.format(arrow + spaces, int(round(percent * 100))), end="\r")

def get_suit(card):
    """
    This function returns the suit of the given card.
    """

    return card[1]


def get_suit_cards(cards, card_suit):
    """
    This function returns the list of cards of the given suit from the initial list of cards.
    """
    return [card for card in cards if get_suit(card) == card_suit]


def index(sequence, predicate):
    """
    This function returns the index of the first element in the sequence which satisfies the predicate, otherwise -1
    Just like javascript
    """
    return next((i for i, e in enumerate(sequence) if predicate(e)), -1)


def find(sequence, predicate):
    """
    This function returns the first element in the sequence which satisfies the given predicate, None otherwise
    Just like Javascript
    """
    return next((e for i, e in enumerate(sequence) if predicate(e)), None)


def get_partner_idx(my_idx):
    return (my_idx + 2) % 4


def get_rank(card):
    return card[0]


CARDS_DICT = {
    "J": {"points": 3, "order": 8},
    "9": {"points": 2, "order": 7},
    "1": {"points": 1, "order": 6},
    "T": {"points": 1, "order": 5},
    "K": {"points": 0, "order": 4},
    "Q": {"points": 0, "order": 3},
    "8": {"points": 0, "order": 2},
    "7": {"points": 0, "order": 1},
}


def get_card_info(card):
    return CARDS_DICT[get_rank(card)]


def is_high(highest_card, compare_card, trump_suit=None):
    is_highest_card_trump = get_suit(highest_card) == trump_suit
    is_compare_card_trump = get_suit(compare_card) == trump_suit

    if (trump_suit and is_highest_card_trump and not is_compare_card_trump):
        return True
    if (trump_suit and not is_highest_card_trump and is_compare_card_trump):
        return False
    # if both have similar suit, we could just check the points with order
    if (get_suit(highest_card) == get_suit(compare_card)):
        high = get_card_info(highest_card)
        compare = get_card_info(compare_card)

        return high["points"] >= compare["points"] and high["order"] > compare["order"]

    return True


def pick_winning_card_idx(cards, trump_suit):
    winner = 0
    first_card = cards[0]

    for i in range(winner, len(cards)):
        winning_card = cards[winner]
        compare_card = cards[i]

        if (not trump_suit and get_suit(first_card) != get_suit(compare_card)):
            continue
        if (not is_high(winning_card, compare_card, trump_suit)):
            winner = i

    return winner
# import sys
# sys.path.append('/home/nathan/Desktop/machine_learinng/college/engine/')
from Scores import Score
from copy import deepcopy

def play_n_games(commit_id, number_of_games, GamePlay, players, pickle_file, team_to_monitor='A'):
    scores = {'commit_id': commit_id, 'games_played': number_of_games, 'win': 0, 'loss': 0, 'annuled': 0, 'under_shoot': 0, 'response_time_avg_play': 0, 'response_time_avg_bid': 0, 'response_time_trump_set': 0, }
    for i in range(number_of_games):
        # print(i)
        progress_bar(i, number_of_games)
        d = GamePlay(deepcopy(players), team_to_monitor=team_to_monitor)
        score = d.play(pickle_file)
        # print('\n\n score of one game', score)
        if scores['annuled']:
            scores['annuled']+=score['annuled']
            scores['response_time_avg_bid'] += score['response_time_avg_bid']
            scores['response_time_avg_play'] += score['response_time_avg_play']
            scores['response_time_trump_set'] += score['response_time_trump_set']
        else:
            scores['win']+=score['win']
            scores['loss']+=score['loss']
            scores['under_shoot'] += score['bid'] - score['scored']
            scores['response_time_avg_bid'] += score['response_time_avg_bid']
            scores['response_time_avg_play'] += score['response_time_avg_play']
            scores['response_time_trump_set'] += score['response_time_trump_set']

    scores['response_time_avg_bid'] = scores['response_time_avg_bid']/scores['games_played']
    scores['response_time_avg_play'] = scores['response_time_avg_play']/scores['games_played']
    scores['response_time_trump_set'] = scores['response_time_trump_set']/scores['games_played']
    # print(f'\n scores: {scores}')
    s=Score()
    s.save(scores)
    s.display()


class Card:
    SUITS = ["H", "D", "C", "S"]
    RANKS = ['7', '8', 'Q', 'K', 'T', '1', '9', 'J']
    OTHERS = ["2", "3", "4", "5", "6", "joker"]
    CARD_WEIGHTS = {"J" : 3, "9" : 2, "T" : 1, "1" : 1}
    def __init__(self, suit, rank):
        self.suit = suit.upper()
        self.rank = rank.upper()
        assert suit.upper() in Card.SUITS, f"Suit: {suit.upper()} is not a valid suit"
        assert rank.upper() in Card.RANKS, {rank.upper()} + f"Rank: {rank.upper()} is not a valid rank"
    
    def __str__(self) -> str:
        return self.rank + self.suit
    
    def __eq__(self, card1) -> bool:
        if self.suit == card1.suit and self.rank == card1.rank:
            return True
        return False
    
    def __lt__(self, card1) -> bool:
        if self.suit == card1.suit:
            # if self.rank in Card.CARD_WEIGHTS.keys():
            #     return Card.CARD_WEIGHTS[self.rank] < Card.CARD_WEIGHTS[card1.rank]
            # else:
            return Card.RANKS.index(self.rank) < Card.RANKS.index(card1.rank)
        raise "Cards are not of the same suit."
    
    def __ge__(self, card1) -> bool:
        if self.suit == card1.suit:
            # if self.rank in Card.CARD_WEIGHTS.keys():
            #     return Card.CARD_WEIGHTS[self.rank] < Card.CARD_WEIGHTS[card1.rank]
            # else:
            return Card.RANKS.index(self.rank) >= Card.RANKS.index(card1.rank)
        raise "Cards are not of the same suit."
    
    
    @staticmethod
    def get_all_cards():
        cards = []
        for suit in Card.SUITS:
            for rank in Card.RANKS:
                cards.append(Card(suit, rank))
        return cards

    @staticmethod
    def display(what, cards, return_value = False):
        cards_list_as_string = [str(card) for card in cards]
        if return_value:
            return cards_list_as_string
        
        # print(f"{what}, cards: {cards_list_as_string}")
       

    # elements in list1 greater than every element at list2
    @staticmethod
    def greater_elements_in_list1(list1, list2):
        greater_elements = []
        for card1 in list1:
            is_greater = True
            for card2 in list2:
                if card1 < card2:
                    is_greater = False
                    break
            if is_greater:
                greater_elements.append(card1)
        return greater_elements
        

    @staticmethod
    def throwableCards(cards_at_hand, cards_at_table, did_reveal_trump_in_root_node=False, trump_suit = None) -> list:
        # only card to throw
        if len(cards_at_hand) == 1:
            # print(f"returning {Card.display('', cards_at_hand, return_value=True)}")
            return cards_at_hand
        # Card.display("\n at_table", cards_at_table)
        # Card.display(f"\n @ {player_id} hand", cards_at_hand)
        # print('\n\n --------------------------------------- ')
        # print('Throwable_cards')
        
        print(f"cards_at_table: {len([str(card) for card in cards_at_table])} {[str(card) for card in cards_at_table]}")
        print(f"cards_at_hand: {len([str(card) for card in cards_at_hand])} {[str(card) for card in cards_at_hand]}")
        print(f"did_reveal_trump_in_root_node:{did_reveal_trump_in_root_node}")
        print(f"trump_suit: {trump_suit}")
        # print('--------------------------------------- \n\n')
        if len(cards_at_table) > 0:
            # trumpRevealed rule: if trump suit revealed in this trick
            # can throw any card of trump suit If your partner is winning the
            
            # throw winning trump if available else throw any trump if available else throw any card
            if did_reveal_trump_in_root_node and trump_suit != None:
                # trump suit was revealed in this trick
                # throw winning trump if available else throw any trump if available else throw any card
                trumps_at_hand = [card for card in cards_at_hand if card.suit == trump_suit]
                trumps_at_table = [card for card in cards_at_table if card.suit == trump_suit]
                # print(f'\n\n did_reveal_trump_in_this_trick: {did_reveal_trump_in_root_node} trump:{trump_suit}\n\n')
                
                # friend throw a trump card
                if len(cards_at_table) >= 2 and cards_at_table[-2].suit == trump_suit:
                    # friend is winning :: throw any trump
                    friend_winning = True
                    for trump in trumps_at_table:
                        if trump >= cards_at_table[-2]:
                            friend_winning = False
                            break
                    
                    if friend_winning:
                        # print(f'friend_winning: {[str(card) for card in trumps_at_hand]}')
                        # friend is winning throw any trump
                        # print(f"returning {Card.display('', trumps_at_hand.copy(), return_value=True)}")
                        return trumps_at_hand
                    # print(f"friend not winning:")
                
                if trumps_at_table and trumps_at_hand:
                    # print(f"at table and at hand ")
                    # table has trump and player have trump :: can throw winning trumps only
                    winning_trumps = Card.greater_elements_in_list1(trumps_at_hand, trumps_at_table)
                    if winning_trumps:
                        # print(f"returning {Card.display('', winning_trumps.copy(), return_value=True)}")
                        # have winning trumps
                        # print(f'winning_trump_card_at_hand: {[str(card) for card in trumps_at_hand]}')
                        return winning_trumps
                    return trumps_at_hand   # have trump, doesn't have winning trump
                elif trumps_at_hand:
                    # print(f"returning {Card.display('', trumps_at_hand.copy(), return_value=True)}")
                    # print(f'trumps_at_hand: {[str(card) for card in trumps_at_hand]}')
                    return trumps_at_hand   # have trump, doesn't have winning trump
                else:
                    # print(f'No trump at hand: {[str(card) for card in trumps_at_hand]}')
                    return cards_at_hand.copy()
            else:
                same_as_initial_suit = [card for card in cards_at_hand if card.suit == cards_at_table[0].suit]
                if same_as_initial_suit != []:
                    # print(f"same as initial suit: {[str(card) for card in same_as_initial_suit]}")
                    # print(f"returning {Card.display('same as initial suit', same_as_initial_suit.copy(), return_value=True)}")
                    # have cards same as initial suit
                    return same_as_initial_suit
        # print(f"returning {Card.display('', cards_at_hand.copy(), return_value=True)}")
        return cards_at_hand.copy()

    # every element of list1 is greater than every element of list2

    
    def calculateWinnerIndex(played, trump_suit=None, trump_revealed=False, show_win_score=False):
        # returns the index of the winner
        # trump sute is None if trump is not revealed
        # Card.display('winner_index_played', played)
        # print(f"\n\n calculateWinnerIndex :win_score: {show_win_score}\n trump_suit: {trump_suit}\n played: {Card.display('played', played, True)}")
        assert len(played) <= 4, f"len(played) != 4: {len(played)}"
        # if (trump_suit != None or trump_suit != False) and (trump_suit in [card.suit for card in played]):
        if (trump_revealed) and (trump_suit in [card.suit for card in played]):
            # trump is revealed
            # and trump in played
            # largest trump wins

            trump_cards = [card for card in played if card.suit == trump_suit]
            # print(Card.display('initial', trump_cards))
            winner_index = played.index(max(trump_cards))
            # print(f'\n ---------- first: played:{[str(card) for card in played]} trump_suit:{trump_suit} winner_index:{winner_index}')
            # Card.display('trump cards', trump_cards)
        else:
            # either trump is not revealed
            # or trump is not in played
            # largest of initial suit wins
            initial_suit_cards = [card for card in played if card.suit == played[0].suit]
            # print(Card.display('initial', initial_suit_cards))
            winner_index = played.index(max(initial_suit_cards))
            # print(f'\n ---------- second: played:{[str(card) for card in played]} trump_suit:{trump_suit} winner_index:{winner_index}')
        # print('\n\ncalculate winner trump suit', str(trump_suit))
        result = [winner_index]
        if show_win_score:
            win_score = sum([Card.CARD_WEIGHTS[card.rank] for card in played if card.rank in Card.CARD_WEIGHTS.keys()])
            result.append(win_score)
        return tuple(result)
    
    @staticmethod
    def canRevealTrump(cards_at_hand, cards_at_table):
        if cards_at_table == []:
            # table is empty :: player is first one to throw card
            return False
        # can reveal trump if player doesn't have intital suit's card
        return cards_at_table[0].suit not in [card.suit for card in cards_at_hand]
    @staticmethod
    
    def get_random_trump_reveal_probability(cards_history = [], players_cards = []):
        RANDOM_TRUMP_INITIALIZATION_PROBABILITY = 0.35  # 35% probability for each trick
        return RANDOM_TRUMP_INITIALIZATION_PROBABILITY
# To append to a pickle file
import pickle
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

# dump_pickle({1:2}, 'test.pkl')
# read_pickle('test.pkl')
# dump_pickle({3:4}, 'test.pkl')
# read_pickle('test.pkl')