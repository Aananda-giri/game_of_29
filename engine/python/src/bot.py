from utils import get_suit, get_suit_cards, get_partner_idx, pick_winning_card_idx, is_high, index, find, Card
import random

def get_bid(body):
    """
    Please note: this is bare implementation of the bid function.
    Do make changes to this function to throw valid bid according to the context of the game.
    """

    ####################################
    #     Input your code here.        #
    ####################################

    MIN_BID = 16
    PASS_BID = 0
    challenger_bid = 16

    # bid 16 : when you are the first player to bid, 
    if len(body["bidHistory"]) == 0:
        return {"bid": 16}

    # Donot bid if your partner is winning the bid
    partner_idx = body["playerIds"][(body["playerIds"].index(body['playerId']) + 2)%4]
    # partner_bid = find(body["bidHistory"], lambda bid: bid["playerId"] == partner_idx)
    
    bid_history = body["bidHistory"]
    history_copy = bid_history.copy()
    for bid in history_copy:
        if bid[1] == 0:
            bid_history.remove(bid)    # remove zero bidders
    
    if len(bid_history) > 0:
        challenger_id = bid_history[-1][0]
        challenger_bid = bid_history[-1][1]
        if challenger_id == partner_idx:
            return {"bid": PASS_BID}
    
    suits_at_hand = [card[1] for card in body["cards"]]
    suit_frequencies = {suit: suits_at_hand.count(suit) for suit in suits_at_hand}
    max_suit_frequency = max(suit_frequencies.values())
    max_repeated_suite = [s for s in suit_frequencies.keys() if suit_frequencies[s] == max_suit_frequency]
    max_repeated_suite_ranks = [card[0] for card in body["cards"] if card[1] in max_repeated_suite]
    last_bid = bid_history[-1][1]
    
    defender = body['bidState']['defenderId'] == body['playerId']
    # print(f'\ndefender: {defender}\n')
    # bid <= 20 : 4 same color cards
    if max_suit_frequency == 4:
        if len(bid_history) > 0:
            if defender:
                # you are defender
                bid_val = last_bid
            else:
                # you are challenger: raise the bid by +1 or pass
                bid_val = last_bid + 1
        
        if bid_val <= 20:
            return {"bid": bid_val}
        return {"bid": PASS_BID}

    # bid <= 18/19 : 3 same color cards
    elif max_suit_frequency == 3:
        if len(bid_history) > 0:
            if defender:
                # you are defender
                bid_val = last_bid
            else:
                # you are challenger: raise the bid by +1 or pass
                bid_val = last_bid + 1
        
        # 19 if [J, 9] or [9, A] else 18
        # max_bid = 19 if ('J' in max_repeated_suite_ranks and '9' in max_repeated_suite_ranks) or ('9' in max_repeated_suite_ranks and 'A' in max_repeated_suite_ranks) or ('J' in max_repeated_suite_ranks and 'A' in max_repeated_suite_ranks) else 18
        max_bid = 19 if ('J' in max_repeated_suite_ranks and '9' in max_repeated_suite_ranks and 'T' in max_repeated_suite_ranks) else 18 if ('9' in max_repeated_suite_ranks and 'A' in max_repeated_suite_ranks) or ('J' in max_repeated_suite_ranks and 'A' in max_repeated_suite_ranks) else 17
        if bid_val <= max_bid:
            return {"bid": bid_val}
        return {"bid": PASS_BID}
    
    # bid <= 16/17` : 2 same color cards
    # 17 if [J, 9] or [9, A] else 18
    elif max_suit_frequency == 2:
        if len(bid_history) > 0:
            if defender:
                # you are defender
                bid_val = last_bid
            else:
                # you are challenger: raise the bid by +1 or pass
                bid_val = last_bid + 1
        max_bid = 17 if ('J' in max_repeated_suite_ranks and '9' in max_repeated_suite_ranks and 'T' in max_repeated_suite_ranks) else 16 if ('9' in max_repeated_suite_ranks or 'A' in max_repeated_suite_ranks)  or ('J' in max_repeated_suite_ranks and 'A' in max_repeated_suite_ranks or  '9' in max_repeated_suite_ranks or  'T' in max_repeated_suite_ranks) else 16
        if bid_val <= max_bid:
            return {"bid": bid_val}
        return {"bid": PASS_BID}
    
    # pass: no same color cards
    return {"bid": PASS_BID}


def get_trump_suit(body):
    """
    Please note: this is bare implementation of the chooseTrump function.
    Do make changes to this function to throw valid card according to the context of the game.
    """

    ####################################
    #     Input your code here.        #
    ####################################


    # own_cards = body["cards"]   # ['JS', 'TS', 'KH', '9C']

    suits_at_hand = [card[1] for card in body["cards"]]     # ['S', 'S', 'H', 'C']
    suit_frequencies = {suit: suits_at_hand.count(suit) for suit in suits_at_hand}  # {'S': 2, 'H': 1, 'C': 1}
    max_suit_frequency = max(suit_frequencies.values())                 # 2
    max_repeated_suite = [s for s in suit_frequencies.keys() if suit_frequencies[s] == max_suit_frequency]  # ['S']
    max_repeated_suite_ranks = [card[0] for card in body["cards"] if card[1] in max_repeated_suite]         # ['J', 'T']

    # 1 max repeated suite or 2 max repeated suite or no repeated suite
    suite_index = 0
    max_suite_weigtht_sum = 0
    # No max repeated suits: sort by suit rank of cards
    for i, suit in enumerate(max_repeated_suite):
        suit_cards = [card for card in body["cards"] if card[1] == suit]
        suit_ranks_sum = sum([Card.CARD_WEIGHTS[str(card[0])] for card in suit_cards if card[1] in Card.CARD_WEIGHTS.keys()])
        if suit_ranks_sum > max_suite_weigtht_sum:
            suite_index = i
            max_suite_weigtht_sum = suit_ranks_sum

    return {"suit": max_repeated_suite[suite_index]}


