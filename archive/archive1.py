# bid pseudocode
players = ['p1', 'p2', 'p3', 'p4']
defender = p0
challenger = p0
defender.bid_value = 16

while(1):
    bid = ask_bid(defender)    # validates bid
    if bid == 28:
        return {'bid_winner': defender, 'bid_value': bid}
    elif bid == None:
        # defender passed, challenger is now defender
        players.remove(defender)
        defender = challenger
        if len(players) > 1:
            # not last man standing
            challenger = players.next()
        else:
            # last man standing -> bid winner 
            return {'bid_winner': challenger, 'bid_value': bid}
    
    # defender :: valid bid (not pass)
    bid = ask_bid(challenger)    # validates bid
    if bid == 28:
        return {'bid_winner': challenger, 'bid_value': bid}
    elif bid == None:
        # challenger passed
        players.remove(challenger)
        if len(players) > 1:
            # not last man standing
            challenger = players.next()
        else:
            # last man standing -> bid winner 
            return {'bid_winner': defender, 'bid_value': bid}


biddingPlayers = [player for player in self.players]

# ---------------------------------------
# implementation of ask_bid
# ---------------------------------------
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
            bid = self.request_bid(biddingPlayers[0], bidHistory, bidState)   # request_bid also validates bid
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
                
                bid = self.request_bid(biddingPlayers[1], bidHistory, bidState) # request_bid also validates bid
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
def play_logic():
    played = [] # cards at table
    trumpRevealed = False   # or trumpSuit
    # False if not self.trump["revealed"] else {
    #     "hand": self.trump["hand"],            # represents the hand at which the trump was revealed
    #     "playerId": self.trump["playerId"],     # the player who revealed the trump
    # },



    
    trumpSuit = False       # bhoos data compatibility (otherwise would use None)
    # trumpSuit = trumpSuit     # defined earlier
    handsHistory = []   # stores the history of hands/tricks played [initial_player, [cards_played], trick_winner ]

    ordered_players = players[bid_winner:] + players[:bid_winner]
    trick_winner = ordered_players[0]
    for i in range(8):
        # 8 tricks in one round
        # throw card logic
        played = []
        for player in ordered_players:
             # request_play_card(self, player, bidHistory, handsHistory, played, trumpSuite)
            card_played = self.request_play_card(player, bidHistory, handsHistory, played, trumpRevealed, trumpSuit if trumpRevealed else False, hand)
            if "revealTrump" in card_played.keys() and card_played["revealTrump"] == True:
                # player request for trump reveal :: player_can-> asserted from request_play_card function
                # player asked for reveal trump
                trumpRevealed = {
                    "hand": i,                 # represents the hand/trick at which the trump was revealed
                    "playerId": player.id,     # the player who revealed the trump
                }
                
                # request for throw card after trump reveal
                card_played = self.request_play_card(player, bidHistory, handsHistory, played, trumpRevealed, trumpSuit if trumpRevealed else False, hand)
            
            played.append(card_played)
        trick_winner_index = self.calculate_winner_index(played.copy(), trumpSuit if trumpRevealed else False)
        handsHistory.append([ordered_players[trick_winner_index], played, trick_winner])
        ordered_players = ordered_players[trick_winner_index:] + ordered_players[:trick_winner_index]
        self.update_trick_points(played, trumpSuit if trumpRevealed else False, players)    # update wins for teams


def update_trick_points(self, played, trump_suite, players):
    def trick_winner_index(played, trump_suite) -> int:
        # returns the index of the winner
        # trump sute is None if trump is not revealed
        if (trump_suite != False) and (trump_suite in [card.suit for card in played]):
            # trump is revealed
            # and trump in played
            # largest trump wins
            trump_cards = [card for card in played if card.suit == trump_suite]
            winner_index = played.index(max(trump_cards))
        else:
            # either trump is not revealed
            # or trump is not in played
            # largest of initial suit wins
            initial_suite_cards = [card for card in played if card.suit == played[0].suit]
            winner_index = played.index(max(initial_suite_cards))
        return winner_index
    
    winner_index = trick_winner_index(played, trump_suite)
    trick_winner = players[winner_index]
    
    # sum of points at end of each trick
    trick_winner_points = sum([CARD_WEIGHTS[card.rank] for card in played if card.rank in CARD_WEIGHTS.keys()])
    self.teams[trick_winner.team]["won"] += trick_winner_points

def update_scoreboard(self):
    # team either looses (decrease round_points) or wins (increase round_points)
    bid_winning_team = "A" if self.teams["A"]["bid"] > self.teams["B"]["bid"] else "B"
    
    if self.teams[bid_winning_team]["won"] >= self.teams[bid_winning_team]["bid"]:
        # bid winning team has scored gte bid value
        self.teams[bid_winning_team]["round_points"] += 1   # bid winning team scores gte what they bid
    else:
        self.teams[bid_winning_team]["round_points"] -= 1   # bid winning team scores lte what they bid

self.play_logic()
self.update_scoreboard() # update round points
self.display_states("after play")   # display records at the end of each round

# resetting Dealers teams: bid, won
self.teams["A"]["won"] = 0
self.teams["A"]["bid"] = -1
self.teams["B"]["won"] = 0
self.teams["B"]["bid"] = -1

# resetting Dealers trump
self.trump = {"suit": None, "playerId": None, "revealed":False} # playerId is the player who revealed the trump at "hand" hand

# resetting Dealers players
self.players = [Player("A1", random_player=True), Player("B1", random_player=True), Player("A2", random_player=True), Player("B2", random_player=True)]

