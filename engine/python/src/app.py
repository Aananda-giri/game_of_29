import os, time

# load contents from .env file
from dotenv import load_dotenv
load_dotenv()

from sanic import Sanic
from sanic.response import json
from sanic.request import Request
from sanic_cors import CORS

from bot import get_bid, get_trump_suit, get_play_card
from game_tree2 import bhoos_compatible_play as mcts_test


# to disable debug mode, set DEBUG=0 in .env file, otherwise debug mode is enabled by default as DEBUG=1
DEBUG = os.getenv("DEBUG", True)
if type(DEBUG) == str:DEBUG = int(DEBUG)

app = Sanic(__name__)
CORS(app)

inbuilt_print = print

def print(args):
    # only log to output if in debug mode
    # logging to console is farily expensive so, log only when necessary
    if DEBUG:
        inbuilt_print(args)



@app.route("/hi", methods=["GET"])
def hi(request: Request):
   # print("Hit the endpoint. Sending hello...")
    return json({"value": "hello"})



@app.route("/bid", methods=["POST"])
def bid(request: Request):
    {'playerId': 'You-1', 'playerIds': ['You-0', 'Opponent-0', 'You-1', 'Opponent-1'], 'cards': ['TD', 'QS', 'KS', 'TS'],
     'timeRemaining': 1500, 'bidHistory': [['You-0', 16], ['Opponent-0', 17], ['You-0', 0]],
      'bidState': {'defenderId': 'Opponent-0', 'challengerId': 'You-1', 'defenderBid': 17, 'challengerBid': 0}}
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
    start_time = time.time()
    body = request.json
    # print(body)

    
    response = json(get_bid(body))
   # print(f'\n\nbid : timeRemaining:{body["timeRemaining"]} responseTime:{(time.time() - start_time)*1000} ')
    return response



@app.route("/chooseTrump", methods=["POST"])
def choose_trump(request: Request):
    """
    Request data format:
    {
        "playerId": "A1",                       # own player id
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
    }
    """
    start_time = time.time()
    body = request.json
    # print(body)
    
    response = json(get_trump_suit(body))
   # print(f'\n\nchoose_trump : timeRemaining:{body["timeRemaining"]} responseTime:{(time.time() - start_time)*1000} ')
    return response



@app.route("/play", methods=["POST"])
def play(request: Request, randomPlayer = False):
    """
    Request data format:
    {
        "playerId": "A2", # own player id
        "playerIds": ["A1", "B1", "A2", "B2"],                  # player ids in order
        "timeRemaining": 1500,
        "teams": [
            { "players": ["A1", "A2"], "bid": 17, "won": 0 },   # first team information
            { "players": ["B1", "B2"], "bid": 0, "won": 4 },    # second team information
        ],
        "cards": ["JS", "TS", "KH", "9C", "JD", "7D", "8D"],    # own cards
        "bidHistory": [ ["A1", 16],             # bidding history in chronological order
                        ["B1",17], 
                        ["A1", 17], 
                        ["B1", 0], 
                        ["A2", 0], 
                        ["B2", 0]
                    ], 
        "played": ["9S", "1S", "8S"],
        "handsHistory": [
            [
                "A1", # player who threw the first card ("7H") 
                ["7H", "1H", "8H", "JH"],           # cards that thrown in the first hand
                "B2" # winner of this hand
            ],
            [
                "A1", # player who threw the first card ("7H") 
                ["7H", "1H", "8H", "JH"],           # cards that thrown in the first hand
                "B2" # winner of this hand
            ]
        ],
        
        # represents the suit if available, the trumpSuit is only present for the player who reveals the trump
        # after the trump is revealed, the trumpSuit is present for all the players
        "trumpSuit": False, # | "H",

        # only after the trump is revealed by the player the information is revealed
        "trumpRevealed": False # | {
            # hand: 2,            # represents the hand at which the trump was revealed
            # playerId: "A2",     # the player who revealed the trump
        #},
    }
    """
    # time.sleep(5)
    start_time = time.time()
    body = request.json
    print("\n\n"+str(body))
    # print(f"\n\n body average_reward_threshold\n\n {body['average_reward_threshold']} player:{body['playerId']}")
    if randomPlayer:
        response = get_play_card(body)
    else:
        try:
            n_simulations = body['n_simulations']   # try get the number of simulations from the request
            # print('\n\n n_simulations: ' + str(n_simulations) + '\n\n')
        except:
            n_simulations = 700
            # print('\n\n n_simulations: ' + str(n_simulations) + '\n\n')
        try:
            DISCOUNT_FACTOR = body['discount_factor']   # try get the number of simulations from the request
        except:
            # lost bid : play more conservatively
            DISCOUNT_FACTOR = 0.7
            for team in body['teams']:
                if body['playerId'] in team['players']:
                    if team['bid'] != 0 or team['bid']!= -1:
                        # won_bid : play more aggressively
                        DISCOUNT_FACTOR = 0.2
        # print(f'\n\n app_discount_factor: {DISCOUNT_FACTOR} \n\n')
        response = mcts_test(body, start_time, n_simulations = 700, DISCOUNT_FACTOR = DISCOUNT_FACTOR)
    # print(f'\n\nplay {body["playerId"]}: timeRemaining:{body["timeRemaining"]} responseTime:{(time.time() - start_time)*1000} ')
    # print(f"\n\n response: {response}")
    # print(f'\n------------returning card{response}')
    return json(response)



if __name__ == "__main__":
    # Docker image should always listen in port 8001
    app.run(host="0.0.0.0", port=8001, debug=False, access_log=False)