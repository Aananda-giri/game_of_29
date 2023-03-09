import random, requests, time, traceback
from utils import Card
import os
from dotenv import load_dotenv
load_dotenv()

class Player:
    def __init__(self, player_id, random_player=True, port="http://0.0.0.0:8001", num_simulations=650, average_reward_threshold = None, DISCOUNT_FACTOR = os.environ.get('DISCOUNT_FACTOR', 0.3)):
        # print(f"\n\n player_discount_factor: {DISCOUNT_FACTOR}  {os.environ.get('DISCOUNT_FACTOR')}\n\n")
        self.id = player_id     # playerIds = ["A1", "B1", "A2", "B2"]
        self.player_index = ["A1", "B1", "A2", "B2"].index(player_id)
        self.team = self.id[0]
        self.is_random_player = random_player
        self.port = port                    # port number of the player
        self.timeRemaining = 15000          # 1500ms in actual game <python is 10* slower than c++>
        self.num_simulations = num_simulations
        self.average_reward_threshold = average_reward_threshold
        self.DISCOUNT_FACTOR = DISCOUNT_FACTOR
        # print(f'\n\n average_reward_threshold\n\n {average_reward_threshold}')
        # for statistics
        self.times_bid = 0
        self.times_play = 0
        self.response_time_avg_bid = 0      # total response time for bid
        self.response_time_avg_play = 0     # total response time for play
        self.response_time_trump_set = 0     # response time for trump set

        # to update later
        self.bid_value = -1   # bid are initialized to None, zero if player passes
        self.cards = []
        
        
    def __str__(self):
        return self.id
        
    def request_bid(self, bidHistory, bidState) -> int:
        # return int(input(f'please enter bid value:  {player.id}'))
        if self.is_random_player:
            # bid randomly
            print(f"got_bidState:{bidState}")
            if self.id == bidState['challengerId']:  # challenger
                if bidState["defenderId"] == bidState['challengerId']:
                    # initial bid against oneself
                    bid_value = 0   # pass and stay with 16
                else:
                    # player is challenger :: has to bid higher than defender
                    bid_value = random.choice([0, bidState["defenderBid"] + 1])   # randomly choose between 0 (pass) and higher than defender bid
            else:
                # player is defender :: has to bid equal or higher than challenger
                # assert: challenger raise the bid, defender match the bid
                bid_value = random.choice([0, bidState["challengerBid"]])   # randomly choose between 0 (pass) and higher than defender bid
        else:
            # time at requesting bid/play
            start_time = time.time()

            request_payload = {
                "playerId": self.id, # own player id
                "playerIds": ["A1", "B1", "A2", "B2"],  # player ids in order
                "timeRemaining": self.timeRemaining,
                "cards": [str(card) for card in self.cards],      # own cards
                "bidHistory": bidHistory.copy(),    # bid history
                "bidState": bidState,
            }
            # print('----------------------------------------------')
            # print(f'\n\n {request_payload} \n\n')
            # print('----------------------------------------------')
            response = requests.post(self.port + "/bid", json=request_payload).json()
            
            
            # update response time
            response_time = (time.time() - start_time) * 1000
            if self.times_bid > 0:
                self.response_time_avg_bid += (self.response_time_avg_bid * self.times_bid + response_time)/self.times_bid
            else:
                self.response_time_avg_bid = response_time
            self.times_bid += 1
            
            # substract time required for bidding
            self.timeRemaining  -= response_time
            assert self.timeRemaining > 0, f"request_bid : time remaining is less than 0 :: {self.timeRemaining}"
            
            assert type(response["bid"]) == int, f"bid value is not an integer : {bid_value}"
            if self.id == bidState['challengerId']:
                # assert: challenger raise the bid, defender match the bid
                if bidState["defenderId"] != bidState['challengerId'] and response["bid"] > 0:
                    assert response["bid"] > bidState["defenderBid"], f"Challenger bid value {response['bid']} is not greater than defender bid : {bidState['defenderBid']} request:{request_payload}"
            else:
                # assert: challenger raise the bid, defender match the bid
                assert (response["bid"] == 0) or (response["bid"] >= bidState["challengerBid"]), f"Defender bid value {response['bid']} is less than challenger bid : {bidState['challengerBid']}"
            # if response["bid"] == 0:
            bid_value = response["bid"]
            # requests.post(player.port + "/bid", json={"bid_value": player.bid_value})
        return bid_value


    
    def request_trump_set(self, bidHistory):
        # response : 
        if self.is_random_player:
            return random.choice(Card.SUITS)
        
        # time at requesting bid/play
        start_time = time.time()

        request_payload = {
            "playerId": self.id,                    # own player id
            "playerIds": ["A1", "B1", "A2", "B2"],  # player ids in order
            "timeRemaining": self.timeRemaining,
            "cards": [str(card) for card in self.cards],                    # own cards
            "bidHistory": bidHistory.copy(),        # bid history
        }
        request_payload = {
            "playerId":"-idya5Bo",
            "playerIds":["Bot 0","-idya5Bo","Bot 1","Kw5JghXi"],
            "cards":["JH","9C","1S","JC","9S","QS","8S"],
            "timeRemaining":1345.553759,
            "bidHistory":[["-idya5Bo",16],["Bot 1",17],["-idya5Bo",0],["Kw5JghXi",0],["Bot 0",0]],
            "played":["8D","QD"],
            "teams":[{"players":["Bot 0","Bot 1"],"bid":17,"won":0},{"players":["-idya5Bo","Kw5JghXi"],"bid":0,"won":0}],
            "handsHistory":[["-idya5Bo",["7C","8C","QC","KS"],"Kw5JghXi"]],
            "trumpSuit":"D","trumpRevealed":{"hand":2,"playerId":"-idya5Bo"}
        }

        # print('----------------------------------------------')
        # print(f'\n\nTrump Set: {request_payload} \n\n')
        # print('----------------------------------------------')
        response = requests.post(self.port + "/chooseTrump", json=request_payload).json()
        
        # update response time
        response_time = (time.time() - start_time) * 1000
        self.response_time_trump_set = response_time
        
        # substract time used for trump_set
        self.timeRemaining  -= (time.time() - start_time) * 1000
        assert self.timeRemaining > 0, f"trump_set : time remaining is less than 0 :: {self.timeRemaining}"
        
        # self.trump = {"suit": response["suit"], "playerId": player.id, "hand": 0}
        assert response["suit"] in Card.SUITS, f"Trump is not  of  a valid suit :" +  str(response)
        return response["suit"]

    def request_play_card(self, bidHistory, handsHistory, played, trumpRevealed, trumpSuit, teams, did_reveal_trump_in_this_trick):
        # returns a card :: response = {"card": "1H"}
        # may ask for revealTrump :: response = {"revealTrump": True}
        # did_reveal_trump_in_this_trick = trumpRevealed and trumpRevealed["playerId"] == self.id and trumpRevealed["hand"] == (len(handsHistory) + 1)

        throwable_cards = Card.throwableCards(self.cards, played, did_reveal_trump_in_this_trick, trumpSuit)
        print(f"\n\nthrowable_cards {Card.display(None, throwable_cards, True)}\n played:{played}")

        self.has_set_trump = max(bidHistory, key = lambda x:x[1])[0] == self.id
        print('\nplayed', played)
        if self.is_random_player:
            if Card.canRevealTrump(self.cards, played) and trumpRevealed == False:
                # trump not revealed and player can reveal it
                if random.randint(0, 1) == 0:
                    # randomly choose to reveal trump
                    return {"revealTrump": True}
                    # self.trump["playerId"] = self.id
                    # self.trump["hand"] = hand
            return {"card" : random.choice(throwable_cards)}    # throw a random throwable card

        
        # time at requesting bid/play
        start_time = time.time()
        print(f'\n\n api_discount_factor: {self.DISCOUNT_FACTOR} \n\n')
        request_payload = {
            "playerId": self.id, # own player id
            "playerIds": ["A1", "B1", "A2", "B2"],                  # player ids in order
            "timeRemaining": self.timeRemaining,
            "teams": [
                { "players": ["A1", "A2"], "bid": teams["A"]["bid"], "won": teams["A"]["won"] },   # first team information
                { "players": ["B1", "B2"], "bid": teams["B"]["bid"], "won": teams["B"]["won"] },    # second team information
            ],
            "cards": [str(card) for card in self.cards],    # own cards
            "bidHistory": bidHistory.copy(),    # bid history
            "played": [str(card) for card in played],    # cards played in the current trick
            "handsHistory": [[str(history[0])] + [[str(card) for card in history[1]]] + [str(history[-1])] for history in handsHistory],    # hands history
        
        # represents the suit if available, the trumpSuit is only present for the player who reveals the trump
        # after the trump is revealed, the trumpSuit is present for all the players
        "trumpSuit": trumpSuit if trumpRevealed or self.has_set_trump else False,
        # self.trump["suit"] if self.trump["revealed"] else False,
        # only after the trump is revealed by the player the information is revealed
        "trumpRevealed": trumpRevealed,
        # False if not self.trump["revealed"] else {
        #     # "hand": self.trump["hand"],            # represents the hand at which the trump was revealed
        #     "playerId": self.trump["playerId"],     # the player who revealed the trump
        # },
        "average_reward_threshold": self.average_reward_threshold,  # For early stopping during simulation
        "discount_factor": self.DISCOUNT_FACTOR, # discount factor for future rewards while simulation
        }
        
        # print('----------------------------------------------')
        # print(f'\n\n Play Card: {request_payload} \n\n')
        # print('----------------------------------------------')
        response = requests.post(self.port + "/play", json=request_payload).json()
        
        # update response time
        response_time = (time.time() - start_time) * 1000
        if self.times_play > 0:
            self.response_time_avg_play += (self.response_time_avg_play * self.times_play + response_time)/self.times_play
        else:
            self.response_time_avg_play = response_time
        self.times_play += 1
        
        # substract time required for playing
        self.timeRemaining  -= response_time
        assert self.timeRemaining > 0, f"request_play : time remaining is less than 0 :: {self.timeRemaining}"
        
        if "card" in response.keys():
                # player threw a cards
                print(f'\n-------- got {self.id}response: {response} response["card"] : {response["card"]}\n')
                response["card"] = Card(response["card"][1], response["card"][0])
                assert response["card"] in throwable_cards, f"Expected : {str([str(card) for card in throwable_cards])} got:{response['card']}" + "payload:" +  str(self.get_play_payload(bidHistory, handsHistory, played, trumpRevealed, trumpSuit if trumpRevealed else False, teams, False))
        else:
                # player asked for reveal trump
                assert Card.canRevealTrump(self.cards, played), f"player can\'t reveal trump :response:{response} played:{[str(card) for card in played]} player_cards:{[str(card) for card in self.cards]}"
                assert trumpRevealed == False, f"trump already revealed : {trumpRevealed}"
                assert response["revealTrump"] == True, f"reveal trump is not a True, should have thrown a card. response: {response}"
        
        # if 'revealTrump' in response.keys() or response["revealTrump"] == False:
        #     request_payload[]
        #     save_json(request_payload, 'play_data.pkl')
        return response
    
    def get_play_payload(self, bidHistory, handsHistory, played, trumpRevealed, trumpSuit, teams, did_reveal_trump_in_this_trick, discount_factor=os.environ.get('DISCOUNT_FACTOR')):
        print(f'\n-------------- playerId:{self} -----------------\n')
        request_payload = {
            "playerId": self.id, # own player id
            "playerIds": ["A1", "B1", "A2", "B2"],                  # player ids in order
            "timeRemaining": self.timeRemaining,
            "teams": [
                { "players": ["A1", "A2"], "bid": teams["A"]["bid"], "won": teams["A"]["won"] },   # first team information
                { "players": ["B1", "B2"], "bid": teams["B"]["bid"], "won": teams["B"]["won"] },    # second team information
            ],
            "cards": [str(card) for card in self.cards],    # own cards
            "bidHistory": bidHistory.copy(),    # bid history
            "played": [str(card) for card in played],    # cards played in the current trick
            "handsHistory": [[str(history[0])] + [[str(card) for card in history[1]]] + [str(history[-1])] for history in handsHistory],    # hands history
        
        # represents the suit if available, the trumpSuit is only present for the player who reveals the trump
        # after the trump is revealed, the trumpSuit is present for all the players
        "trumpSuit": trumpSuit if trumpRevealed else False,
        # self.trump["suit"] if self.trump["revealed"] else False,
        # only after the trump is revealed by the player the information is revealed
        "trumpRevealed": trumpRevealed,
        # False if not self.trump["revealed"] else {
        #     # "hand": self.trump["hand"],            # represents the hand at which the trump was revealed
        #     "playerId": self.trump["playerId"],     # the player who revealed the trump
        # },
        "average_reward_threshold": self.average_reward_threshold,  # For early stopping during simulation
        "discount_factor": self.DISCOUNT_FACTOR, # discount factor for future rewards while simulation
        }
        return request_payload

    def has_all_jacks(self):
        all_ranks = [card.rank for card in self.cards]
        if all_ranks.count('J') == 4:
            return True
    
    '''
    # todo:
        - replace is_random_player with random external player 
    
    # done:
        - remove Game.trump and Player.trump
      
    '''
