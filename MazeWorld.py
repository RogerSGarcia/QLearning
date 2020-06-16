from utils import *
from tkinter import *
import numpy as np
import time
from PIL import ImageGrab

# Configure the type of Q-run
camgian_maze = False
random_walls = True
generate_reds = False

# Determine if we will use Camgian Demo Maze
if camgian_maze:
	maze_width = 19
	maze_height = 19
	random_walls = False
	generate_reds = True
else:
	maze_width = 3
	maze_height = 3

# Initalize Grid World using tkinter
iteration = 1
triangle_size = 0.0
cell_score_min = -9999
cell_score_max = 9999
Width = 50

master = Tk()
(x, y) = (maze_width, maze_height)
master.title(str(x) + 'x' + str(y) + "GridWorld")
board = Canvas(master, width=x*Width, height=y*Width)
position = [[0 for i in range(x)] for j in range(y)]
colorscore = [[0 for i in range(x)] for j in range(y)]
actions = ["up", "down", "left", "right"]

score = 1
restart = False
walk_reward = -0.01
status = None
rewards = []
specials = []

##################################################################################################################
# Generate goal state (GREEN)
##################################################################################################################
goal_state = get_goal_state(random_walls, maze_width, maze_height)
specials.append((goal_state[0], goal_state[1], "green", 1))

##################################################################################################################
# Generate a set of walls (BLACK)
##################################################################################################################
if random_walls:
	player = (0,0)
	walls = get_rand_walls(maze_width, maze_height, player, goal_state)
else:
	player = (1, 1)
	if camgian_maze:
		walls = get_camgian_maze()
	else:
		maze = get_maze_from_generator(maze_width, maze_height)
		walls = get_walls_for_maze(maze)

##################################################################################################################
# Generate random set of red rectangles (RED)
##################################################################################################################
if generate_reds:
	red_squares = get_rand_reds(maze_width, maze_height, player, goal_state, walls)
	for red_xy in red_squares:
		specials.append((red_xy[0], red_xy[1], "red", -1))



##################################################################################################################
##################################################################################################################
# Under the hood stuff for World Environment 
##################################################################################################################
##################################################################################################################
cell_scores = {}

def create_triangle(i, j, action):
    if action == actions[0]:
        return board.create_polygon((i+0.5-triangle_size)*Width, (j+triangle_size)*Width,
                                    (i+0.5+triangle_size)*Width, (j+triangle_size)*Width,
                                    (i+0.5)*Width, j*Width,
                                    fill="white", width=1)
    elif action == actions[1]:
        return board.create_polygon((i+0.5-triangle_size)*Width, (j+1-triangle_size)*Width,
                                    (i+0.5+triangle_size)*Width, (j+1-triangle_size)*Width,
                                    (i+0.5)*Width, (j+1)*Width,
                                    fill="white", width=1)
    elif action == actions[2]:
        return board.create_polygon((i+triangle_size)*Width, (j+0.5-triangle_size)*Width,
                                    (i+triangle_size)*Width, (j+0.5+triangle_size)*Width,
                                    i*Width, (j+0.5)*Width,
                                    fill="white", width=1)
    elif action == actions[3]:
        return board.create_polygon((i+1-triangle_size)*Width, (j+0.5-triangle_size)*Width,
                                    (i+1-triangle_size)*Width, (j+0.5+triangle_size)*Width,
                                    (i+1)*Width, (j+0.5)*Width,
                                    fill="white", width=1)


def render_grid():
    global specials, walls, Width, x, y, player, position
    for i in range(x):
        for j in range(y):
            position[i][j] = board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill="white", width=1)
            temp = {}
            for action in actions:
                temp[action] = create_triangle(i, j, action)
            cell_scores[(i,j)] = temp
    for (i, j, c, w) in specials:
        board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill=c, width=1)
    for (i, j) in walls:
        board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill="black", width=1)

render_grid()


def set_cell_score(state, action, val):
	global cell_score_min, cell_score_max
	triangle = cell_scores[state][action]
	green_dec = int(min(255, max(0, (val - cell_score_min) * 255.0 / (cell_score_max - cell_score_min))))
	green = hex(green_dec)[2:]
	red = hex(255-green_dec)[2:]
	if len(red) == 1:
		red += "0"
	if len(green) == 1:
		green += "0"
	color = "#" + red + green + "00"
	board.itemconfigure(triangle, fill=color)


def try_move(dx, dy):
	global player, x, y, score, walk_reward, me, restart, iteration, rewards, status
	if restart == True:
		restart_game()
	new_x = player[0] + dx
	new_y = player[1] + dy
	score += walk_reward
	rewards.append(walk_reward)
	if (new_x >= 0) and (new_x < x) and (new_y >= 0) and (new_y < y) and not ((new_x, new_y) in walls):
		color_visited(new_x, new_y)
		board.coords(me, new_x*Width+Width*2/10, new_y*Width+Width*2/10, new_x*Width+Width*8/10, new_y*Width+Width*8/10)
		player = (new_x, new_y)
	for (i, j, c, w) in specials:
		if new_x == i and new_y == j:
			score -= walk_reward
			rewards.pop()
			score += w
			rewards.append(w)
			if score > 0:
				# print iteration, " ====== [SUCCESS] Action lead to Green Goal! score: ", score
				status = '[SUCCESS] GOAL'
			else:
				# print iteration, " XXXXXX [FAILURE] Action lead to DEATH x_x ! score: ", score
				status = '[FAILURE] TRY AGAIN'
			restart = True
			iteration += 1
			# color_reset()
			return
    #print "score: ", score

def color_visited(new_x, new_y):
	colorscore[new_x][new_y] += 1
	colorind = colorscore[new_x][new_y]
	colorspeed = 0.045
	colorvalue  = 255
	colorvalue2 = 255
	colorvalue = int(round(max(0, -(colorspeed*colorind**2)+255), 0))
	if colorvalue == 0:
		colorind -= 505
		colorvalue2 = int(round(max(0, -(colorspeed*colorind**2)+255), 0))
	colorvalue  = format(colorvalue,  '02x')
	colorvalue2 = format(colorvalue2, '02x')
	coloritem = "#" + colorvalue + colorvalue2 + "ff"
	board.itemconfigure(position[new_x][new_y], fill=coloritem, tag="visited")

def color_reset():
	for item in board.find_withtag("visited"):
		board.itemconfigure(item, fill="white")

def call_up(event):
    try_move(0, -1)


def call_down(event):
    try_move(0, 1)


def call_left(event):
    try_move(-1, 0)


def call_right(event):
    try_move(1, 0)


def restart_game():
    global player, score, me, restart, rewards
    if random_walls:
    	player = (0, 0)
    else:
    	player = (1, 1)
    score = 1
    restart = False
    rewards = list()
    board.coords(me, player[0]*Width+Width*2/10, player[1]*Width+Width*2/10, player[0]*Width+Width*8/10, player[1]*Width+Width*8/10)

def has_restarted():
    return restart

master.bind("<Up>", call_up)
master.bind("<Down>", call_down)
master.bind("<Right>", call_right)
master.bind("<Left>", call_left)

me = board.create_rectangle(player[0]*Width+Width*2/10, player[1]*Width+Width*2/10,
                            player[0]*Width+Width*8/10, player[1]*Width+Width*8/10, fill="orange", width=1, tag="me")
board.grid(row=0, column=0)

def start_game():
	master.mainloop()
