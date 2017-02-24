'''
A visual demonstration of Breadth First Search Algorithm
using Pygame.
''' 
import time
from copy import deepcopy
from gridworld import GridWorld

grid = [[0 for col in range(10)] for row in range(10)]
init = [0, 0]
goal = [9, 9]
cell_width = 45
cell_height = 45
screen_size = 500
cell_margin = 5

grid_world = GridWorld(screen_size,cell_width,cell_height, cell_margin, init, goal, grid)

def check_valid(node):
    if node[0] >= 0 and node[0] < len(grid) and node[1] >= 0  and node[1] < len(grid[0]) and (grid[node[0]][node[1]] == 0 or grid[node[0]][node[1]] == 10):
        return True
    else:
        return False

def run_bfs(init, goal, grid,cost, find_path):
    delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 0, 1 ], # go down
         [ 1, 0]] # go right
    delta_name = ['^', '<', 'v', '>']
    action = [[-1 for row in range(len(grid[0]))] for col in range(len(grid))]
    policy = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]

    next = None
    visited = []
    opened = []
    opened.append([0, init])
    visited.append(init)
    opened.sort()
    opened.reverse()
    next = opened.pop()
    came_from = []
    while next[1]!= goal:
        temp = []
        # print "expanding node :",next[1]
        # print "neighboring nodes: "
        for d in range(len(delta)):
            x = next[1][0] + delta[d][0]
            y = next[1][1] + delta[d][1]

            if check_valid([x, y]):
                if [x, y] not in visited:
                    opened.append([next[0]+cost, [x, y]])
                    visited.append([x, y])
                    temp.append([next[0]+cost, [x, y]])
                    action[x][y] = d
                    
        # print temp
        grid_world.draw_cell(temp)
        grid_world.show()
        time.sleep(0.1)
        if(len(opened)>0):
            next = opened.pop(0)
    
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

    if find_path:
        # newpath = deepcopy(path)
        smooth_path = grid_world.smooth_path(path)
        grid_world.draw_path(smooth_path)
        grid_world.show()
    

run_bfs(init, goal, grid, cost=1, find_path=True)

