''' source
# https://analyticsindiamag.com/comprehensive-guide-to-deep-q-learning-for-data-science-enthusiasts/

# references:
https://analyticsindiamag.com/machine-learning-fairness-bias-google-open-ai-gym/
https://analyticsindiamag.com/reinforcement-learning-comes-to-android-phones/


# Let’s summary of all Deep Q-learning processes into steps :

    1. First, provide the environment’s state to the agent.
    2. The agent uses Q-values of all possible actions for the provided state.
    3. Agent picks and performs an action based on Q-Value of action for gathering higher rewards.
    4. Observe reward and next steps.
    5. Stores previous experience in experience replay memory. 
    6. Training of the networks using experience replay memory.
    7. Repeat steps 2-6 for each state.
'''

# import the libraries
import numpy as np
import random
from IPython.display import clear_output
from collections import deque
import progressbar
import gym
from tensorflow.keras import Model, Sequential
from tensorflow.keras.layers import Dense, Embedding, Reshape
from tensorflow.keras.optimizers import Adam

# creating gym environment
env_taxi = gym.make("Taxi-v3").env
env_taxi.render()

# no. of observations and states of environment
print('Number of states: {}'.format(env_taxi.observation_space.n))
print('Number of actions: {}'.format(env_taxi.action_space.n)) 



# implementing the deep Q-learning algorithm for taxi-agent
class taxi:
     def __init__(self, env_taxi, optimizer):
         # Initialize attributes
         self._state_size = env_taxi.observation_space.n
         self._action_size = env_taxi.action_space.n
         self._optimizer = optimizer
         self.expirience_replay_memory = deque(maxlen=2000)
         # Initialize discount and exploration rate
         self.discount = 0.6
         self.exploration = 0.1
         # Build networks
         self.q_network = self._build_compile_model()
         self.target_network = self._build_compile_model()
         self.align_both_model()
     def gather(self, state, action, reward, next_state, terminated):
         self.expirience_replay_memory.append((state, action, reward, next_state, terminated))
     def _build_compile_model(self):
         model = Sequential()
         model.add(Embedding(self._state_size, 10, input_length=1))
         model.add(Reshape((10,)))
         model.add(Dense(50, activation='relu'))
         model.add(Dense(50, activation='relu'))
         model.add(Dense(self._action_size, activation='linear'))
         model.compile(loss='mse', optimizer=self._optimizer)
         return model
     def align_both_model(self):
         self.target_network.set_weights(self.q_network.get_weights())
     def active(self, state):
         if np.random.rand() <= self.exploration:
             return env_taxi.action_space.sample()
         q_values = self.q_network.predict(state)
         return np.argmax(q_values[0])
     def retraining(self, batch_size):
         minbatch = random.sample(self.expirience_replay_memory, batch_size)
         for state, action, reward, next_state, terminated in minbatch:
             target = self.q_network.predict(state)
             if terminated:
                 target[0][action] = reward
             else:
                 t = self.target_network.predict(next_state)
                 target[0][action] = reward + self.discount * np.amax(t)
             self.q_network.fit(state, target, epochs=1, verbose=0) 
def _build_compile_model(self):
     model = Sequential()
     model.add(Embedding(self._state_size, 10, input_length=1))
     model.add(Reshape((10,)))
     model.add(Dense(50, activation='relu'))
     model.add(Dense(50, activation='relu'))
     model.add(Dense(self._action_size, activation='linear'))
     model.compile(loss='mse', optimizer=self._optimizer)
     return model

# create a object of taxi class and prepare it for training
optimizer = Adam(learning_rate=0.01)
taxi = taxi(env_taxi, optimizer)
batch_size = 32
num_of_episodes = 100
timesteps_per_episode = 1000
taxi.q_network.summary() 
 
# train the model
for e in range(0, num_of_episodes):
     # Reset the environment
     state = env_taxi.reset()
     state = np.reshape(state, [1, 1])
     # Initialize variables
     reward = 0
     terminated = False
     bar = progressbar.ProgressBar(maxval=timesteps_per_episode/10, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
     bar.start()
     for timestep in range(timesteps_per_episode):
         # Run Action
         action = taxi.active(state)
         # Take action    
         next_state, reward, terminated, info = env_taxi.step(action)
         next_state = np.reshape(next_state, [1, 1])
         taxi.gather(state, action, reward, next_state, terminated)
         state = next_state
         if terminated:
             taxi.alighn_both_model()
             break
         if len(taxi.expirience_replay_memory) > batch_size:
             taxi.retrain(batch_size)
         if timestep%10 == 0:
             bar.update(timestep/10 + 1)
     bar.finish()
     if (e + 1) % 10 == 0:
         print("**********************************")
         print("Episode: {}".format(e + 1))
         env_taxi.render()
         print("**********************************")