
'''
A visual demonstration of path smoothing
''' 
import pygame
import time
from copy import deepcopy
 
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# cell dimensions
WIDTH = 45
HEIGHT = 45
MARGIN = 5
 
pygame.init()
pygame.font.init()
 
# Set the width and height of the screen [width, height]
size = (500, 500)
screen = pygame.display.set_mode(size)

font=pygame.font.SysFont('arial', 20)
#text=font.render('@', True, (0, 0, 0))

pygame.display.set_caption("Grid world")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

row = 0
column = 0

init = [0, 0]
goal = [9, 9]
grid = []
policy = []
color = RED

def init_grid():
    for row in range(10):
        grid.append([])
        policy.append([])
        for column in range(10):
            grid[row].append(0)
            policy[row].append(' ')

    policy[goal[0]][goal[1]] = '*'
    policy[init[0]][init[1]] = 's'

    grid[init[0]][init[1]] = 1  # initial state
    grid[goal[0]][goal[1]] = 10 # goal state


    screen.fill(BLACK)

    for row in range(10):
        for column in range(10):
            color = WHITE
            if grid[row][column] == 1:
                color = GREEN
            elif grid[row][column] == 10:
                color = RED
            elif grid[row][column] == -10:
                color = BLACK
            pygame.draw.rect(screen, 
                color,
                [(MARGIN + WIDTH) * column + MARGIN,
                (MARGIN + HEIGHT) * row + MARGIN,
                WIDTH,
                HEIGHT])
    path = [[0, 0],
        [0, 1],
        [0, 2],
	[0, 3],
	[0, 4],
	[1, 4],
	[2, 4],
	[3, 4],
	[4, 4],
	[5, 4],
	[6, 4],
	[7, 4],
	[8, 4],
	[9, 4],
	[9, 5],
	[9, 6],
	[9, 7],
	[9, 8],
	[9, 9]]

    draw_path(path, BLUE)

def printpaths(path,newpath):
    for old,new in zip(path,newpath):
        print '['+ ', '.join('%.3f'%x for x in old) + \
               '] -> ['+ ', '.join('%.3f'%x for x in new) +']'

def draw_path(path, color):
	origin = [0+1*MARGIN+22.5,0+1*MARGIN+22.5]
	col = MARGIN + WIDTH
	row = MARGIN + HEIGHT
	pygame.draw.lines(screen, color, False, [(origin[0]+col*i[1], origin[1]+row*i[0]) for i in path], 4)
	clock.tick(60)
	pygame.display.flip()


# smoothing algorithm
def smooth(path, weight_data = 0.5, weight_smooth = 0.1, tolerance = 0.000001):

    # Make a deep copy of path into newpath
    newpath = deepcopy(path)

    change = tolerance

    while change >= tolerance:
        change = 0
        for i in range(1, len(path) - 1):
            for j in range(len(path[0])):
                d1 = weight_data*(path[i][j] - newpath[i][j])
                d2 = weight_smooth*(newpath[i-1][j] + newpath[i+1][j] - 2*newpath[i][j])
                change += abs(d1 + d2)
                newpath[i][j] += d1 + d2
                
    
    return newpath 

path = [[0, 0],
        [0, 1],
        [0, 2],
	[0, 3],
	[0, 4],
	[1, 4],
	[2, 4],
	[3, 4],
	[4, 4],
	[5, 4],
	[6, 4],
	[7, 4],
	[8, 4],
	[9, 4],
	[9, 5],
	[9, 6],
	[9, 7],
	[9, 8],
	[9, 9]]
        
# printpaths(path,smooth(path))

init_grid()

while True:
	draw_path(smooth(path), GREEN)
	


# Close the window and quit.
pygame.quit()
