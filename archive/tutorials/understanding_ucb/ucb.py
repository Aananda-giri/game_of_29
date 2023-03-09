import math
import random
import sys
import numpy as np
import matplotlib.pyplot as plt

class UCB:
    def __init__(self, choices):
        self.choices = choices
        self.num_choices = len(choices)
        self.counts = [0] * self.num_choices
        self.values = [0.0] * self.num_choices
    
    def choose(self):
        total_count = sum(self.counts)
        for i in range(self.num_choices):
            if self.counts[i] == 0:
                return self.choices[i]
            else:
                
                # Exploration: selecting less explored choices
                upper_bound = (math.sqrt(2 * math.log(total_count) / self.counts[i]))
                
                # Exploitation: selecting choices with high reward
                self.values[i] = (self.values[i] / self.counts[i]) + upper_bound
                
        return max(zip(self.values, self.choices))[1]

    def update(self, choice, reward):
        index = self.choices.index(choice)
        self.counts[index] += 1
        self.values[index] += reward
def reward_for_choice(choice):
    return random.randrange(0, 10) if choice == 0 else random.randrange(2, 12) if choice == 1 else random.randrange(3, 13)

if __name__ == "__main__":
    choices = [0, 1, 2]
    ucb = UCB(choices)
    iterations = int(sys.argv[1])

    # Store the values and counts for each iteration
    values_history = []
    counts_history = []

    # Define a threshold for the variance
    variance_threshold = 0.001

    for i in range(iterations):
        choice = ucb.choose()
        reward = reward_for_choice(choice)
        ucb.update(choice, reward)

        values_history.append(ucb.values.copy())
        counts_history.append(ucb.counts.copy())
        
        # Check the variance of the values
        # when variance of the values for a given choice becomes small enough, we can consider that choice to be the best choice.
        variance = np.var(ucb.values)
        if variance < variance_threshold:
            break
    
    print(f'best choice is {ucb.choose()}, iteration: {i}')
    # Plot the values and counts for each iteration
    plt.figure(figsize=(10,5))
    plt.subplot(2,1,1)
    plt.plot(values_history)
    plt.xlabel('Iteration')
    plt.ylabel('Value')
    plt.legend(['Choice 0', 'Choice 1', 'Choice 2'])

    plt.subplot(2,1,2)
    plt.plot(counts_history)
    plt.xlabel('Iteration')
    plt.ylabel('Count')
    plt.legend(['Choice 0', 'Choice 1', 'Choice 2'])

    plt.tight_layout()
    plt.show()
