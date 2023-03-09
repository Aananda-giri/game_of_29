# ucb2 implementation
import random, math, time
from copy import deepcopy
from utils import Card

PLAYERS = ['A1', 'A2', 'B1', 'B2']
PLAYER_IDS = [0,1,2,3]

class Node:
    def __init__(self, players_cards, cards_at_table, cards_not_played, player_index, player_id, parent, trump_suit, trump_revealed=False, card_thrown=None, did_reveal_trump_in_this_trick=False):
        # print(f"players_cards:{players_cards}")
        self.cards = players_cards
        self.cards_at_table = cards_at_table
        self.trump_suit = trump_suit
        self.trump_revealed = trump_revealed
        self.player_index = player_index
        self.player_id = player_id
        self.parent = parent
        self.card_thrown = card_thrown
        self.did_reveal_trump_in_root_node = did_reveal_trump_in_this_trick
        # print(f'\n\n did_reveal_trump_in_this_trick: {self.did_reveal_trump_in_root_node} trump:{self.trump_suit}\n\n')
        # print(f'\n\nnodes card thrown: {self.card_thrown}')
        if cards_not_played == None:
            self.cards_not_played = [card for card in Card.get_all_cards() if card not in players_cards]
        else:
            self.cards_not_played = cards_not_played
        # print(f'\n\nnot_played:{[self.cards_not_played]}\n\n')
        
        self.visit_count = 0
        self.wins = 0
        self.plays = 0
        
        
        self.children = []
        
        
        # self.card_thrown = None
        # self.roundWinner_no = None
        # self.isLeaf = False
    
    def expandNode(self):
        """
        Expand a node to produce all child nodes will all possible moves
        """

        # print(f"\nTrump Revealed: {self.did_reveal_trump_in_root_node}")
        # cards valid to throw
        throwables = Card.throwableCards(self.cards, self.cards_at_table, self.did_reveal_trump_in_root_node, self.trump_suit)
        # print(f'\n\ngot throwables:{[str(card) for card in throwables]}\n')
        for card in throwables:
            # update players cards
            # new_cards = deepcopy(self.cards)
            # new_cards.remove(card)
            # self.card_thrown = card

            # players_cards, cards_at_table, cards_not_played, player_id, parent
            self.children.append(Node(deepcopy(self.cards), self.cards_at_table.copy(), self.cards_not_played, self.player_index, self.player_id, self, self.trump_suit, self.trump_revealed, card))
            # print(f'\n\n children[-1] card thrown: {self.children[-1].cards}')
        
        # [print(str(node.card_thrown)) for node in self.children]
        return self.children
    
    def selectNode(self):
        times_played = self.plays     # number of times any child has been visited
        num_children = len(self.children)
        if times_played < num_children:
            return self.children[times_played]            # select all arms at least once before starting to exploit
        
        
        ucb_values = [0.0 for _ in range(num_children)]
        for child in self.children:
            if child.plays > 0:
                # arm has been chosen at least once
                average_reward = child.wins / child.plays
                exploration = math.sqrt(2 * math.log(times_played) / child.plays)
                ucb_values[self.children.index(child)] = average_reward + exploration
        
        # return the index of arm with the highest UCB value
        # return max(range(self.num_children), key=lambda child: ucb_values[self.children.index(child)])
        selected = max(self.children, key = lambda child: child.wins)
        # print(f"\n\nvalues{selected.wins}{[child.wins for child in self.children]}\n\n")
        return selected
    # def selectNode(self):
    #     selected_node = None
    #     selected_UCT = -float('inf')
        
    #     for child in self.children:
    #         child_UCT = child.calc_UCT()
    #         if child_UCT > selected_UCT:
    #             selected_node = child
    #             selected_UCT = child_UCT
        
    #     return selected_node
    
    def backpropagate(self, reward):
        # update node and root node
        self.plays += 1
        self.parent.plays += 1
        
        n = self.plays
        value = self.wins
        new_value = ((n - 1) / float(n)) * value + (1 / float(n)) * reward
        self.wins = new_value
        # self.parent.plays += 1
    def dump_node(self):
       # print(f"Card:{self.card_thrown} Plays: {self.plays}, Wins: {self.wins}")
       pass

    def calculate_order(self, len_cards_at_table, player_id):
        ordered_player_ids = [player_id]
        # pre: insert players before players index
        # [ordered_player_ids.insert(0, (player_id - (i+1)) % 4) for i in range(len_cards_at_table)]
        # post: insert players after players index
        ordered_player_ids += [i%4 for i in range(player_id + 1, 5 - len(ordered_player_ids) + player_id)]
        print(f'---------- ordered_player_ids: {ordered_player_ids}\n')
        return ordered_player_ids
        # return {"ordered_player_ids": ordered_player_ids[-4:]}
    
    def simulate_node5(self, DISCOUNT_FACTOR):
        # print(f"\n ------throw_one_{self.player_index}:@_hands------- {[str(card) for card in self.cards]} @table {[str(card) for card in self.cards_at_table]} @not_played {[str(card) for card in self.cards_not_played]}")
        # print(f'\n\n--------------- Simulating: {self.card_thrown} ------------------\n\n')
        def append_one_card_at_table(self, player_id, cards_at_hand,cards_not_played, cards_at_table, trump_suit, trump_revealed, possible_trumps):
            # if len(cards_at_hand) == 1:
            #     cards_at_table.append(cards_at_hand[0])
            #     cards_at_hand = []
            #     # return cards_at_hand[0]
            # print(f"\n ------throw_one_{self.player_index}:{player_id} @_hands------- {[str(card) for card in cards_at_hand]} @table {[str(card) for card in cards_at_table]}")
            # if len(cards_at_table) == 4:
            #     return (cards_at_table, cards_at_hand, cards_not_played, trump_suit, trump_revealed)
            if player_id == self.player_index:
                if not trump_revealed:
                    # trump not revealed
                    cant_follow_suit = cards_at_table[0].suit not in [card.suit for card in cards_at_hand] if len(cards_at_table) > 0 else False
                    if cant_follow_suit:
                    # if random.random() < Card.get_random_trump_reveal_probability():
                        # trump_suit = random.choice(possible_trumps)
                        # trump_suit = trump_suit
                        trump_revealed = True

                # players turn to throw
                throwable_cards = Card.throwableCards(cards_at_hand, cards_at_table, trump_suit = trump_suit)
                # print(f"\n ------throwable @_hands------- {[str(card) for card in cards_at_hand]} @table {[str(card) for card in cards_at_table]} : {[str(card) for card in throwable_cards]}")
                random_card_thrown = random.choice(throwable_cards)
                cards_at_hand.remove(random_card_thrown)
                cards_at_table.append(random_card_thrown)
            else:
                # opponents (other players) turn to throw
                if not trump_suit:
                    # randomly initialize trump: set or not set by player
                    # trump not revealed
                    cant_follow_suit = cards_at_table[0].suit not in [card.suit for card in cards_not_played] if len(cards_at_table) > 0 else False
                    if cant_follow_suit or random.random() < Card.get_random_trump_reveal_probability():
                        if not trump_revealed:
                            trump_revealed = True

                
                
                
                throwable_cards = Card.throwableCards(cards_not_played, cards_at_table, trump_suit = trump_suit)
                # print(f'\n-------- throwable_cards: {[str(card) for card in throwable_cards]}')
                random_card_thrown = random.choice(throwable_cards)
                cards_not_played.remove(random_card_thrown)
                cards_at_table.append(random_card_thrown)
                # assert len(cards_at_table) + len(cards_at_hand) + len(cards_not_played) + len([Card(c[1], c[0]) for c in body["played"]]) == 32, f'sum of cards not =32 at_hand:{[str(card) for card in cards_at_hand]} at_table:{[str(card) for card in cards_at_table]} not_played:{[str(card) for card in cards_not_played]} already_played:{[str(card) for card in [Card(c[1], c[0]) for c in body["played"]]]}'
            return (cards_at_table, cards_at_hand, cards_not_played, trump_suit, trump_revealed)

        if not self.trump_suit:
            possible_trumps = ['c', 'D', 'H', 'S']  # None : by default
        else:
            possible_trumps = [self.trump_suit] # trump set by user and not revealed yet
        print(f'-------------\npossible_trumps: {possible_trumps}\n-------------')

        # genereate seperate possible trees by trump
        for trump in possible_trumps:
            trump_suit = trump
            trump_revealed = self.trump_revealed
            
            cards_at_table = deepcopy(self.cards_at_table)
            cards_at_hand = deepcopy(self.cards)
            cards_not_played = deepcopy(self.cards_not_played)
            print(f'\n\n--------------- Simulating: \ntable: {[str(c) for c in cards_at_table]} \n hand:{len(cards_at_hand)} {[str(c) for c in cards_at_hand]}\n thrown: {self.card_thrown}\n not_played: {len(cards_not_played)} {[str(card) for card in cards_not_played]}------------------\n\n')
            
            wins = 0
            # ordered players :: reference/analysis: archive.py problem 1
            # card already thrown by player, yet to append to table
            ordered_player_ids = (self.calculate_order(len(cards_at_table), self.player_index))
            
            # loop order because some players may have already thrown cards at first trick
            # loop_order = ordered_player_ids[ordered_player_ids.index(self.player_index):]
            # ordered_player_ids = [(i+ self.player_index)%4 for i in range(4)][:4-len(cards_at_table)]
            loop_order = [(i+ self.player_index)%4 for i in range(4)][:4-len(cards_at_table)]
            print(f'---------- loop order: player_index: {self.player_index} {loop_order}\n')
            first_trick = True   # throw self.card_thrown in first trick
            # player_index = ordered_player_ids.index[self.player_index]
            # print(f'\n\nordered player id : {ordered_player_ids}')
            # print(f'before_player_cards:{len(cards_at_hand)}, other_cards:{len(cards_not_played)}')
            initial_len_cards_at_hand = len(cards_at_hand)
            while len(cards_at_hand) > 0:
                # print(f'after_player_cards:{len(cards_at_hand)}, other_cards:{len(cards_not_played)}')
                # player throw 1 card
                while len(cards_at_table) < 4:
                    for player_id in loop_order:
                        if first_trick:
                            first_trick = False
                            cards_at_table.append(self.card_thrown)
                            cards_at_hand.remove(self.card_thrown)
                            # print(f"\n ------throw_one_{self.player_index}:{player_id} @_hands------- {[str(card) for card in cards_at_hand]} @table {[str(card) for card in cards_at_table]}")
                        else:
                            cards_at_table, cards_at_hand, cards_not_played, trump_suit, trump_revealed = append_one_card_at_table(self, player_id, cards_at_hand, cards_not_played, cards_at_table, trump_suit, trump_revealed, possible_trumps)
                            assert len(cards_at_table) <= 4 , f'cards at table is greater than 4: {len(cards_at_table)} {[str(card) for card in cards_at_table]}'
                            
                ## check if player wins
                winner_index, win_score = Card.calculateWinnerIndex(cards_at_table, trump_suit, trump_revealed, show_win_score=True)
                print(f"\n\n-------- winner_index:{winner_index} ordered_player_ids:{ordered_player_ids} player_index:{self.player_index} at_table:{[str(card) for card in cards_at_table]} trump:{self.trump_suit}")
                cards_at_table = [] # clear cards at table
                # print(f'ordered ids: {ordered_player_ids}, player_index:{self.player_index}')
                # Card.display('@table', cards_at_table)
                # print(f'winner index: {winner_index}')
                # print('winner_index:', winner_index)
                
                if ordered_player_ids[winner_index] == self.player_index:   # or ordered_player_ids[(winner_index+2)%4] == self.player_index:
                    # player's team won
                    # print('player team won')
                    wins += win_score * (1 - float(DISCOUNT_FACTOR)) ** (initial_len_cards_at_hand - len(cards_at_hand) - 1)
                else:
                    # print('player team lost')
                    wins -= 0.3 * (win_score * (1 - float(DISCOUNT_FACTOR)) ** (initial_len_cards_at_hand - len(cards_at_hand) - 1))
                # update ordered player
                ordered_player_ids = PLAYER_IDS[ordered_player_ids[winner_index]:] + PLAYER_IDS[:ordered_player_ids[winner_index]]
                loop_order = ordered_player_ids
        return wins/len(possible_trumps)
    
    def __str__(self) -> str:
        return str(self.card_thrown)

