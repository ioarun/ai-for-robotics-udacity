from gridworld import GridWorld
import time

def compute_value(grid,value,policy, goal,cost):
	action = [[-1 for col in range(len(grid[0]))] for row in range(len(grid))]
	change = True
	while change:
		change = False

		for x in range(len(grid)):
			for y in range(len(grid[0])):

				if goal[0] == x and goal[1] == y:
					if value[x][y] > 0:
						value[x][y] = 0
						change = True

				elif grid[x][y] == 0:
					temp = []
					for a in range(len(delta)):
						x2 = x + delta[a][0]
						y2 = y + delta[a][1]

						if x2 >= 0 and x2 < len(grid) and y2 >= 0 and y2 < len(grid[0]) and grid[x2][y2]==0:
							v2 = value[x2][y2] + cost_step

							if v2 < value[x][y]:
								change = True
								value[x][y] = v2
								temp.append([str(v2)+" "+str(delta_name[a])+"", [x, y]])
								gridworld.draw_cell(temp)
								gridworld.show()
								time.sleep(0.5)
								policy[x][y] = delta_name[a]

	return policy 

grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 1, 0],
        [0, 0, 1, 0, 1, 0],
        [0, 0, 0, 0, 1, 0]]
value = [[99  for col in range(len(grid[0]))] for row in range(len(grid))]
policy = [[' ' for col in range(len(grid[0]))] for row in range(len(grid))]
policy[len(grid)-1][len(grid[0]) - 1] = '*'
goal = [len(grid)-1, len(grid[0])-1]
cost = 1 # the cost associated with moving from a cell to an adjacent one

init = [0, 0]

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']

cost_step = 1

screen_size = 500
cell_width = 45
cell_height = 45
cell_margin = 5

gridworld = GridWorld(screen_size,cell_width, cell_height, cell_margin,init, goal, grid)

print compute_value(grid,value,policy, goal, cost=1)
while True:
	pass
