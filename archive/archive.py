# ----------------------------
# problem 2
# ----------------------------
# calculateWinnerIndex not working as expected
from game_of_29.utils import Card
c=['JD', 'KD', 'TD', '8D']
cards = [Card(t[1], t[0]) for t in c]
Card.display('',cards)      # , cards: ['JD', 'KD', 'TD', '8D']
Card.calculateWinnerIndex(cards, 'H')   # gives 3, should have been 0

# ----------------------------
# problem 1
# ----------------------------
# to find order of players given pre-filled cards at table
# e.g.1 ::  given
cards_at_table = ['2H', '6D']
player_indexes = [0,1,2,3]
player_index = 1
# required output
order = [1, 2]

# e.g.2 ::  given
cards_at_table = ['1k', 'AD']
player_ids = [0,1,2,3]
player_index = 3
# required output
order = [3, 0]

# -------- code -------- 
def calculate_order(len_cards_at_table, player_index):
    ordered_players = []
    for i in range(0,4 - len_cards_at_table):
        ordered_players.append((i + player_index)%4)

    return ordered_players_indexes

<below: wrong problem defination below>
# e.g.1
# given
cards_at_table = ['2H', '6D']
player_ids = [0,1,2,3]
player_id = 1
# required output
order = [3, 0, 1, 2]

# e.g.2
# given
cards_at_table = ['6D']
player_ids = [0,1,2,3]
player_id = 3
# required output
order = [2, 3, 0, 1]

def calculate_order(len_cards_at_table, player_id):
    # right solution for wrong problem defination
    ordered_player_ids = [player_id]
    # pre: insert players before players index
    [ordered_player_ids.insert(0, (player_id - (i+1)) % 4) for i in range(len_cards_at_table)]
    # post: insert players after players index
    ordered_player_ids += [i%4 for i in range(player_id + 1, 5 - len(ordered_player_ids) + player_id)]
    return {"ordered_player_ids": ordered_player_ids[-4:]}

def calculate_order(self, len_cards_at_table, player_id):
        ordered_player_ids = [player_id]
        # pre: insert players before players index
        [ordered_player_ids.insert(0, (player_id - (i+1)) % 4) for i in range(len_cards_at_table)]
        # post: insert players after players index
        ordered_player_ids += [i%4 for i in range(player_id + 1, 5 - len(ordered_player_ids) + player_id)]
        return ordered_player_ids
        # return {"ordered_player_ids": ordered_player_ids[-4:]}

def v2_calculate_pre_order(pid, len_at_table):
    # other players before player
    n=len_at_table
    return [i%4 for i in range(pid + 1, pid+4 + (4-n) )]



# logic
'''
# other players before player
# we'll insert to 0 index so range is reversed
# range(a,b) -> range(a, b%4) if b < 0?
# what about range(2,1)?
len(cards_at_table)   player_id    req range            req. output
    2                    1           (2, 7)          [i % 4 for i in range(2, 3)] = [3, 0, 1]
    3                    1           (2,6)                 [i % 4 for i in range(2, 6)] = [2, 3, 0, 1]
    1                    3           (4,7)                 [2, 3]
    0                    3                                 [3]
    n                    pid         (pid + 1, pid+4 + (4-n) )

# other players after player
len(cards_at_table)   player_id    req range    req. output
    2                    1           (2,4) 
    3                    1           (2,3)
    1                    3           (4,7)
    n                    pid         (pid + 1, pid+1 + (4-n) )
'''

ordered_player_ids

# test
calculate_order(2,1)    # {'ordered_player_ids': [3, 0, 1, 2]}
calculate_order(3,1)    # {'ordered_player_ids': [2, 3, 0, 1]}
calculate_order(1,3)    # {'ordered_player_ids': [2, 3, 0, 1]}
calculate_order(0,3)    # {'ordered_player_ids': [3, 0, 1, 2]}


