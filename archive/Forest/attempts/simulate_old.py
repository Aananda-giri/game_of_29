def simulate_node(self):
        # print(f"\n ------throw_one_{self.player_index}:@_hands------- {[str(card) for card in self.cards]} @table {[str(card) for card in self.cards_at_table]} @not_played {[str(card) for card in self.cards_not_played]}")
        def append_one_card_at_table(self, player_id, cards_at_hand, cards_at_table):
            # if len(cards_at_hand) == 1:
            #     cards_at_table.append(cards_at_hand[0])
            #     cards_at_hand = []
            #     # return cards_at_hand[0]
            # print(f"\n ------throw_one_{self.player_index}:{player_id} @_hands------- {[str(card) for card in cards_at_hand]} @table {[str(card) for card in cards_at_table]}")
            if player_id == self.player_index:
                # players turn to throw
                throwable_cards = Card.throwableCards(cards_at_hand, cards_at_table)
                # print(f"\n ------throwable @_hands------- {[str(card) for card in cards_at_hand]} @table {[str(card) for card in cards_at_table]} : {[str(card) for card in throwable_cards]}")
                random_card_thrown = random.choice(throwable_cards)
                cards_at_hand.remove(random_card_thrown)
                cards_at_table.append(random_card_thrown)
            else:
                # opponent (other players) turn to throw
                throwable_cards = Card.throwableCards(cards_not_played, cards_at_table)
                # print(f'\n-------- throwable_cards: {[str(card) for card in throwable_cards]}')
                random_card_thrown = random.choice(throwable_cards)
                cards_not_played.remove(random_card_thrown)
                cards_at_table.append(random_card_thrown)
            return (cards_at_table, cards_at_hand, cards_not_played)

        cards_at_table = self.cards_at_table.copy()
        cards_at_hand = self.cards.copy()
        cards_not_played = self.cards_not_played.copy()
        
        wins = 0
        
        # ordered players :: reference/analysis: archive.py problem 1
        # card already thrown by player, yet to append to table
        ordered_player_ids = (self.calculate_order(len(cards_at_table), self.player_index))
        first_simulation = True
        while len(cards_at_hand) > 0:
            
            # trump not set
            if not self.trump_suit:
                # randomly initialize trump
                if random.random() < RANDOM_TRUMP_INITIALIZATION_PROBABILITY:
                    self.trump_suit = random.choice(Card.SUITS)

            # player_index = ordered_player_ids.index[self.player_index]
            # print(f'\n\nordered player id : {ordered_player_ids}')
            # print(f'before_player_cards:{len(cards_at_hand)}, other_cards:{len(cards_not_played)}')
            if first_simulation:
                first_simulation = False
                for player_id in ordered_player_ids[ordered_player_ids.index(self.player_index):]:
                    if first_simulation:
                        # first card of simulate node : node have already choosen card to throw
                        
                        first_simulation = False
                        cards_at_table.append(self.card_thrown)
                        cards_at_hand.remove(self.card_thrown)  # already removed in expand_node?
                        break
                    else:
                        cards_at_table, cards_at_hand, cards_not_played = append_one_card_at_table(self, player_id, cards_at_hand, cards_at_table)
            else:
                # print(f'after_player_cards:{len(cards_at_hand)}, other_cards:{len(cards_not_played)}')
                for player_id in ordered_player_ids:
                    cards_at_table, cards_at_hand, cards_not_played = append_one_card_at_table(self, player_id, cards_at_hand, cards_at_table)
            ## check if player wins
            winner_index, win_score = Card.calculateWinnerIndex(cards_at_table, self.trump_suit, show_win_score=True)
            # print(f"\n\n-------- winner_index:{winner_index} ordered_player_ids:{ordered_player_ids} player_index:{self.player_index} at_table:{[str(card) for card in cards_at_table]} trump:{self.trump_suit}")
            cards_at_table = [] # clear cards at table
            # print(f'ordered ids: {ordered_player_ids}, player_index:{self.player_index}')
            # Card.display('@table', cards_at_table)
            # print(f'winner index: {winner_index}')
            # print('winner_index:', winner_index)
            
            if ordered_player_ids[winner_index] == self.player_index or ordered_player_ids[(winner_index+2)%4] == self.player_index:
                # player's team won
                # print('player team won')
                wins += win_score
            # else:
            #     # print('player team lost')
            #     wins -= win_score
            # update ordered player
            ordered_player_ids = PLAYER_IDS[ordered_player_ids[winner_index]:] + PLAYER_IDS[:ordered_player_ids[winner_index]]
        return wins