def get_play_card(body, did_reveal_trump_in_this_trick, DISCOUNT_FACTOR, cards_not_played=None, n_simulations = 1000, average_reward_threshold=None):
    # print(f'\n\n get_play_discount_factor: {DISCOUNT_FACTOR} \n\n')
    # only one card to throw
    if len(body["cards"]) == 1:
        # print(f"\n--------only card to throw: {body['cards'][0]} --------\n")
        return body["cards"][0]

    # Create the root node to start with <Selection> 
    rootNode = Node(players_cards=deepcopy(body["cards"]), cards_at_table=deepcopy(body["played"]), cards_not_played = cards_not_played, player_index=body["playerIds"].index(body["playerId"]), player_id=str(body['playerId']), parent=None, trump_suit=body["trumpSuit"], trump_revealed = body["trumpRevealed"], card_thrown=None, did_reveal_trump_in_this_trick = did_reveal_trump_in_this_trick)
    # print(rootNode.did_reveal_trump_in_root_node)

    # Create the first level children <expansions>
    nodes = rootNode.expandNode()
    
    
    # Run the simulation 10,000 times
    # for i in range(1000):
    # print(f'\n\n time.time: {time.time()} sum: {body["timeRemaining"] + float(body["startTime"])} starttime: {body["startTime"]} remaining: {body["timeRemaining"]}')
    simulate_count = 0
    # while time.time() < body["timeRemaining"]/1000 + float(body["startTime"]):
    # while time.time() < 0.12 + float(body["startTime"]):
    
    # <For early stopping>
    # Average Reward Threshold for stopping the simulation
    
    if average_reward_threshold == None or average_reward_threshold == 0:
        average_reward_threshold = 0.0001
    # print(f'\n\n average_reward_threshold : {average_reward_threshold}\n\n')
    # Keep track of the average reward in the previous iteration
    previous_average_reward = 0
    rewards = []

    while simulate_count < n_simulations:
        # while time.time() < start_time + body['timeRemaining'] - 0.3:
        simulate_count += 1
        
        # select the node to simulate   <Selection: by UCB2>
        node = rootNode.selectNode()
        
        # <simulate> and <Backpropagate>
        # print(f"\n\nnode: {node}\n\n")
        # if node.player_id[0] == 'A':    # Team A
        win_value = node.simulate_node5(DISCOUNT_FACTOR)
        # else:   # TEAM B
        #     win_value = node.simulate_node5_neg(DISCOUNT_FACTOR)
        rewards.append(win_value)

        node.backpropagate(win_value)
        # node.backpropagate(win_value)
        # print('\n\n Count', simulate_count)
        
        # <early stopping>
        # Calculate the average reward
        # if node.player_id[0] == 'B':    # Team A
        average_reward = sum(rewards) / (simulate_count + 1)
        # Check if the algorithm has converged
        if abs(average_reward - previous_average_reward) < average_reward_threshold:
            break
        # Update the previous average reward
        previous_average_reward = average_reward
    # print('\n\n SimulateCount', simulate_count)
    
    # print(f"\n\nlen_nodes={len(nodes)}")
    # Dislpay the dump
    [node.dump_node() for node in nodes]
    Card.display('cards at table', nodes[0].cards_at_table)
    # Card.display('cards at table', nodes[1].cards_at_table)
   # print(f'\n\n trump card: {nodes[0].trump_suit}')

    # Find the node that has been explored the highest number of times
    # [print(str(node.card_thrown)) for node in nodes]
    nodes.sort(key=lambda x: x.wins, reverse=True)
    # print(f" iterations: {simulate_count+1}, choice: {nodes[0].card_thrown}, choices:{[str(child) for child in rootNode.children]}, Average reward: {sum(rewards) / (simulate_count+1)}")
    return nodes[0].card_thrown

