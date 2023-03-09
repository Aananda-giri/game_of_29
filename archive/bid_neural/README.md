# play neural nets: <ToDo>
 ## Generate Data for neural nets:
    python3 Play.py train_data_test 1000 train_data.pkl > test.out

## Todo:
    1. Generate training data from monte-carlo self plays.
    2. Train a new model using that data.
    3. Evaluate the new model against the current best model. If the new model is better, then save it to replace the best model.
    4. Quit after a set number of iterations or if there hasn’t been any improvement for a while.
    5. Generate new training data from games where the current model plays against itself, exploration_rate=0.1
    # 6. Continue to train the current model with the newly generated data for a few epochs.
    7. Go to step 3.


# Neural network for bidding in Game of 29:
```
- very low accuracy
```
only one output is given at a time while training,how to one hot encode inputs and outputs
* Outputs Neurons = 2   # Each representing bid_value when trump set and bid_value if trump not set

* Inputs : 4 cards
* Outputs : 3 numbers of range 0 to 28

example input: AD, QC, JH, 9S
example output: 12
only one output is given at a time while training,how to one hot encode inputs and outputs

# Neural network for playing in Game of 29:
* Input Neurons = 32    # Representing each possible card
* Outputs Neurons = 1   # One of inputs given

* Inputs : 8 cards
* Outputs : one of 8 cards given as input

example input: ['AD', 'QC', 'JH', '9S', '1S','9D','KH','KS']
example output: 'JH'
