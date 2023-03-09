import random
import sys
from copy import deepcopy
commit_id = sys.argv[1]
number_of_games = int(sys.argv[2])
pickle_file = sys.argv[3]   # file_name to store the game data
# to import Card from utils.py
sys.path.append("/home/machina/Documents/machine_learning/college/engine/python/src")
from utils import Card
from utils import play_n_games, dump_pickle, load_pickle
from Api import Player



class GamePlay:
    def __init__(self, players, team_to_monitor = "A"):
        self.players = players
        self.teams = {"A": {"won": 0, "bid" : -1, "round_points": 0, "players":[players[0], players[2]]}, "B": { "won": 0, "bid" : -1, "round_points": 0, "players":[players[1], players[3]]}}   # update bid_value later
        self.train_data = {"A1":{"bid": 0, "won": 0, "initial_cards": [], 'final_cards': [], "set_trump": False}, "A2":{"bid": 0, "won": 0, 'initial_cards': [], 'final_cards': [], "set_trump": False}, "B1":{"bid": 0, "won": 0, 'initial_cards': [], 'final_cards': [], "set_trump": False}, "B2":{"bid": 0, "won": 0, 'initial_cards': [], 'final_cards': [], "set_trump": False}, "handsHistory": []}
        self.trumpSuit = False  # 'C' or 'D' or 'H' or 'S'
        self.trumpRevealed = False  # {hand: 2, playerId: "A2",} :: hand at which the trump was revealed and the player who revealed the trump
        self.is_annulled = False
        self.team_to_monitor = team_to_monitor
    
    def display_states(self, lable = ""):
        print("\n\t",  "-"*50, "\t")
        print("\t\t", lable)
        print("\t",  "-"*50, "\t")
        for player in self.players:
            print(f"\nplayer:{player.id}")
            print(f"cards: {[str(card) for card in player.cards]}")
            print(f"bid_value: {player.bid_value}")
        print(f"teams: {self.teams}")
        print(f"trump: {self.trumpSuit}")
        # time.sleep(3)   # allowing result to see

    def update_round_points(self, bid_winner, bid_value):
        # updates round point for bid winning team at the end of each round
        if sum([Card.CARD_WEIGHTS[card.suit] for card in self.teams[bid_winner.team]["cards"] if card.suit in Card.CARD_WEIGHTS.keys()]) >= self.bid_value:     # update team "A" points
            self.teams[bid_winner.team]["won"] += 1
            winning_team = bid_winner.team
        else:
            self.teams[bid_winner.team]["won"] -= 1
            winning_team = "B" if bid_winner.team == "A" else "A"
        return winning_team
    
    # implementation of ask_bid
    def bid_logic(self):
        # for bhoose data compatibility
        # initially make challenger bid against itself
        # if passes :: bid is 16 and it is defender
        # if bid >16 :: bid is bid_value and it is defender
        
        biddingPlayers = [player for player in self.players]
        biddingPlayers[0].bid_value = 16
        bidState =  {
            "defenderId": biddingPlayers[0].id,
            "defenderBid": biddingPlayers[0].bid_value,
            "challengerId": biddingPlayers[0].id,
            "challengerBid":  -1
        }
        bidHistory = []
        

        while(1):
            # print('\nwhile1', bidState)
            bid = biddingPlayers[0].request_bid(bidHistory, bidState)   # request_bid also validates bid
            if bidHistory == [] and bid <16:
                bid = 16     # A1's minimum bid is 16
            biddingPlayers[0].bid_value = bid
            bidHistory.append([biddingPlayers[0].id, biddingPlayers[0].bid_value])      # update bid history
            # print(f'\nreturned bid\'{bid}\'')
            if bid == 28:
                return {'bid_winner': biddingPlayers[0], 'bid_value': biddingPlayers[0].bid_value, 'bid_history': bidHistory}
            elif bid == 0:
                # defender passed, ask next challenger for bid
                if len(bidHistory) != 1:
                    # dont remove first player if it passes
                    # defender passed, challenger is now defender
                    biddingPlayers.remove(biddingPlayers[0])  # defender and challenger automatically updated
                
                if len(biddingPlayers) == 1:
                    # last man standing -> bid winner 
                    return {'bid_winner': biddingPlayers[0], 'bid_value': biddingPlayers[0].bid_value, 'bid_history': bidHistory}
                
            while(1):
                bidState =  {   # updating bid state
                    "defenderId": biddingPlayers[0].id,
                    "defenderBid": biddingPlayers[0].bid_value,
                    "challengerId": biddingPlayers[1].id,
                    "challengerBid": biddingPlayers[1].bid_value
                }
                # print('\nwhile2', bidState)
                
                bid = biddingPlayers[1].request_bid(bidHistory, bidState) # request_bid also validates bid
                biddingPlayers[1].bid_value = bid
                bidHistory.append([biddingPlayers[1].id, biddingPlayers[1].bid_value])      # update bid history
                
                if bid == 28:
                    # defen
                    return {'bid_winner': biddingPlayers[1], 'bid_value': bid, 'bid_history': bidHistory}
                elif bid != 0:
                    # challenger did not passed :: ask defender for bid
                    break
                else:
                    # challenger passed :: ask next challenger for bid
                    biddingPlayers.remove(biddingPlayers[1])   # challenger automatically updated
                    if len(biddingPlayers) == 1:
                        # last man standing -> bid winner 
                        return {'bid_winner': biddingPlayers[0], 'bid_value': biddingPlayers[0].bid_value, 'bid_history': bidHistory}
            
            bidState =  {   # updating bid state
                    "defenderId": biddingPlayers[0].id,
                    "defenderBid": biddingPlayers[0].bid_value,
                    "challengerId": biddingPlayers[1].id,
                    "challengerBid": biddingPlayers[1].bid_value
                }
    
    # ---------------------------------------
    # implementation of play_card after bid
    # ---------------------------------------
    def play_logic(self, trumpSuit, bidHistory, bid_winner):
        def rotate_randomly(players):
            i = random.randint(0,4)
            players = players[i:] + players[:i]
            # for i in range(random.randint(0,10)):
            #     players.append(players.pop(0))
            return players

        # trumpSuit = False       # bhoos data compatibility (otherwise would use None)
        # trumpSuit = trumpSuit     # defined earlier
        handsHistory = []   # stores the history of hands/tricks played [initial_player, [cards_played], trick_winner ]

        players = rotate_randomly([player for player in self.players])
        # print("\n trying slicing: ", players)
        
        bid_winner_index = players.index(bid_winner)
        ordered_players = players[bid_winner_index:] + players[:bid_winner_index]
        print(f'\nordered_players: {ordered_players}')
        trick_winner = ordered_players[0]
        
        roundHistory = {players[0].id:[], players[1].id:[], players[2].id:[], players[3].id:[]}    # history for nural nets
        for i in range(8): # 8 tricks in one round
            # throw card logic
            print('\nrange9\n')
            played = [] # cards at table
            
            trick_history = {players[0].id:{'reward':0, 'reward_partner_won': 0}, players[1].id:{'reward':0, 'reward_partner_won': 0}, players[2].id:{'reward':0, 'reward_partner_won': 0}, players[3].id:{'reward':0, 'reward_partner_won': 0}}    # to append to history_for_nural_nets
            for player in ordered_players:
                trick_history[player.id]['trump_revealed'] = True if self.trumpRevealed else False # data for neural nets
                trick_history[player.id]['cards_at_table'] = [str(card) for card in played] # data for neural nets
                trick_history[player.id]['cards_at_hand'] = [str(card) for card in player.cards] # data for neural nets
                trick_history[player.id]['opponent_cards'] = [str(card) for card in ordered_players[0].cards + ordered_players[1].cards + ordered_players[2].cards + ordered_players[3].cards if card not in player.cards] # data for neural nets
                print(f"\n- --------- pcards_at_hand:{player.cards}, \n{trick_history[player.id]['cards_at_hand']}")
                # print('for_player')
                # request_play_card(self, player, bidHistory, handsHistory, played, trumpsuit)
                response = player.request_play_card(bidHistory, handsHistory, played, self.trumpRevealed, trumpSuit if self.trumpRevealed else False, self.teams, False)
                print(f'#trumpRevealed{self.trumpRevealed}')
                revealed_trump_in_this_trick = False
                if "revealTrump" in response.keys():
                    print('#revealing_trump')
                    # player request for trump reveal :: player_can-> asserted from request_play_card function
                    # player asked for reveal trump
                    self.trumpRevealed = {
                        "hand": i + 1,                 # represents the hand/trick at which the trump was revealed
                        "playerId": player.id,     # the player who revealed the trump
                    }
                    
                    # request for throw card after trump reveal
                    response = player.request_play_card(bidHistory, handsHistory, played, self.trumpRevealed, trumpSuit if self.trumpRevealed else False, self.teams, True)
                    revealed_trump_in_this_trick = True
                
                if revealed_trump_in_this_trick:
                    throwable_cards = Card.throwableCards(player.cards, played, did_reveal_trump_in_root_node=True, trump_suit = self.trumpSuit)
                else:
                    throwable_cards = Card.throwableCards(player.cards, played, did_reveal_trump_in_root_node=False, trump_suit = self.trumpSuit)
                assert response["card"] in throwable_cards, "Expected : " + str([str(card) for card in throwable_cards]) + " but got: " + str(response["card"]) +  str(player.get_play_payload(bidHistory, handsHistory, played, self.trumpRevealed, trumpSuit if self.trumpRevealed else False, self.teams, False))
                trick_history[player.id]['has_set_trump'] = player.has_set_trump # data for neural nets
                trick_history[player.id]['probable_trumps'] = [self.trumpSuit] if self.trumpRevealed or player.has_set_trump else ['C', 'D', 'H', 'S']   # data for neural nets
                trick_history[player.id]['throwable_cards'] =[str(card) for card in throwable_cards] # data for neural nets
                trick_history[player.id]['thrown'] = str(response["card"]) # data for neural nets
                trick_history[player.id]['throwable_cards'] = [str(card) for card in throwable_cards] # data for neural nets
                trick_history[player.id]['revealed_trump_in_this_trick'] = revealed_trump_in_this_trick
                
                print(f'response: card: {str(response["card"])}')
                played.append(response["card"])
                player.cards.remove(response["card"])   # remove card from players cards
                print(f'\n\n played: {[str(card) for card in played]}')
        
        
            # print(f'\n\n calculating winner:: played: {played}, trumpSuit: {trumpSuit if self.trumpRevealed else False}\n\n')
            (trick_winner_index, win_points) = Card.calculateWinnerIndex(played = played.copy(), trump_suit = trumpSuit if self.trumpRevealed else False, show_win_score = True)
            # update team points for trick winner
            trick_winner = ordered_players[trick_winner_index]
            self.teams[trick_winner.team]["won"] += win_points
            
            trick_history[trick_winner.id]['reward'] = win_points # data for neural nets
            trick_history[ordered_players[(trick_winner_index + 2)%4].id]['reward_partner_won'] = win_points # data for neural nets
            [roundHistory[player.id].append(trick_history[player.id]) for player in ordered_players]   # data for neural nets
            handsHistory.append([trick_winner, played, trick_winner])   # player payload data
        
        

            # update order of players for next game
            ordered_players = ordered_players[trick_winner_index:] + ordered_players[:trick_winner_index]
        return handsHistory, roundHistory
            

    def update_scoreboard(self):
        # team either looses (decrease round_points) or wins (increase round_points)
        bid_winning_team = "A" if self.teams["A"]["bid"] > self.teams["B"]["bid"] else "B"
        
        if self.teams[bid_winning_team]["won"] >= self.teams[bid_winning_team]["bid"]:
            # bid winning team has scored gte bid value
            self.teams[bid_winning_team]["round_points"] += 1   # bid winning team scores gte what they bid
        else:
            self.teams[bid_winning_team]["round_points"] -= 1   # bid winning team scores lte what they bid
        self.display_states("after update scoreboard")
    def test_annull_game(self):
        # annull game if a team does not has any trump card in entire game
            team_a_cards = [card for player in self.players if player.team == 'A' for card in player.cards]
            team_b_cards = [card for player in self.players if player.team == 'B' for card in player.cards]
            for team_cards in [team_a_cards, team_b_cards]:
                if self.trumpSuit not in [card.suit for card in team_cards]:
                    self.is_annulled = True
            
            # annull game if any player has all 4 jacks among 8 cards dealt
            for player in self.players:
                all_ranks = [card.rank for card in player.cards]
                if all_ranks.count('J') == 4:
                    self.is_annulled = True
    def record(self, value):
        print('\n\nvalue\n', value)
    def play(self, pickle_file_name = None):
        # initialize cards
        
        handsHistory = []
        
        self.display_states("Initially")
        
        # a complete game <game ends when one team wins 6 games or looses 6 games>
        
        # while abs(self.teams["A"]["round_points"]) < 6 and abs(self.teams["B"]["round_points"]) < 6:
        for i in range(1):    # only one round
            # distribute initial 16 cards (4 cards each)
            shuffled_cards = Card.get_all_cards()
            random.shuffle(shuffled_cards)

            # distribute 4-cards each initially
            for player in self.players:
                player.cards = shuffled_cards[:4].copy()
                shuffled_cards = shuffled_cards[4:]
            
            self.display_states("cards distribute || before bid")

            # ------------------
            # bidding
            # ------------------
            BID_RESULTS = self.bid_logic()
            
            for player in self.players:
                # storing for neural nets
                self.train_data[player.id]['initial_cards'] = [str(card) for card in player.cards]
            
            print('---------------------------------BID_RESULTS --------------------\n', BID_RESULTS)
            BID_WINNER = BID_RESULTS['bid_winner']
            bidHistory = BID_RESULTS['bid_history']
            
            # update bid value of teams
            self.teams[BID_WINNER.id[0]]['bid'] = BID_RESULTS['bid_value']

            # ask for trump to top bidder :: setting trump card :: 
            trump_suit = BID_WINNER.request_trump_set(bidHistory)
            print('---------------------------------bidHistory --------------------\n', bidHistory)
            assert trump_suit in Card.SUITS, f"Trump suit must be one of the four suits not \'{trump_suit}\'"
            self.trumpSuit = trump_suit
            
            # ---------------------------------------
            # distribute remaining cards (4 each)
            # ---------------------------------------
            for player in self.players:
                player.cards.extend(shuffled_cards[:4].copy())
                shuffled_cards = shuffled_cards[4:]
            self.display_states("after bid || before play")
            for player in self.players:
                # storing for neural nets
                self.train_data[player.id]['final_cards'] = [str(card) for card in player.cards]

            # check if game is annulled after trump set
            self.test_annull_game()
            if self.is_annulled:
                break

            # ---------------------------------------
            # play_cards for 8 rounds
            # ---------------------------------------
            handsHistory, neuralHistory = self.play_logic(self.trumpSuit, bidHistory, BID_WINNER)
            for hist in handsHistory:
                self.train_data['handsHistory'].append([str(hist[0]), [str(card) for card in hist[1]], str(hist[2])])
            
            # update train_data
            self.train_data[str(BID_RESULTS['bid_winner'])]['set_trump'] = True
            self.train_data[str(BID_RESULTS['bid_winner'])]['bid'] = BID_RESULTS['bid_value']
            for player in self.players:
                self.train_data[player.id]['won'] = self.teams[player.team]['won']
                self.train_data[player.id]['num_simulations'] = player.num_simulations
                self.train_data[player.id]['is_random_player'] = player.is_random_player
                self.train_data[player.id]['neuralHistory'] = neuralHistory[player.id]
                # self.train_data[team + '1']['bid'] = self.train_data[team + '2']['bid'] = self.teams[team]['bid']
                # self.train_data[team + '1']['won'] = self.train_data[team + '2']['won'] = self.teams[team]['won']

            # print('--------------------------------- train_data --------------------\n', self.train_data)
            dump_pickle(self.train_data, pickle_file_name)
            self.update_scoreboard() # update round points
            self.display_states("after play")   # display records at the end of each round
            # print('---------------------------------handsHistory --------------------\n', handsHistory)

        # annull game if trump is not revealed in entire game
        if self.trumpRevealed == False:
            self.is_annulled = True

        # game winner
        # print('---------------------------------teams --------------------\n', self.teams)
        if self.teams[BID_WINNER.team]['won'] >= self.teams[BID_WINNER.team]['bid']:
            # bidding team won the game
            winning_team = BID_WINNER.team
        else:
            # bidding team lost the game
            winning_team = 'A' if BID_WINNER.team == 'B' else 'B'
        self.record({'winning_team': winning_team, 'bid_winner': BID_WINNER.team, 'bid_value': self.teams[BID_WINNER.team]['bid'], 'bid_history': bidHistory, 'hands_history': handsHistory, 'trump_suit': self.trumpSuit, 'is_annulled': self.is_annulled})
        return_value_of_game_state = {'win' : 1 if winning_team == self.team_to_monitor else 0, 'loss' : 0 if winning_team == self.team_to_monitor else 1, 'annuled': 1 if self.is_annulled else 0, 'bid':self.teams['A']['bid'] if BID_WINNER == self.team_to_monitor else 0, 'scored':self.teams[self.team_to_monitor]["won"], "response_time_avg_bid":self.teams[self.team_to_monitor]['players'][0].response_time_avg_bid, "response_time_avg_play":(self.teams[self.team_to_monitor]['players'][0].response_time_avg_play + self.teams[self.team_to_monitor]['players'][1].response_time_avg_play)/2, "response_time_avg_bid":(self.teams[self.team_to_monitor]['players'][0].response_time_avg_bid + self.teams[self.team_to_monitor]['players'][1].response_time_avg_bid)/2, "response_time_trump_set":(self.teams[self.team_to_monitor]['players'][0].response_time_trump_set + self.teams[self.team_to_monitor]['players'][1].response_time_trump_set)/2}
        print("\n\n ----------------------------------------------")
        print(f" game over team: A: {self.teams['A']} \n  B: {self.teams['B']}        ")
        print(f" Winning Team: Team \'{winning_team}\'         ")
        print("\n\n ----------------------------------------------")
        
        # resetting Game teams: bid, won
        self.teams["A"]["won"] = 0
        self.teams["A"]["bid"] = -1
        self.teams["B"]["won"] = 0
        self.teams["B"]["bid"] = -1

        # resetting Game trump
        self.trumpSuit = {"suit": None, "playerId": None, "revealed":False} # playerId is the player who revealed the trump at "hand" hand

        # resetting Game players
        p = [Player("A1", random_player = self.players[0].is_random_player, num_simulations = self.players[0].num_simulations), Player("B1", random_player= self.players[1].is_random_player, num_simulations = self.players[1].num_simulations), Player("A2", random_player= self.players[2].is_random_player, num_simulations = self.players[2].num_simulations), Player("B2", random_player= self.players[3].is_random_player, num_simulations = self.players[0].num_simulations)]
        self.players = p

        # deleting game data
        self.train_data = {'handsHistory': [], 'A1': {'set_trump': False, 'bid': -1, 'won': 0}, 'B1': {'set_trump': False, 'bid': -1, 'won': 0}, 'A2': {'set_trump': False, 'bid': -1, 'won': 0}, 'B2': {'set_trump': False, 'bid': -1, 'won': 0}}
        self.is_annulled = False
        self.trumpRevealed = False
        self.team_to_monitor = None
        self.round = 0
        self.hand = 0
        self.trumpSuit = {"suit": None, "playerId": None, "revealed":False} # playerId is the player who revealed the trump at "hand" hand
        self.teams = {"A": {"won": 0, "bid": -1, "players": [self.players[0], self.players[2]]}, "B": {"won": 0, "bid": -1, "players": [self.players[1], self.players[3]]}}
        
        del BID_WINNER
        del BID_RESULTS
        
        return(return_value_of_game_state)


