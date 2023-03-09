# UCB2 algorithm
'''
import math
import random

class UCB2:
    def __init__(self, num_choices):
        self.num_choices = num_choices
        self.values = [0.0] * num_choices
        self.counts = [0] * num_choices
        self.t = 0

    def choose(self):
        self.t += 1
        max_ucb = -1e100
        max_choice = -1
        for i in range(self.num_choices):
            if self.counts[i] == 0:
                return i
            ucb = self.values[i] + math.sqrt(2 * math.log(self.t) / self.counts[i])
            if ucb > max_ucb:
                max_ucb = ucb
                max_choice = i
        return max_choice

    def update(self, choice, reward):
        self.counts[choice] += 1
        n = self.counts[choice]
        value = self.values[choice]
        
        new_value = ((n - 1) / float(n)) * value + (1 / float(n)) * reward
        # weighted average of the current value and the newly obtained reward
        # n is the number of times the choice has been made
        # e.g. (4/5)*previous_rewards + (1/5)*new_reward    # for 5 games played
        
        self.values[choice] = new_value
def reward_for_choice(choice):
    return random.randrange(0, 10) if choice == 0 else random.randrange(2, 12) if choice == 1 else random.randrange(3, 13)

if __name__ == "__main__":
    # Initialize the UCB2 algorithm
    ucb2 = UCB2(3)
    
    # Store the values and counts for each iteration
    values_history = []
    counts_history = []

    # Define a threshold for the variance
    variance_threshold = 0.001


    iters = int(sys.argv[1])
    # Run the algorithm for 1000 iterations
    for i in range(iters):
        choice = ucb2.choose()
        reward = reward_for_choice(choice)
        ucb2.update(choice, reward)

        # Store the values and counts for each iteration
        values_history.append(ucb2.values.copy())
        counts_history.append(ucb2.counts.copy())
        
        # Check the variance of the values
        # when variance of the values for a given choice becomes small enough, we can consider that choice to be the best choice.
        variance = np.var(ucb2.values)
        if variance < variance_threshold:
            break
    
    print(f'best choice is {ucb2.choose()}, iteration: {i}')
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
    # Print the final values for each choice
    print(ucb2.values)
    print(np.var(ucb2.values))


'''







'''
    UCB2: new code
'''

# import numpy as np
# from math import sqrt
# import random
# # Average Reward Threshold for stopping the simulation
# average_reward_threshold = 0.01
# # Keep track of the average reward in the previous iteration
# previous_average_reward = 0

# class UCB2:
#     def __init__(self, choices):
#         self.choices = choices
#         self.counts = [0 for _ in range(len(choices))]
#         self.values = [0.0 for _ in range(len(choices))]
#         self.confidence = [0.0] * len(choices)  # confidence 
#         self.upper_bounds = [0.0] * len(choices)
        
#     def reward_for_choice(self, choice):
#         if choice == 0:
#             return random.randrange(0,10)
#         elif choice == 1:
#             return random.randrange(2,12)
#         if choice == 2:
#             return random.randrange(3,13)
#         if choice == 3:
#             return random.randrange(3,13)
#         if choice == 4:
#             return random.randrange(3,14)
#         if choice == 5:
#             return random.randrange(3,15)
        
#     def choose(self):
#         n = sum(self.counts)
#         for i in range(len(self.choices)):
#             if self.counts[i] == 0:
#                 print(f'---------------count------------------{self.counts}')
#                 self.counts[i] = 1
#                 return i
#             reward = self.reward_for_choice(i)
#             self.counts[i] += 1
#             self.values[i] = ((n - 1) / float(n)) * self.values[i] + (1 / float(n)) * reward
#             self.confidence[i] = sqrt(2 * math.log(n) / self.counts[i])
#             upper_bound = self.values[i] + self.confidence[i] / sqrt(self.counts[i])
#             self.upper_bounds[i] = upper_bound
        
#         return max(range(len(self.choices)), key=lambda x: self.upper_bounds[x])
    
#     def run_simulation(self, num_iterations):
#         choices = []
#         for i in range(num_iterations):
#             choice = self.choose()
#             self.choices.append(choice)
#         return choices
#     def run_simulation2(self, num_iterations):
#         '''
#         - accuracy as stopping criteria
#         - accuracy can have max value of 1.0
#         '''

#         accuracy_threshold = 0.01

#         # Initialize a flag to indicate if the accuracy threshold has been reached
#         accuracy_reached = False
#         choices = []
#         rewards = []
#         previous_average_reward = 0
#         for i in range(num_iterations):
#             print(i)
#             choice = self.choose()
#             self.choices.append(choice)

#             # while not accuracy_reached and i < num_iterations:
#             # Choose the arm using the UCB2 algorithm
#             # choice = self.choose()
            
#             # Get the reward for the chosen arm
#             reward = self.reward_for_choice(choice)
#             rewards.append(reward)
            
