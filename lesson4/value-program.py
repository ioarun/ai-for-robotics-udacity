# ----------
# Problem:
# 
# Create a function compute_value which returns
# a grid of values. The value of a cell is the minimum
# number of moves required to get from the cell to the goal. 
#
# If a cell is a wall or it is impossible to reach the goal from a cell,
# assign that cell a value of 99.
# ----------

grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 1, 0],
        [0, 0, 1, 0, 1, 0],
        [0, 0, 0, 0, 1, 0]]
value = [[99  for col in range(len(grid[0]))] for row in range(len(grid))]

goal = [len(grid)-1, len(grid[0])-1]
cost = 1 # the cost associated with moving from a cell to an adjacent one

init = [0, 0]

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']

cost_step = 1

def compute_value(grid,goal,cost):
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
					for a in range(len(delta)):
						x2 = x + delta[a][0]
						y2 = y + delta[a][1]

						if x2 >= 0 and x2 < len(grid) and y2 >= 0 and y2 < len(grid[0]) and grid[x2][y2]==0:
							v2 = value[x2][y2] + cost_step

							if v2 < value[x][y]:
								change = True
								value[x][y] = v2
			# print value

	return value 

print compute_value(grid, goal, cost)