if __name__ == "__main__":
    # players = [Player("A1", random_player=False, num_simulations=7000), Player("B1", random_player=False, num_simulations=700), Player("A2", random_player=False, num_simulations=7000), Player("B2", random_player=False, num_simulations=700)]
    # print('number of players', len(players))
    # play_n_games(commit_id, number_of_games, GamePlay, players, team_to_monitor='A')

    # players = [Player("A1", random_player=False, num_simulations=700), Player("B1", random_player=False, num_simulations=7000), Player("A2", random_player=False, num_simulations=700), Player("B2", random_player=False, num_simulations=7000)]
    # print('number of players', len(players))
    # play_n_games(commit_id, number_of_games, GamePlay, players, team_to_monitor='B')

    # players = [Player("A1", random_player=False, num_simulations=1000), Player("B1", random_player=True, num_simulations=1000), Player("A2", random_player=False, num_simulations=1000), Player("B2", random_player=True, num_simulations=1000)]
    # players = [Player("A1", random_player=False, num_simulations=1000), Player("B1", random_player=True, num_simulations=1000), Player("A2", random_player=False, num_simulations=1000), Player("B2", random_player=True, num_simulations=1000)]
    
    # Against Random
    # players = [Player("A1", random_player=False), Player("B1", random_player=True), Player("A2", random_player=False), Player("B2", random_player=True)]

    # reward threshold: python3 Play.py threshold_.001v.00001_10000iters 300 train_data.pkl >> test.out    : 48.667
    # players = [Player("A1", random_player=False, average_reward_threshold = 0.001), Player("B1", random_player=False, average_reward_threshold = 0.00001), Player("A2", random_player=False, average_reward_threshold = 0.00001), Player("B2", random_player=False, average_reward_threshold = 0.00001)]
    
    # A vs B : 44.667 - 48%
    # Discount factor: : python3 Play.py discount.3v.5 300 train_data.pkl > test.out    : 47.667
    # players = [Player("A1", random_player=False, average_reward_threshold = 0.0001, DISCOUNT_FACTOR=0.3), Player("B1", random_player=False, average_reward_threshold = 0.0001, DISCOUNT_FACTOR=0.5), Player("A2", random_player=False, average_reward_threshold = 0.0001, DISCOUNT_FACTOR=0.3), Player("B2", random_player=False, average_reward_threshold = 0.0001, DISCOUNT_FACTOR=0.5)]
    
    # Discount factor: : python3 Play.py discount.3v.7 300 train_data.pkl > test.out    : 44.0
    # players = [Player("A1", random_player=False, average_reward_threshold = 0.0001, DISCOUNT_FACTOR=0.3), Player("B1", random_player=False, average_reward_threshold = 0.0001, DISCOUNT_FACTOR=0.7), Player("A2", random_player=False, average_reward_threshold = 0.0001, DISCOUNT_FACTOR=0.3), Player("B2", random_player=False, average_reward_threshold = 0.0001, DISCOUNT_FACTOR=0.7)]

    # Against Self: python3 Play.py tree_vs_tree5.10000iters 300 train_data.pkl > test.out    : 44.0
    # players = [Player("A1", random_player=False, num_simulations=10000), Player("B1", random_player=False, num_simulations=10000), Player("A2", random_player=False, num_simulations=10000), Player("B2", random_player=False, num_simulations=10000)]

    # python3 Play.py UCB2_vs_UCB2_early_stop 500 train_data.pkl > test.out    : 48.2 : Early stopping is better
    players = [Player("A1", random_player=False, num_simulations=10000), Player("B1", random_player=False, num_simulations=10000), Player("A2", random_player=False, num_simulations=10000), Player("B2", random_player=False, num_simulations=10000)]
    

    print('number of players', len(players))
    play_n_games(commit_id, number_of_games, GamePlay, players, pickle_file, team_to_monitor='A')

    # players = [Player("A1", random_player=False, num_simulations=750, port="http://0.0.0.0:8002"), Player("B1", random_player=True, num_simulations=7000, port="http://0.0.0.0:8002"), Player("A2", random_player=False, num_simulations=750, port="http://0.0.0.0:8002"), Player("B2", random_player=True, num_simulations=7000, port="http://0.0.0.0:8002")]
    # print('number of players', len(players))
    # play_n_games(commit_id, number_of_games, GamePlay, players, team_to_monitor='A')

    # print('\n scores sent', scores)

