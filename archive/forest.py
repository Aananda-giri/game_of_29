import itertools
'''

- (if trump_suit) ignore suit different than trump suit
- (else) ignore suit different from initial cards suit

'''

class Table:
    def encode(self, cards, trump):
        # encoding
        if trump == None:
            # no trump : ignore cards of suit different from first cards suit
            return [card for card in cards if card.suit == cards[0].suit]
        else:
            # trump : ignore cards of suit different from trump suit
            return [str(card) for card in cards if card.suit == trump]
    def expand(self, cards):
        # ranks = [i for i in range(1, 9)]
        # conbination of cards
        # cards = [str(card) for card in range(1,4)]
        print(cards)
        combination = [list(i) for i in itertools.combinations(cards, 2)]
        print('combinatio:', combination)
        variants = []
        for trick in combination[1:]:
            # rotate trick left
            # rotated = trick[1:] + trick[:1]
            variants.append(trick[1:] + trick[:1])
            variants.append(trick[2:] + trick[:2])
            # variants.append(trick[3:] + trick[:3])
            # variants.append(trick[4:] + trick[:4])
        print('variants', variants)
        # return variants
Table.expand([i for i in range(1,4)])