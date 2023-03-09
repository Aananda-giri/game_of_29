Two player game
all_cards = ['a','b', 'c', 'd', 'e', 'f', 'g', 'h']
all_ranks = [1, 2, 3, 4, 5, 6, 7, 8]

player a gets two random all_cards
player b gets remaining 6 cards
first thrower has an advantage of 0.5 * rank of card
winner  gets to throw first

how can we solve this game?


import random

def simulate_game(all_cards, all_ranks, a_cards, b_cards, first_thrower):
    current_thrower = first_thrower
    while len(a_cards) > 0 and len(b_cards) > 0:
        if current_thrower == "a":
            card = random.choice(a_cards)
            a_cards.remove(card)
            rank = all_ranks[all_cards.index(card)]
        else:
            card = random.choice(b_cards)
            b_cards.remove(card)
            rank = all_ranks[all_cards.index(card)]

        if rank > max(all_ranks[all_cards.index(c) for c in a_cards + b_cards]):
            current_thrower = "a" if current_thrower == "b" else "b"

    return "a" if len(a_cards) > 0 else "b"

def solve_game(all_cards, all_ranks, a_cards, b_cards, first_thrower):
    n = 1000 # number of simulations
    win_counts = {card: 0 for card in a_cards}
    for i in range(n):
        random.shuffle(a_cards)
        winner = simulate_game(all_cards, all_ranks, a_cards.copy(), b_cards.copy(), first_thrower)
        if winner == "a":
            win_counts[a_cards[0]] += 1

    best_card = max(a_cards, key=lambda card: win_counts[card] / n + 0.5 * all_ranks[all_cards.index(card)])
    return best_card

all_cards = ['a','b', 'c', 'd', 'e', 'f', 'g', 'h']
all_ranks = [1, 2, 3, 4, 5, 6, 7, 8]
random.shuffle(all_cards)
a_cards = all_cards[:2]
b_cards = all_cards[2:]
first_thrower = "a"
best_card = solve_game(all_cards, all_ranks, a_cards, b_cards, first_thrower)
print("Best card:", best_card)