def get_play_card(body):
    """
    Please note: this is bare implemenation of the play function.
    It just returns the last card that we have.
    Do make changes to the function to throw valid card according to the context of the game.
    """

    ####################################
    #     Input your code here.        #
    ####################################

    own_cards = body["cards"]
    first_card = None if len(body["played"]) == 0 else body["played"][0]
    trump_suit = body["trumpSuit"]
    trump_revealed = body["trumpRevealed"]
    hand_history = body["handsHistory"]
    own_id = body["playerId"]
    played = body["played"]
    player_ids = body["playerIds"]
    my_idx = player_ids.index(own_id)
    my_idx = index(
        player_ids, lambda id: id == own_id)
    my_partner_idx = get_partner_idx(my_idx)
    first_turn = (my_idx + 4 - len(played)) % 4
    is_bidder = trump_suit and not trump_revealed

    # if we are the one to throw the first card in the hands
    if (not first_card):
        # print('\n ------------- return1 \n')
        return {"card": random.choice(own_cards)}  # own_cards[-1]}

    first_card_suit = get_suit(first_card)
    own_suit_cards = get_suit_cards(own_cards, first_card_suit)

    # if we have the suit with respect to the first card, we throw it
    if len(own_suit_cards) > 0:
        # print('\n ------------- return10 \n')
        return {"card": random.choice(own_suit_cards)}  # own_suit_cards[-1]}

    # if we don't have cards that follow the suit
    # @example
    # the first player played "7H" (7 of hearts)
    #
    # we could either
    #
    # 1. throw any card
    # 2. reveal the trump

    # trump has not been revealed yet, and we don't know what the trump is
    # let's reveal the trump
    trump_suit = body["trumpSuit"]
    trump_revealed = body["trumpRevealed"]
    if (not trump_suit and not trump_revealed):
        # print('\n ------------- return11 \n')
        return {"revealTrump": True}
    # trump was revealed by me in this hand
    # or
    # I am going to reveal the trump, since I am the bidder

    is_bidder = trump_suit and not trump_revealed
    did_reveal_the_trump_in_this_hand = trump_revealed and trump_revealed["playerId"] == own_id and trump_revealed["hand"] == (\
        len(hand_history) + 1)
    if (is_bidder or did_reveal_the_trump_in_this_hand):
        response = {}
        if (is_bidder):
            response["revealTrump"] = True


    # we don't have any trump suit cards, throw random
    own_trump_suit_cards = get_suit_cards(own_cards, trump_suit)
    if (len(own_trump_suit_cards) == 0):
        # print('\n ------------- return100 \n')
        # print(f'\n ------------ own_cards: {own_cards}')
        return {"card": random.choice(own_cards)}     # own_cards[-1]}

    did_reveal_the_trump_in_this_hand = trump_revealed and trump_revealed["playerId"] == own_id and trump_revealed["hand"] == (
        len(hand_history) + 1)

    # trump was revealed by me in this hand
    # or
    # I am going to reveal the trump, since I am the bidder

    if (is_bidder or did_reveal_the_trump_in_this_hand):
        response = {}
        if (is_bidder):
            response["revealTrump"] = True

        # if there are no trumps in the played
        if (len(get_suit_cards(played, trump_suit)) == 0):
            response["card"] = random.choice(own_trump_suit_cards)  # own_trump_suit_cards[-1]
            # print('\n ------------- return101 \n')
            return response

        winning_trump_card_idx = pick_winning_card_idx(played, trump_suit)
        winning_card_player_idx = (first_turn + winning_trump_card_idx) % 4

        # if we revealed the trump in this round and the winning card is trump, there are two cases
        # 1. If the opponent is winning the hand, then you must throw the winning card of the trump suit against your opponent's card.
        # 2. If your partner is winning the hand, then you could throw any card of trump suit since your team is only winning the hand.
        if (winning_card_player_idx == my_partner_idx):
            response["card"] = random.choice(own_trump_suit_cards)  # own_trump_suit_cards[-1]
            # print('\n ------------- return110 \n')
            return response

        winning_trump_card = played[winning_trump_card_idx]
        winning_card = find(own_trump_suit_cards, lambda card: is_high(
            card, winning_trump_card)) or own_trump_suit_cards[-1]

        # player who revealed the trump should throw the trump suit card
        # print('\n ------------- return111 \n')
        return {"card": winning_card}
    # print('\n ------------- return1000 \n')
    return {"card": own_cards[-1]}