"""
            Request data format:
            {
                "playerId": "A1", # own player id
                "playerIds": ["A1", "B1", "A2", "B2"],  # player ids in order
                "timeRemaining": 1200,
                "cards": ["JS", "TS", "KH", "9C"],      # own cards
                "bidHistory": [ ["A1", 16],             # bidding history in chronological order
                                ["B1",17], 
                                ["A1", 17], 
                                ["B1", 0], 
                                ["A2", 0], 
                                ["B2", 0]
                            ],
                "bidState": {
                    "defenderId": "A1",
                    "challengerId": "B1",
                    "defenderBid": 16,
                    "challengerBid": 17
                },
            }
        """
        

''' 
# todo:
    - Record data, free memory
    - bid neural networls
    - only 1500 ms for (bidding + playing) i.e. 1500ms for one whole game.
    - trumpReveal: if self.revealed_trump_in_this_trick: throwable_cards = any if friend_winning else winnin_trumps if winnin_trumps else trumps if trumps else any_card
    - implement bhoos parameters: timeRemaining, see for others
    - bid in anti-clockwise order?
    - tests
    - bhoos ask: remove "bid_history" for request_trump?
    
# done:
    - fix score: random vs game tree
    - num_simulations from Play
    - annulled game:
        - trump not revealed by the end of the game
        - any player has all 4 jacks among 8 cards dealt
        - a team does not has any trump card in entire game
    - store scores in a csv file
    - response_time_avg
    - update_round_points function : team["cards"] -> team["won"]
    - Add players to team A:{"players": ["A1", "A2"]}
    - game stopping criteria : |teams["A"]["round_points"]| >= 6 or |teams["B"]["round_points"]| >= 6
    - Display winner
    - hide trump card before trump reveal for non bid_winners
    - update round wins
    - at the end of each round :: update round points and reset bid, won
    - update team bit points after bid :: not needed (bid winners bid is updated) other team's bid is -1 and unchanged
    - reset Game (teams: bid, won), (trump), (players)
    - trumpSuit
    - self.trumpRevealed
    - teams['bid_value'] -> teams['bid']
    - teams['points'] -> teams['won']
    - removed Game.trump["hand"]

    - throw card logic, trump suit logic
    - only allow bid higher than previous bid
    - give bhoos_format_data: bidHistory data while bidding/playying
    - check if player can reveal trump

    - assert/test: challenger raise, defender match
    - reveal trump
    - handsHistory in request_play_card
    - redundant (challenger variable, player.bid_role = "challenger")
    - update bid roles: challenger/defender
    - T for 10


# todo optional:
    - marrige rule
    - one player mode

# bhoos rules :
- first player bids 16

'''