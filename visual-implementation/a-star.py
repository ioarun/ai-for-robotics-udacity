# A visual demonstration of A* search algorithm

from gridworld import GridWorld
import time

# build grid structure
grid = [[0 for col in range(10)] for row in range(10)]
grid[0][1] = 1 # obstacle
grid[1][1] = 1 # obstacle
grid[2][1] = 1 # obstacle
grid[3][1] = 1 # obstacle
grid[4][4] = 1 # obstacle

init = [0, 0]
goal = [4, 5]

# build heuristics grid
heuristics = [[0 for col in range(len(grid[0]))] for row in range(len(grid))]
k = len(grid[0]) - 1
for i in range(len(grid)-1, -1, -1):
	num = (len(grid[0])-1) - k
	for j in range(len(grid[0])-1, -1, -1):
		heuristics[i][j] = num
		num += 1
	k -= 1

screen_size = 500
cell_width = 45
cell_height = 45
cell_margin = 5

gridworld = GridWorld(screen_size,cell_width, cell_height, cell_margin,init, goal, grid)

def check_valid(node, grid):
    if node[0] >= 0 and node[0] < len(grid) and node[1] >= 0  and node[1] < len(grid[0]) and (grid[node[0]][node[1]] == 0):
        return True
    else:
        return False

def heuristic(a, b):
	return (abs(a[0] - b[0]) + abs(a[1] - b[1]))

def run_a_star(grid, heuristics, init, goal, cost):
	delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1]] # go right
	delta_name = ['^', '<', 'v', '>']  
	action = [[-1 for row in range(len(grid[0]))] for col in range(len(grid))]
	policy = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]
	expanded = [[-1 for row in range(len(grid[0]))] for col in range(len(grid))]

	visited = []
	opened = []

	# [f, g, [x, y]] 
	# f = g + heuristics[x][y]
	# opened.append([0+heuristics[init[0]][init[1]], 0, init[0], init[1]])
	opened.append([heuristic(goal, init), 0, init[0], init[1]])

	visited.append([init[0], init[1]])
	next = opened.pop()
	count = 0
	
	while [next[2],next[3]] != goal:

		if len(opened) > 0:
			opened.sort()
			print opened
			opened.reverse()
			next = opened.pop()

		x = next[2]
		y = next[3]
		g = next[1]
		f = next[0]
		gridworld.draw_cell([[f, [x, y]]])
		gridworld.show()
		time.sleep(0.5)
		expanded[next[2]][next[3]] = count
		count += 1
		for a in range(len(delta)):
			x2 = x + delta[a][0]
			y2 = y + delta[a][1]
		
			if check_valid([x2, y2], grid):
				g2 = g + cost
				if [x2, y2] not in visited:
					#f = g2 + heuristics[x2][y2]
					f = g2 + heuristic(goal, [x2, y2])
					opened.append([f,g2,x2, y2])
					visited.append([x2, y2])
					action[x2][y2] = a
		
	print expanded
	# policy search
	x = goal[0]
	y = goal[1]
	policy[x][y] = '*'
	path = []
	path.append([x, y])
	while([x, y] != init):
		x1 = x - delta[action[x][y]][0]
		y1 = y - delta[action[x][y]][1]
		policy[x1][y1] = delta_name[action[x][y]]
		x = x1
		y = y1
		path.append([x, y])
	print policy
	path.reverse()
	print path
	smooth_path = gridworld.smooth_path(path)
	gridworld.draw_path(smooth_path)
	gridworld.show()

run_a_star(grid, heuristics, init, goal, cost=1)