#             # Update the values and counts for the chosen arm
#             # self.update(choice, reward)
            
#             # # Calculate the average reward for each arm
#             # avg_rewards = [self.values[i] / self.counts[i] if self.counts[i]!=0 else 0 for i in range(len(self.choices))]
#             # # Check if the accuracy threshold has been reached
#             # accuracy_reached = max(avg_rewards) >= accuracy_threshold
#             # if accuracy_reached:
#             #     break

#             # Calculate the average reward
#             average_reward = sum(rewards) / (i + 1)
#             # Check if the algorithm has converged
#             if abs(average_reward - previous_average_reward) < average_reward_threshold:
#                 break
#             # Update the previous average reward
#             previous_average_reward = average_reward
#         return choices, i, average_reward, self.values.copy(), self.counts.copy()
# # Create an instance of UCB2 algorithm with choices [0, 1, 2]
# ucb2 = UCB2([0, 1, 2])

# # Run the simulation for 1000 iterations
# # choices = ucb2.run_simulation(1000)
# choices, iters, average_reward, values, counts = ucb2.run_simulation2(1000)

# # Print the number of times each choice was selected
# print(f"Choice 1 selected: {choices.count(0)}, value: {ucb2.values}")
# print(f"Choice 1 selected: {choices.count(1)}, value: {ucb2.values}")
# print(f"Choice 2 selected: {choices.count(2)}, value: {ucb2.values}")

# # Display
# print(f"choice: {ucb2.choose()}, iterations: {iters+1}, Average reward: {average_reward}\n values={values}, counts:{counts}")




import math
import random
import sys
import numpy as np
import matplotlib.pyplot as plt

class UCB2:
    def __init__(self, num_arms, show_plot=False):
        self.num_arms = num_arms
        self.counts = [0 for _ in range(num_arms)]
        self.values = [0.0 for _ in range(num_arms)]
        self.show_plot = show_plot
    def choose_arm(self):
        t = sum(self.counts)    # number of times any arm has been played
        if t < self.num_arms:
            return t            # select all arms at least once before starting to exploit
        
        ucb_values = [0.0 for _ in range(self.num_arms)]
        for arm in range(self.num_arms):
            if self.counts[arm] > 0:
                # arm has been chosen at least once
                average_reward = self.values[arm] / self.counts[arm]
                exploration = math.sqrt(2 * math.log(t) / self.counts[arm])
                ucb_values[arm] = average_reward + exploration
        
        # return the arm with the highest UCB value
        return max(range(self.num_arms), key=lambda arm: ucb_values[arm])

    def update(self, chosen_arm, reward):
        self.counts[chosen_arm] = self.counts[chosen_arm] + 1
        n = self.counts[chosen_arm]
        value = self.values[chosen_arm]
        new_value = ((n - 1) / float(n)) * value + (1 / float(n)) * reward
        self.values[chosen_arm] = new_value
    
    def simulate(self, reward_function, num_iterations = 1000):
        # Keep track of rewards received in each iteration
        rewards = []

        # History to plot
        values_history = []
        counts_history = []

        # Average Reward Threshold for stopping the simulation
        average_reward_threshold = 0.01
        # Keep track of the average reward in the previous iteration
        previous_average_reward = 0

        for i in range(num_iterations):
            # Choose an arm to play
            arm = ucb2.choose_arm()
            
            # Get the reward for the chosen arm
            reward = reward_function(arm)
            
            # Update the UCB2 algorithm with the chosen arm and the reward
            ucb2.update(arm, reward)
            
            # Keep track of the rewards received
            rewards.append(reward)

            values_history.append(ucb2.values.copy())
            counts_history.append(ucb2.counts.copy())

            # Calculate the average reward
            average_reward = sum(rewards) / (i + 1)
            # Check if the algorithm has converged
            if abs(average_reward - previous_average_reward) < average_reward_threshold:
                break
            # Update the previous average reward
            previous_average_reward = average_reward

        if self.show_plot:
            print(f"choice: {ucb2.values.index(max(ucb2.values))}, iterations: {i+1}, Average reward: {sum(rewards) / num_iterations}\n values: {ucb2.values}, counts: {ucb2.counts}")
            # Plot the values and counts for each iteration
            self.plot(values_history, counts_history)
    def plot(self, values_history, counts_history):
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
        # Print the final values for each choice
        print(ucb2.values)
        print(np.var(ucb2.values))

if __name__ == "__main__":
    def reward_function(choice):
        return random.randrange(0, 10) if choice == 0 else random.randrange(2, 12) if choice == 1 else random.randrange(3, 13)
    
    # Initialize the UCB2 object with the number of arms (3 in this case)
    # Number of iterations to run
    num_iterations = 1000
    
    ucb2 = UCB2(3, True)
    ucb2.simulate(reward_function, num_iterations)

    