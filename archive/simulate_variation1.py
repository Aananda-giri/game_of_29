def simulate_node(self, DISCOUNT_FACTOR):
        # print(f"\n ------throw_one_{self.player_index}:@_hands------- {[str(card) for card in self.cards]} @table {[str(card) for card in self.cards_at_table]} @not_played {[str(card) for card in self.cards_not_played]}")
        def append_one_card_at_table(self, player_id, cards_at_hand, cards_at_table, trump_suit, trump_revealed, possible_trumps):
            # if len(cards_at_hand) == 1:
            #     cards_at_table.append(cards_at_hand[0])
            #     cards_at_hand = []
            #     # return cards_at_hand[0]
            # print(f"\n ------throw_one_{self.player_index}:{player_id} @_hands------- {[str(card) for card in cards_at_hand]} @table {[str(card) for card in cards_at_table]}")
            if player_id == self.player_index:
                if not trump_revealed:
                    # trump not revealed
                    cant_follow_suit = cards_at_table[0].suit not in [card.suit for card in cards_at_hand] if len(cards_at_table) > 0 else False
                    if cant_follow_suit:
                    # if random.random() < Card.get_random_trump_reveal_probability():
                        trump_suit = random.choice(possible_trumps)
                        trump_revealed = True

                # players turn to throw
                throwable_cards = Card.throwableCards(cards_at_hand, cards_at_table, trump_suit = trump_suit)
                # print(f"\n ------throwable @_hands------- {[str(card) for card in cards_at_hand]} @table {[str(card) for card in cards_at_table]} : {[str(card) for card in throwable_cards]}")
                random_card_thrown = random.choice(throwable_cards)
                cards_at_hand.remove(random_card_thrown)
                cards_at_table.append(random_card_thrown)
            else:
                # opponents (other players) turn to throw
                if not trump_revealed:
                    # randomly initialize trump: set or not set by player
                    # trump not revealed
                    cant_follow_suit = cards_at_table[0].suit not in [card.suit for card in cards_not_played] if len(cards_at_table) > 0 else False
                    if cant_follow_suit or random.random() < Card.get_random_trump_reveal_probability():
                        if not trump_revealed:
                            trump_suit = random.choice(possible_trumps)
                            trump_revealed = True

                
                
                
                throwable_cards = Card.throwableCards(cards_not_played, cards_at_table, trump_suit = trump_suit)
                # print(f'\n-------- throwable_cards: {[str(card) for card in throwable_cards]}')
                random_card_thrown = random.choice(throwable_cards)
                cards_not_played.remove(random_card_thrown)
                cards_at_table.append(random_card_thrown)
            return (cards_at_table, cards_at_hand, cards_not_played, trump_suit, trump_revealed)

        cards_at_table = self.cards_at_table.copy()
        cards_at_hand = self.cards.copy()
        cards_not_played = self.cards_not_played.copy()
        
        wins = 0
        

        if not self.trump_suit:
            possible_trumps = ['c', 'D', 'H', 'S']  # None : by default
        else:
            possible_trumps = [self.trump_suit] # trump set by user and not revealed yet
        trump_suit = self.trump_suit if self.trump_suit else None
        trump_revealed = self.trump_revealed
        
        # ordered players :: reference/analysis: archive.py problem 1
        # card already thrown by player, yet to append to table
        ordered_player_ids = (self.calculate_order(len(cards_at_table), self.player_index))
        
        # loop order because some players may have already thrown cards at first trick
        loop_order = ordered_player_ids[ordered_player_ids.index(self.player_index):]

        # player_index = ordered_player_ids.index[self.player_index]
        # print(f'\n\nordered player id : {ordered_player_ids}')
        # print(f'before_player_cards:{len(cards_at_hand)}, other_cards:{len(cards_not_played)}')
        initial_len_cards_at_hand = len(cards_at_hand)
        while len(cards_at_hand) > 0:
            # print(f'after_player_cards:{len(cards_at_hand)}, other_cards:{len(cards_not_played)}')
            # player throw 1 card
            while len(cards_at_table) < 4:
                for player_id in loop_order:
                    cards_at_table, cards_at_hand, cards_not_played, trump_suit, trump_revealed = append_one_card_at_table(self, player_id, cards_at_hand, cards_at_table, trump_suit, trump_revealed, possible_trumps)
            ## check if player wins
            winner_index, win_score = Card.calculateWinnerIndex(cards_at_table, trump_suit, trump_revealed, show_win_score=True)
            # print(f"\n\n-------- winner_index:{winner_index} ordered_player_ids:{ordered_player_ids} player_index:{self.player_index} at_table:{[str(card) for card in cards_at_table]} trump:{self.trump_suit}")
            cards_at_table = [] # clear cards at table
            # print(f'ordered ids: {ordered_player_ids}, player_index:{self.player_index}')
            # Card.display('@table', cards_at_table)
            # print(f'winner index: {winner_index}')
            # print('winner_index:', winner_index)
            
            if ordered_player_ids[winner_index] == self.player_index:   # or ordered_player_ids[(winner_index+2)%4] == self.player_index:
                # player's team won
                # print('player team won')
                wins += win_score * (1 - float(DISCOUNT_FACTOR)) ** (initial_len_cards_at_hand - len(cards_at_hand) - 1)
            # else:
            #     # print('player team lost')
            #     wins -= win_score
            # update ordered player
            ordered_player_ids = PLAYER_IDS[ordered_player_ids[winner_index]:] + PLAYER_IDS[:ordered_player_ids[winner_index]]
            loop_order = ordered_player_ids
        return wins