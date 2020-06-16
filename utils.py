import generator
import numpy as np

##################################################################################################################
# Generate goal state green rectangle
##################################################################################################################
def get_goal_state(random_walls, maze_width, maze_height):
	if random_walls:
		green_x = int( maze_width - 1)
		green_y = int( maze_height - 1)
	else:
		green_x = int( maze_width - 2)
		green_y = int( maze_height - 2)
	return (green_x, green_y)


##################################################################################################################
# Generate a random set of walls
##################################################################################################################
def get_rand_walls(maze_width, maze_height, player, goal_state):
	number_of_walls = int(maze_width*maze_height*0.20) 
	walls = []

	for i in range(number_of_walls):
		while True:
			wall_x = np.random.randint(0, maze_width)
			wall_y = np.random.randint(0, maze_height)
			if (wall_x, wall_y) not in walls and (wall_x, wall_y) != player and (wall_x, wall_y) != goal_state:
				break
		walls.append((wall_x, wall_y))
	return walls

##################################################################################################################
# Generate a random set of red squares
##################################################################################################################
def get_rand_reds(maze_width, maze_height, player, goal_state, walls):
	number_of_red = int(maze_width*maze_height*0.05)
	red_squares = []

	for i in range(number_of_red):
		while True:
			red_x = np.random.randint(0, maze_width)
			red_y = np.random.randint(0, maze_height)
			if (red_x, red_y) not in walls and (red_x, red_y) != player and (red_x, red_y) not in red_squares and (red_x, red_y) != goal_state:
				break
		red_squares.append((red_x, red_y))
	return red_squares

##################################################################################################################
# Create Maze using Maze Generator
##################################################################################################################
def get_maze_from_generator(maze_width, maze_height):
	generator_width = int((maze_width - 1.0) / 2.0)
	generator_height = int((maze_height - 1.0) / 2.0)

	maze, start_x, start_y, end_x, end_y = generator.make_maze(generator_width, generator_height)
	return maze

##################################################################################################################
# Get walls from Maze (from the output of Maze Generator)
##################################################################################################################
def get_walls_for_maze(maze_array):
	walls = []
	for row in range(maze_array.shape[0]):
		for col in range(maze_array.shape[1]):
			if maze_array[row][col] == 1.0:
				walls.append((col,row))

	return walls

##################################################################################################################
# Get walls for Camgian Maze
##################################################################################################################
def get_camgian_maze():
	walls = []
	wall_mapping = {}
	# wall_mapping[0] = []
	wall_mapping[1] = [8]
	wall_mapping[2] = [7,9]
	wall_mapping[3] = [6,10]
	wall_mapping[4] = [5,11]
	wall_mapping[5] = [6,10]
	wall_mapping[6] = [4,7,9,12]
	wall_mapping[7] = [3,5,8,11,13]
	wall_mapping[8] = [2,6,10,14]
	wall_mapping[9] = [1,7,9,15]
	wall_mapping[10] = [2,6,10,14]
	wall_mapping[11] = [3,5,8,11,13]
	wall_mapping[12] = [4,7,9,12]
	wall_mapping[13] = [6,10]
	wall_mapping[14] = [5,11]
	wall_mapping[15] = [6,10]
	wall_mapping[16] = [7,9]
	wall_mapping[17] = [8]
	# wall_mapping[18] = []
	# wall_mapping[19] = []
	for row, all_cols in wall_mapping.items():
		for col in all_cols:
			walls.append((col,row))
	return(walls)
