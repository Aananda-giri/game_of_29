# --------------------------------------------
# correlation between cards and scores (bid)
# --------------------------------------------

* I have set of cards that give certain score, how to predict score by new set of cards by training on data?

To predict the score of a new set of cards based on training data, you can use a machine learning model. One approach would be to use a supervised learning algorithm, which requires a dataset of labeled examples that includes the input (the set of cards) and the corresponding output (the score).

Here are the general steps you can follow to train a machine learning model to predict the score of a new set of cards:

    1. Collect a dataset of sets of cards and their corresponding scores.

    2. Preprocess the data as needed. This may include cleaning the data, scaling numerical features, and encoding categorical features.

    3. Split the data into a training set and a test set.

    4. Choose a machine learning model and train it on the training set. There are many different types of models that you can use, such as linear regression, decision trees, or neural networks.

    5. Evaluate the model's performance on the test set. This will give you an idea of how well the model can generalize to new data.

    6. Fine-tune the model by adjusting its hyperparameters or trying different models until you achieve satisfactory performance.

    7. Use the trained model to predict the score of a new set of cards by providing it as input to the model.

It's important to note that the accuracy of your predictions will depend on the quality and diversity of your training data, as well as the complexity and flexibility of your chosen model.






* a fixed set of variables contribute to result, how to know contribution of each variable involved?

There are several methods that can be used to determine the contribution of individual variables to a result. Here are a few options:

    1. Sensitivity analysis: This involves altering the value of a single variable while holding all other variables constant, and observing the effect on the result. This can be repeated for each variable to determine its relative contribution.

    2. Regression analysis: This statistical technique can be used to analyze the relationship between a dependent variable (the result) and one or more independent variables (the variables that contribute to the result). By analyzing the statistical relationship between the variables, it is possible to determine the relative importance of each variable in predicting the result.

    3. Partial dependence plots: These plots show the marginal effect of a single variable on the predicted result, holding all other variables constant. This can be helpful in understanding the individual contributions of each variable.

    4. Decision tree models: These models can be used to identify the most important variables in predicting a result by creating a tree-like structure that splits the data based on the variables that are most important in predicting the result.




* problem: I have cards and score, score won varies between 16 and 25. I want to know is there any correlation between cards and score.

* how to seperate correlation of one variable when a combination of variables give one result

## multiple regression analysis
It is often necessary to separate the contribution of individual variables to a combined result when working with multiple variables. One way to do this is by using multiple regression analysis, which allows you to model the relationship between a dependent variable (the combined result) and one or more independent variables (the individual variables).

`from sklearn.linear_model import LinearRegression`

# Create a LinearRegression model and fit it to the data
`model = LinearRegression()`
`model.fit(X, y)`

# Extract the coefficients for the independent variables
`coefficients = model.coef_`

# Print the coefficients
`print(coefficients)`

## In this example, X is a 2D array of independent variables and y is a 1D array of the dependent variable. The coef_ attribute of the LinearRegression model contains the coefficients for the independent variables.

## Correlation: movie rating vs. number of viewers
* lies between -1 and 1
* sign tells direction of correlation (-ve correlation: 0 to -1, +ve correlation: 0 to 1) 
* magnitude tells quality of straight line fit (larger the magnitude better the quality)

# -------------------------------
# set best trump suit
# -------------------------------


# set max one of max repeated suit as trump
max_repeated_suit = max(set(suits), key = suits.count).upper()
suits = ['H', 'H', 'C', 'S']
set H

# set higher weighted cards as trump
suits = ['C', 'C', 'H', 'H']

# set lower weighted cards as trump
suits = ['C', 'C', 'H', 'H']

# -------------------------------
# handsHistory to string
# -------------------------------
handsHistory = [[
                "A1", # player who threw the first card ("7H") 
                ["7H", "1H", "8H", "JH"],           # cards that thrown in the first hand
                "B2" # winner of this hand
            ],[
                "A1", # player who threw the first card ("7H") 
                ["7H", "1H", "8H", "JH"],           # cards that thrown in the first hand
                "B2" # winner of this hand
            ],
            ]

[[history[0]] + [[str(card) + 'test' for card in history[1]]] + [history[-1]] for history in handsHistory]

output = [['A1', ['7Htest', '1Htest', '8Htest', 'JHtest'], 'B2'], ['A1', ['7Htest', '1Htest', '8Htest', 'JHtest'], 'B2']]

# -------------------------------
# Time distribution code
# -------------------------------
import time
class player:
    def __init__(self) -> None:
        # initialize max. time a player gets for a game (bid + play)
        self.max_time = 1500

        # time at requesting bid/play
        start_time = time.time()
        request_bid() / request_play()
        
        # substract time used for bidding/play
        self.timeRemaining  -= (time.time() - start_time) * 1000

# -------------------------------
# score board
# -------------------------------
# Rank	Team	    Games Played	Win/Loss/Nullified	    Score	Score (%)	Reckless	Last Submission	        Avg R.T (ms)
#       in ka dum	500	            343/136/21	            207	    70.7	    2	        27 Dec, 07:12 pm	    811.91

# message	    Games Played	Win/Loss/Nullified	    Score	Max_Score (%)	Date

results = {'reckless':0, 'chicken':0, 'won':0, 'loose': 0, 'won_points':0}
matchesPlayed = 1000
hyperParameters = {'learning_rate': 0.2 }
for i in range(matchesPlayed):
    result = gamePlay(hyperParameters)
    
    results['reckless'] += results['reckless']
    results['chicken'] += result['chicken']
    results['won'] += result['won']
    results['loose'] += result['loose']
    results['won_points'] += result['won_points']

'''
# note:
game result = {'over-shoot':(bid_value - score) if (has_bid and bid_value >= score), 'under-shoot': (has_bid and bid_value - score) if score >= bid_value, 'won': 1 if won(score >= bid_value || opponent loose) 0 else, 'loose': 1 if loose((score < bid_value or opponent won)) 0 else, 'won_points':0}

'''

# -------------------------------
# visualize
# -------------------------------

# effect of exploration in no. of wins
from matplotlib import pyplot as plt

matchesPlayed = 1000
exploration_rate = [25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]
matches_won =  [38496, 42000, 46752, 49320, 53200,
         56000, 62316, 64928, 67317, 68748, 73752]

plt.plot(exploration_rate, matches_won)
plt.xlabel('exploration_rate')
plt.ylabel(f'matches won of {matchesPlayed} played')
plt.title('Effect of Exploraion Rate In Matches Won')
plt.show()