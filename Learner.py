import MazeWorld as World
import threading
import time
import numpy as np
import sys
from PIL import ImageGrab
from plot_utils import *

# python Learner.py 0.3 0.1 0.03
def print_usage():
    print('USAGE: python Learner.py gamma alpha_decay sleep(secs)')

if len(sys.argv) != 4:
    print('Incorrect number of arguments')
    print_usage()
    sys.exit()

# Initialize parameters
discount = float(sys.argv[1]) # 0.3 # Discount factor
alpha_decay = float(sys.argv[2]) # 0.1 # Learning rate decay

# Speed of game
# Number of seconds program should pause execution between iterations
sleepy = float(sys.argv[3]) # 0.01 
save = False

# Define the actions  = ["up", "down", "left", "right"]
actions = World.actions
states = []
Q = {}
episodes = []
scores = []
avg_rewards = []
alphas = []

# Define the states
for i in range(World.x):
    for j in range(World.y):
        states.append((i, j))

# Initialize Q-table
for state in states:
    temp = {}
    for action in actions:
        temp[action] = 0.1
        World.set_cell_score(state, action, temp[action])
    Q[state] = temp

# Map actions to states in Q-table
for (i, j, c, w) in World.specials:
    for action in actions:
        Q[(i, j)][action] = w
        World.set_cell_score((i, j), action, w)

def do_action(action):
    """
    Performs action and returns state, action taken, reward and new state
    action : action to perform "up", "down", "left", "right"

    Returns
    state, action, reward, state2 : state, action, reward, new state
    """
    state = World.player
    reward = -World.score
    if action == actions[0]:
        World.try_move(0, -1)
    elif action == actions[1]:
        World.try_move(0, 1)
    elif action == actions[2]:
        World.try_move(-1, 0)
    elif action == actions[3]:
        World.try_move(1, 0)
    else:
        return
    state2 = World.player
    reward += World.score
    return state, action, reward, state2

def max_Q(state):
    """
    Returns the max Q-value for all actions in a given state
    :param state (tuple): state to check Q-values

    :return action, val (str, float): action with max Q-value
    """
    val = None
    action = None
    for a, q in Q[state].items():
        if val is None or (q > val):
            val = q
            action = a
    return action, val

def update_Q(state, action, alpha, reward, discount, max_q):
    """
    Update Q-table
    :param state (tuple): state to be updated
    :param action (str): action corresponding to state
    :param alpha (float): alpha value 
    :param inc (float): increment value 

    :return None: updates Q-value and World Environment
    """
    Q[state][action] = Q[state][action] * (1 - alpha)
    Q[state][action] = Q[state][action] + (alpha * (reward + discount * max_q))
    World.set_cell_score(state, action, Q[state][action])

def run(alpha_decay,save,sleepy):
    global discount, avg_alphas
    time.sleep(0.001)
    alpha = 1
    number_of_iterations = 1.0
    success = 0
    verbose = False
    while True:

        # Pick the action
        state = World.player
        max_act, max_val = max_Q(state)
        (state, action, reward, state2) = do_action(max_act)
        
        if verbose:
            print('**********\nWorld Iter: ', World.iteration, '\nMove: ', int(number_of_iterations - 1.0), '\n', '**********')
            print(' ACTION:', action, '\n ALPHA: ', alpha, '\n SCORE: ', World.score, '\n Status: ', World.status)

        # Update Q-Value
        max_act, max_val = max_Q(state2)
        update_Q(state, action, alpha, reward, discount, max_val)

        # Check if the game has restarted
        if World.has_restarted():

            avg_rewards.append(sum(World.rewards)/len(World.rewards))
            episodes.append(World.iteration)
            alphas.append(alpha)
            scores.append(World.score)

            if verbose:
                print_info(alpha, discount, World.walk_reward, World.iteration, int(number_of_iterations - 1.0))

            if World.iteration == 20:
                World.end_game()

            World.restart_game()
            time.sleep(0.001)

        # Update number of iteration
        number_of_iterations += 1.0

        # Update the learning rate
        alpha = 1 / pow(number_of_iterations, alpha_decay)#-0.1

        # MODIFY THIS SLEEP IF THE GAME IS GOING TOO FAST.
        time.sleep(sleepy)

t = threading.Thread(target=run, args=(alpha_decay,save,sleepy))
t.daemon = True
t.start()
World.start_game()

# plot results and save
results_to_plots(episodes, scores, avg_rewards, discount, alphas, World.walk_reward)

print('Q-LEARNING GRID WORLD PARAMETERS:')
print('  Discount Factor : ', discount)
print('  Walk Reward : ', World.walk_reward)