def bhoos_compatible_play(body, start_time, n_simulations, DISCOUNT_FACTOR):
    # rootNode = Node(players_cards=deepcopy(body["cards"]), cards_at_table=deepcopy(body["played"]), cards_not_played = None, player_index=body["playerIds"].index(body["playerId"]), parent=None, trump_suit=body["trumpSuit"])
    # print("\n\n ------------ started -------------- \n\n")
    # print(f"\n\n threshold: {body['average_reward_threshold']} \n")
    body_converted = {"cards": [Card(c[1], c[0]) for c in body["cards"] ], "played": [Card(c[1], c[0]) for c in body["played"] ], "playerIds": body["playerIds"], "playerId": body["playerId"], "trumpSuit": body["trumpSuit"], "timeRemaining" : float(body['timeRemaining'])/(8 - len(body["handsHistory"])), "startTime": start_time, "trumpRevealed": body["trumpRevealed"]}
    # print(f'\n\nbody_converted : {body_converted}\n\n')

    # print(f'\n\n ---- trumpRevealed: {body_converted["trumpRevealed"]} by_player:{body_converted["trumpRevealed"]["playerId"] == body_converted["playerId"]} hand: {body_converted["trumpRevealed"]["hand"]} hist.len: {(len(body["handsHistory"]))}')
    did_reveal_trump_in_this_trick = body_converted["trumpRevealed"] and body_converted["trumpRevealed"]["playerId"] == body_converted["playerId"] and body_converted["trumpRevealed"]["hand"] - 1 == (len(body["handsHistory"]))
    # print(f'revealed: {body["trumpRevealed"]} by:{body["trumpRevealed"]["playerId"]} at: {body["trumpRevealed"]["hand"]} hand_history_len{len(body["handsHistory"])} me: {body["playerId"]}  res: {did_reveal_trump_in_this_trick}')
    if not did_reveal_trump_in_this_trick:
        # see if can reveal trump
        if body["played"] and not body["trumpRevealed"]:    # not first card of trick, and trump not already revealed
            suits_of_cards_player_have = [card[-1] for card in body["cards"]]
            initial_table_suit = body["played"][0][-1]

            cant_follow_suit = initial_table_suit not in suits_of_cards_player_have
            if cant_follow_suit:
               # Player can reveal trump
               # print("\n\n ------------ revealed trump -------------- \n\n")
               # print(f"players cards: {body['cards']} \n cards at table: {body['played']} \n\n")
               
               # dont reveal trump if partner is winning the trick
               if len(body['played']) >= 2 :
                    winning_player_index = Card.calculateWinnerIndex(body_converted['played'], body['trumpSuit'], body['trumpRevealed'], show_win_score=False)[0]
                    partner_index = None
                    if len(body['played']) == 2:
                        partner_index = (2 * len(body['played']) - 4) % 4
                    elif len(body['played']) == 3:
                        partner_index = 1
                    if not winning_player_index == partner_index:
                        # partner is not winning the trick : reveal trump
                        return {"revealTrump": True}
                    else:
                        # partner is winning the trick : dont reveal trump
                        # throw min. of throwable cards
                        throwables = Card.throwableCards(body_converted['cards'], body_converted['played'], False, body['trumpSuit'] if body['trumpRevealed'] else None)
                        
                        # Get min. throwable card from among different suits
                        throwable_suits = [card.suit for card in throwables]
                        min_card = throwables[0]
                        for suit in throwable_suits:
                            suit_cards = [card for card in throwables if card.suit == suit]
                            min_suite_card = min(suit_cards)
                            if Card.RANKS.index(min_suite_card.rank) < Card.RANKS.index(min_card.rank):
                                if ((min_card.suit != body['trumpSuit']) and (min_suite_card.suit != body['trumpSuit'])) or (min_card.suit == body['trumpSuit'] and min_suite_card.suit != body['trumpSuit']):
                                    # either both are trump or (min_card is trump and min_suite_card is not trump)
                                    min_card = min_suite_card

                        # print(f'\n\n throwables: {[str(card) for card in throwables]} min_throwable:{min(throwables)}')
                        return {"card": str(min_card)}
    
    cards_already_played = [Card(c[1], c[0]) for c in body["played"]]
    for hand in body["handsHistory"]:
        cards_already_played += [Card(c[1], c[0]) for c in hand[1]]
    all_cards = Card.get_all_cards()
    
    cards_not_played = [card for card in all_cards if card not in cards_already_played] # remove cards already played
    print(f'\n-----------------------cards not played hist.: {[str(card) for card in cards_not_played]}-----------------------\n')
    cards_not_played = [card for card in cards_not_played if card not in body_converted['cards']]   # remove players cards
    print(f'\n-----------------------cards not played  cards.: {[str(card) for card in cards_not_played]}-----------------------\n')
    cards_not_played = [card for card in cards_not_played if card not in body_converted['played']]   # remove cards at table
    print(f'\n-----------------------cards not played  table: {[str(card) for card in cards_not_played]}-----------------------\n')
    # print(f"\n ------hand_hist: {body['handsHistory']}throw_one_{body_converted['playerId']}:@_hands------- {[str(card) for card in body_converted['cards']]} @table {[str(card) for card in body_converted['played']]} @not_played {[str(card) for card in cards_not_played]}")
    # Card.display("\n\nnot already played", cards_not_played)
    # print(f'\n\n bhoos_discount_factor: {DISCOUNT_FACTOR} \n\n')
    best_card_to_throw = get_play_card(body_converted, did_reveal_trump_in_this_trick, DISCOUNT_FACTOR, cards_not_played, n_simulations, body['average_reward_threshold'] if 'average_reward_threshold' in body.keys() else None)
    response = {"card": str(best_card_to_throw)}
    
    





    # copy without understanding
    # trump has not been revealed yet, and we don't know what the trump is
    # let's reveal the trump
    # trump_suit = body["trumpSuit"]
    # trumpRevealed = body["trumpRevealed"]
    # if (not trump_suit and not trumpRevealed):
    #     return {"revealTrump": True}
    # # trump was revealed by me in this hand
    # # or
    # # I am going to reveal the trump, since I am the bidder

    # is_bidder = trump_suit and not trumpRevealed
    # handHistory = body["handsHistory"]
    # did_reveal_the_trump_in_this_hand = trumpRevealed and trumpRevealed["playerId"] == body["playerId"] and trumpRevealed["hand"] == (
    #     len(handHistory) + 1)
    # if (is_bidder or did_reveal_the_trump_in_this_hand):
    #     if (is_bidder):
    #         response["revealTrump"] = True
    # print(f"------- sending response {response} ")
    return response



