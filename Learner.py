import World
import threading
import time
import matplotlib.pyplot as plt

import numpy as np
import sys
import pyscreenshot as ImageGrab


def print_usage():
    print 'USAGE: python Learner.py gamma alpha_decay sleep(secs)'

if len(sys.argv) != 4:
    print 'Incorrect number of arguments'
    print_usage()
    sys.exit()

discount = float(sys.argv[1]) #0.3
alpha_decay = float(sys.argv[2]) #0.1
sleepy = float(sys.argv[3]) #0.01
save = False


actions = World.actions
states = []
Q = {}
plot_x = []
plot_y = []
avg_rewards = []
avg_alphas = []
last_alphas = list()

# plt.ion()
# fig = plt.figure()
# plt.plot([], [])
# plt.show()
# plt.figure()

for i in range(World.x):
    for j in range(World.y):
        states.append((i, j))

for state in states:
    temp = {}
    for action in actions:
        temp[action] = 0.1
        World.set_cell_score(state, action, temp[action])
    Q[state] = temp

for (i, j, c, w) in World.specials:
    for action in actions:
        Q[(i, j)][action] = w
        World.set_cell_score((i, j), action, w)


def do_action(action):
    s = World.player
    r = -World.score
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
    s2 = World.player
    r += World.score
    return s, action, r, s2


def max_Q(s):
    val = None
    act = None
    for a, q in Q[s].items():
        if val is None or (q > val):
            val = q
            act = a
    return act, val


def inc_Q(s, a, alpha, inc):
    Q[s][a] *= 1 - alpha
    Q[s][a] += alpha * inc
    World.set_cell_score(s, a, Q[s][a])


def run(alpha_decay,save,sleepy):
    global discount, avg_alphas, last_alphas
    time.sleep(0.001)
    alpha = 1
    t = 1
    flag = True
    alphas = list()
    success = 0
    while flag:
        print '**********\nWorld Iter: ', World.iteration, '\nMove: ', int(t), '\n', '**********'

        # Pick the right action
        s = World.player
        max_act, max_val = max_Q(s)
        (s, a, r, s2) = do_action(max_act)
        print ' ACTION:', a, '\n ALPHA: ', alpha, '\n SCORE: ', World.score, '\n Status: ', World.status

        # Update Q
        max_act, max_val = max_Q(s2)
        inc_Q(s, a, alpha, r + discount * max_val)

        # Check if the game has restarted
        score = World.score
        rewards = World.rewards
        alphas.append(alpha)
        last_alphas.append(alpha)

        t += 1.0

        if World.has_restarted():
            print '*********************'
            print 'Average Learning Rate: ', sum(alphas)/len(alphas)
            print 'Discount Factor (gamma): ', discount
            print 'Walk Reward: ', World.walk_reward
            print 'World Iter: ', World.iteration
            print 'Number of Moves (actions): ', int(t-1.0)
            print '*********************'
            if score > 0:
                success += 1
                if save:
                    #save screenshot of world
                    im = ImageGrab.grab(bbox=(0,0,500,500))
                    im.save('WORLDscreenshot.png')
                    save = raw_input()
                    if save == 'y':
                        save = True
                    else:
                        save = False
                print 'PAUSING Goal Count: ', success
                if success >= 5:
                    raw_input()

            avg_rewards.append(sum(rewards)/len(rewards))
            avg_alphas.append(sum(alphas)/len(alphas))

            World.restart_game()

            alphas = list()
            last_alphas = list()

            time.sleep(0.001)
            t = 1.0

            plot_x.append(World.iteration)
            plot_y.append(score)

            # plt.plot(plot_x, plot_y, color="black")
            # # plt.pause(0.0001)
            # plt.draw()
            # plt.plot(plot_x,plot_y)
            # plt.show()


        #Update World iteration
        # t += 1.0
        # Update the learning rate
        alpha = 1 / pow(t, alpha_decay)#-0.1

        # MODIFY THIS SLEEP IF THE GAME IS GOING TOO FAST.
        time.sleep(sleepy)


t = threading.Thread(target=run, args=(alpha_decay,save,sleepy))
t.daemon = True
t.start()
World.start_game()

print '======================'
print plot_x, plot_y
print '======================'
print 'avg rewards', avg_rewards
print '======================'
###### Plotting ######
plt.plot(plot_x,plot_y, color='g')
plt.title("Iteration vs Score")
plt.xlabel("Iteration")
plt.ylabel("Score")
plt.grid(True)
# plt.savefig('Result00.svg', format = 'svg', dpi = 1200)
# plt.text(max(plot_x)*0.70, 0, 'Discount Factor: ' + str(discount) + '\n' + 'Walk Reward: '+ str(World.walk_reward))
# plt.text(max(plot_x), 0, r'$\mu=100,\ \sigma=15$')
# plt.savefig('myfig.png')
#####################################################
plt.clf()
plt.plot(plot_x,avg_rewards,color='k')
plt.title("Avg. Reward Over Time")
plt.xlabel("Iteration")
plt.ylabel("Avg. Reward")
plt.grid(True)
# plt.savefig('Result01.svg', format = 'svg', dpi=1200)
# plt.savefig('Result01.eps', format='eps', dpi=1000)
#####################################################
plt.clf()
plt.plot(plot_x,avg_alphas,color='m')
plt.title("Avg. " + r'$\alpha$' + " Over Time")
plt.xlabel("Iteration")
plt.ylabel("Avg. " + r'$\alpha$')
plt.grid(True)
# plt.savefig('Result02.svg', format = 'svg', dpi=1200)
#####################################################
plt.clf()
plt.plot(range(0,len(last_alphas)),last_alphas,color='y')
plt.title("Decay "+ r'$\alpha$' + " over Time (optimal)")
plt.xlabel("Actions to Goal")
plt.ylabel(r'$\alpha$')
plt.grid(True)
# plt.savefig('Result03.svg', format = 'svg', dpi=1200)

print 'Q-LEARNING GRID WORLD PARAMETERS:'
print '  Discount Factor : ', discount
print '  Walk Reward : ', World.walk_reward

# X = np.linspace(-np.pi, np.pi, 256, endpoint=True)
# C,S = np.cos(X), np.sin(X)
# plt.plot(X,C)
# plt.plot(X,S)
# plt.show()