'''
    # ------------------------
    #  Predicting throwables
    # ------------------------
    inputs = [[0,0,1], [0,1,1], [,0,1], [1,1,1], ]
    first two features are data
    third feature of input denote whether or not it can be output
    how to train such network?
'''

import torch
import torch.nn as nn
import torch.optim as optim
import random

# Define the neural network model
class Network(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(Network, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.fc3 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x

# Initialize the model
input_size = 2
hidden_size = 64
output_size = 1
model = Network(input_size, hidden_size, output_size)

# Define the loss function and optimizer
criterion = nn.MSELoss() # Mean Squared Error loss
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Define the memory buffer for experience replay
memory = []

# Train the network
for episode in range(100): # Train for 100 episodes
    state = random.randint(0, 29) # Start in a random state
    for t in range(100): # Take up to 100 steps in each episode
        # Choose an action randomly
        action = random.randint(0, 2)

        # Take the action and observe the next state and reward
        next_state = random.randint(0, 29)
        reward = random.uniform(-1, 1)

        # Store the transition in the memory buffer
        memory.append((state, action, reward, next_state))

        # Sample a random batch of transitions from the memory buffer
        batch = random.sample(memory, 32)

        # Unpack the batch and convert to tensors
        states, actions, rewards, next_states = zip(*batch)
        states = torch.tensor(states, dtype=torch.float32)
        actions = torch.tensor(actions, dtype=torch.long)
        rewards = torch.tensor(rewards, dtype=torch.float32)
        next_states = torch.tensor(next_states, dtype=torch.float32)

        # Compute the Q-values for the current states and next states
        q_values = model(states)
        next_q_values = model(next_states)

        # Compute the target Q-values
        target_q_values = rewards + 0.9 * next_q_values.max(1)[0].unsqueeze(-1)

        # Compute the loss between the predicted and target Q-values
        loss = criterion(q_values.gather(1, actions.unsqueeze(-1)), target_q_values)

        # Backpropagate the error and update the model's parameters
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

'''
# ------------------------
# Distributing Rewards
# ------------------------
'''
# Intrinsic Motivation : Reward for intermediate steps
# Extrinsic Motivation : Reward for final goal <Discount> <monte Carlo> <Temproal Difference + SARSA>
import random
import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

# Reward function
def reward_for_choice(choice):
    return random.randrange(0, 10) if choice == 0 else random.randrange(2, 12) if choice == 1 else random.randrange(3, 13)

# DQN Model
model = Sequential()
model.add(Dense(32, input_dim=1, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(3, activation='linear'))
model.compile(loss='mse', optimizer=Adam(lr=0.01))

# Training loop
for episode in range(10000):
    # Choose an action (0, 1, or 2)
    action = np.argmax(model.predict(np.array([[0]])))
    
    # Get the reward for the chosen action
    reward = reward_for_choice(action)
    
    # Train the model
    target = np.zeros((1, 3))
    target[0][action] = reward
    model.fit(np.array([[0]]), target, epochs=1, verbose=0)

# Test the model
print(model.predict(np.array([[0]])))


'''
# ------------------------
# Neural Network
# ------------------------
inputs = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1]
first 32 [0-31] features represent a card
[32] represent whether or not trump_set by player
[33] represent whether or not card could be trump
[34] feature represent whether or not trump is revealed
[35] card is at table
[36] card is with opponent
[37] represent whether or not it can be output
how to create and train such network?
'''

import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense

# Preprocess the data
inputs = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1]
inputs = np.array(inputs, dtype=np.float32).reshape(1, -1)

# Define the model architecture
model = Sequential()
model.add(Dense(32, input_shape=(inputs.shape[1],), activation='relu'))
model.add(Dense(16, activation='relu'))
model.add(Dense(3, activation='softmax'))

# Compile the model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
model.fit(inputs, labels, epochs=10, batch_size=32, validation_split=0.2)

# Evaluate the model
score = model.evaluate(inputs, labels, batch_size=32)
print("Loss: {:.4f}, Accuracy: {:.2f}%".format(score[0], score[1] * 100))


'''
# One Hot Encoding
# all cards 
all_cards = ['7H', '8H', 'QH', 'KH', 'TH', '1H', '9H', 'JH', '7D', '8D', 'QD', 'KD', 'TD', '1D', '9D', 'JD', '7C', '8C', 'QC', 'KC', 'TC', '1C', '9C', 'JC', '7S', '8S', 'QS', 'KS', 'TS', '1S', '9S', 'JS']

# Create a list of card names
to_one_hot_encode = ['7H', '8H', 'QH', 'KH']

# throwables
throwables = ['7H', '8H']

# trump
trump_suits = ['H', 'D', 'C', 'S', None]

# Revealed trump
trump_revealed = True
'''
import numpy as np
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

# all cards 
all_cards = ['7H', '8H', 'QH', 'KH', 'TH', '1H', '9H', 'JH', '7D', '8D', 'QD', 'KD', 'TD', '1D', '9D', 'JD', '7C', '8C', 'QC', 'KC', 'TC', '1C', '9C', 'JC', '7S', '8S', 'QS', 'KS', 'TS', '1S', '9S', 'JS']

# Create a list of card names
to_one_hot_encode = [['7H', '8H', 'QH', 'KH']]

# throwables
throwables = ['7H', '8H']

# trump
trump_suits = ['H', 'D', 'C', 'S', None]

# Revealed trump
trump_revealed = True



# Convert the card names to one hot encoded vectors
def card_to_vector(card):
    index = all_cards.index(card['card'])
    vector = np.zeros(38)
    vector[index] = 1
    
    throwable = card['card'] in card['throwables']
    vector[32] = throwable

    # 1 is trump <player set trump> :: 0 maybe <player dont set trump>
    set_trump = card['set_trump']
    vector[33] = set_trump
    probably_trump = card['probably_trump']
    vector[34] = probably_trump

    is_trump_revealed = card['is_trump_revealed']
    vector[35] = is_trump_revealed

    at_table = card['card'] in card['at_table']
    vector[36] = at_table

    opponents_card = card in opponents_card
    vector[37] = opponents_card

    return vector

def input_to_vector(input_cards):
    # one hot encode the cards
    return np.array([card_to_vector(card) for card in input_cards])

X = np.array([input_to_vector(input_cards) for input_cards in to_one_hot_encode])