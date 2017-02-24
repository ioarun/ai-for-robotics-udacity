import pygame
import time
from copy import deepcopy

class GridWorld:

	def __init__(self, screen_size,cell_width, 
		cell_height, cell_margin,init, goal, grid):

		# define colors
		self.BLACK = (0, 0, 0)
		self.WHITE = (255, 255, 255)
		self.GREEN = (0, 255, 0)
		self.RED = (255, 0, 0)
		self.BLUE = (0, 0, 255)
		self.YELLOW = (255, 255, 0)

		# cell dimensions
		self.WIDTH = cell_width
		self.HEIGHT = cell_height
		self.MARGIN = cell_margin
		self.color = self.WHITE


		pygame.init()
		pygame.font.init()

		# set the width and height of the screen (width , height)
		self.size = (screen_size, screen_size)
		self.screen = pygame.display.set_mode(self.size)

		self.font = pygame.font.SysFont('arial', 20)

		pygame.display.set_caption("Grid world")

		self.clock = pygame.time.Clock()

		self.init = init
		self.goal = goal
		self.grid = grid


		self.screen.fill(self.BLACK)

		for row in range(len(grid)):
			for col in range(len(grid[0])):
				if [row, col] == self.init:
					self.color = self.GREEN
				elif [row, col] == self.goal:
					self.color = self.RED
				elif grid[row][col] == 1:
					self.color = self.BLACK
				else:
					self.color = self.WHITE
				pygame.draw.rect(self.screen,
					self.color,
					[(self.MARGIN + self.WIDTH)*col+self.MARGIN,
					(self.MARGIN + self.HEIGHT)*row+self.MARGIN,
					self.WIDTH,
					self.HEIGHT])

	def text_objects(self, text, font):
		textSurface = font.render(text, True, self.BLACK)
		return textSurface, textSurface.get_rect()

	def draw_cell(self, nodes):
		for node in nodes:
			row = node[1][0]
			column = node[1][1]
			value = node[0]
			rect = pygame.draw.rect(self.screen,
					self.BLUE,
					[(self.MARGIN + self.WIDTH)*column+self.MARGIN,
					(self.MARGIN + self.HEIGHT)*row+self.MARGIN,
					self.WIDTH,
					self.HEIGHT])
			TextSurf, TextRect = self.text_objects(str(value), self.font)
			TextRect.center = ((self.MARGIN + self.WIDTH)*column + 4*self.MARGIN,
				(self.MARGIN + self.HEIGHT)*row + 4*self.MARGIN)
			self.screen.blit(TextSurf, TextRect)


	def draw_path(self, path):
		origin = [0+1*self.MARGIN+22.5,0+1*self.MARGIN+22.5]
		col = self.MARGIN + self.WIDTH
		row = self.MARGIN + self.HEIGHT
		pygame.draw.lines(self.screen, self.GREEN, False, [(origin[0]+col*i[1], origin[1]+row*i[0]) for i in path], 4)

	# smoothen the path
	def smooth_path(self,path,weight_data = 0.5, weight_smooth = 0.1, tolerance = 0.000001):
		#newpath = return_path
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

	def show(self):
		self.clock.tick(60)
		pygame.display.flip()
			