if __name__ == "__main__":
    body = {"cards": [Card(suit='C', rank='J'), Card(suit='D', rank='J'), Card(suit='H', rank='J'), Card(suit='H', rank='Q'), Card(suit='H', rank='8'), Card(suit='H', rank='9'), Card(suit='D', rank='1'), Card(suit='H', rank='Q'), ], "played": [Card(suit='S', rank='1'), Card(suit='S', rank='K')], "playerIds": [0, 1, 2, 3], "playerId": 0, "trumpSuit": "H"}
    best_card_to_throw = get_play_card(body)
   # print(f"card to play: {best_card_to_throw}")

'''
## todo
  - future discount factor: 
  {0:}
  reward = r0 + (1-𝛾)r1 + (1-𝛾)**2*r2 + (1-𝛾)**3*r3 + (1-𝛾)**4*r4 + (1-𝛾)**5*r5 + (1-𝛾)**6*r6 + (1-𝛾)**7*r7
  𝛾 = 1 -> 100% discount
  𝛾 = 0 -> 0% discount
  
  for i in range(1,9):
    print(0.75**i*100)
caution:
    - set high: agent will select low present reward over high future reward
    - set low: imperfect information, agent will select high present reward over low future reward

  - agressive: higher future discount factor proportional to my bid
  - defensive: higher future discount factor proportional to opponent's bid
  - agressive: lower future discount factor proportional to my bid

  - Remove Trump Revealed from Card.GetWinnerIndex, give None as trump if not revealed
  - player removed card from hand during expand, again first to throw from at_hand during simulation
  - debug :: simulate_node: line 112 :: Card.throwableCards(cards_not_played, cards_at_table, did_reveal_trump_in_root_node=False, trump_suit = None))
  - same reward if you won or friend won
  
  - performance metrics for engine
  - implement this code for actual game
    - address cards already played
  * simulation
    - revealTrump logic: when player can't follow the suit ; 
       - throwables in revealed trick = winnin_trumps if winning_trumps else trumps if trumps else any_card
    - find optimal val. of : RANDOM_TRUMP_INITIALIZATION_PROBABILITY
    - don't ignore order of throw (winner throw first)
    
- no backpropagation of wins below

## done
    - same reward :: partner winning or player winning
    - address cards already played by others
    - revealTrump logic: when player can't follow the suit ; 
        - throwables in revealed trick = winnin_trumps if winning_trumps else trumps if trumps else any_card
    - remove playerId argument of Card.throwableCards() is not used
    - use divided timeRemaining for throw logic  
    
    * simulation:
        - dont ignore trump : randomly initialize trump is not already initialized
        - Oppponent only throws throwable

## Info
    - rewards accumulate over the whole game. 
    - Reward(Each Trick Victory) = sum of card values in Trick won
'''