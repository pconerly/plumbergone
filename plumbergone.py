import pygame
import os
import sys
from copy import deepcopy
from pygame.locals import *

#Global Game Settings
main_dir = os.path.split(os.path.abspath(__file__))[0]
width = 1024
height = 512
size = width, height
white = 255, 255, 255
black = 0, 0, 0
clock = pygame.time.Clock()
mainloop = True
FPS = 60
playtime = 0

#Grid Settings
cell_size = 35 #pixels
borderx = (width % cell_size) / 2 + cell_size
bordery = (height % cell_size) / 2 + cell_size
cell_count_x = (width - (2 * borderx)) / cell_size
cell_count_y = (height - (2 * bordery)) / cell_size

class gameboard():
	def __init__(self, x, y):
		self.grid = []
		self.new(x, y)
		self.previous = []
		self.lowest = []

	def new(self, x, y):
		for row in range(y):
			self.grid.append([])
			for column in range(x):
				self.grid[row].append(0)
	
	def pos(self, row, column):
		x = borderx + column * cell_size
		y = bordery + row * cell_size
		return x, y

	def row(self, y):
		return int((y - bordery) / cell_size)

	def column(self, x):
		return int((x - borderx) / cell_size)

	def add_pipe(self, player, column, row, entry, exit):
		self.grid[row][column] = [player, entry+exit]
		Pipe(self.pos(row, column))
		#print player, column, row, entry+exit
				
	def collision(self, x, y):
		row = (x - borderx) / cell_size
		column = (y - bordery) / cell_size
		if column < 0:
			return True
		elif row < 0:
			return True
		elif column >= len(self.grid):
			return True
		elif row >= len(self.grid[column]):
			return True
		if self.grid[column][row] != 0:
			return True
		else:
		   	return False
                       
	def store(self):
		gameboard.lowest = deepcopy(gameboard.previous)
		gameboard.previous = deepcopy(gameboard.grid)

board = gameboard(cell_count_x, cell_count_y)

#Image files
def load_image(image):
	"""Load the image and convert it to a surface."""
	image = os.path.join(main_dir, 'media', image)
	surface = pygame.image.load(image)
	return surface.convert()

player_image = "media/player.bmp"
pipe_image = "media/pipe.bmp"

screen = pygame.display.set_mode(size)

class player():
	def __init__(self, number, x, y, image):
		self.number = number
		self.image = pygame.image.load(image)
		self.image = pygame.Surface.convert(self.image)
		self.image.set_colorkey(white)

		#Screen placement
		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.centery = y
		self.x = x
		self.y = y
		self.velocity = [0, 0]
		self.speed = 85 #pixels a second

		#Grid placement
		self.entry = "center"
		self.previous_column = board.column(self.x)
		self.previous_row = board.row(self.y)
		self.current_column = self.previous_column
		self.current_row = self.previous_row

	def reset(self):
		self.velocity = [0, 0]
		self.rect.centerx = self.x
		self.rect.centery = self.y

	def movement(self, direction):
		"""Calculates the x and y directional velocities."""
		self.velocity[0] = self.speed * direction[0]
		self.velocity[1] = self.speed * direction[1]

	def status(self):
		"""Status checks the column and rows for changes, then places pipes."""
		self.current_column = board.column(self.x)
		self.current_row = board.row(self.y)

		if self.previous_column != self.current_column:
			#print "column", self.number, self.previous_column, self.current_column
			if self.previous_column > self.current_column:
				self.previous_entry = self.entry
				self.entry = 'right'
				board.add_pipe(self.number, self.previous_column,
							   self.current_row, self.entry, 
							   self.previous_entry)
				self.previous_column = self.current_column
			else:
				self.previous_entry = self.entry
				self.entry = 'left'
				board.add_pipe(self.number, self.previous_column,
							   self.current_row, self.entry, 
							   self.previous_entry)
				self.previous_column = self.current_column

		if self.previous_row != self.current_row:
			#print "row", self.number, self.previous_row, self.current_row
			if self.previous_row > self.current_row:
				self.previous_entry = self.entry
				self.entry = 'down'
				board.add_pipe(self.number, self.current_column,
							   self.previous_row, self.entry, 
							   self.previous_entry)
				self.previous_row = self.current_row
			else:
				self.previous_entry = self.entry
				self.entry = 'up'
				board.add_pipe(self.number, self.current_column,
							   self.previous_row, self.entry, 
							   self.previous_entry)
				self.previous_row = self.current_row

class Pipe(pygame.sprite.Sprite):
	images = []
	def __init__(self, pos):
		pygame.sprite.Sprite.__init__(self, self.containers)
		self.image = self.images[0]
		self.rect = self.image.get_rect(topleft=pos)
		#print "New pipe at", pos[0], pos[1]
"""
class Score(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.font = pygame.font.Font(None, 20)
		self.color = black
		self.update()
		self.rect = self.image.get_rect().move(0, 0)
"""

#Establish players and starting positions
startx1 = borderx + (cell_size / 2)
starty1 = bordery + (cell_size / 2)
startx2 = width - startx1
starty2 = height - starty1
player1 = player(1, startx1, starty1, player_image)
player2 = player(2, startx2, starty2, player_image)
playerlist = [player1, player2]

#Control Scheme
player1.up = K_UP
player1.down = K_DOWN
player1.left = K_LEFT
player1.right = K_RIGHT

player2.up = K_w
player2.down = K_s
player2.left = K_a
player2.right = K_d

def main():
	"""
	pygame.init()
	"""
	pass

screen.fill(white)

Pipe.images = [load_image('pipe.bmp')]

pipes = pygame.sprite.Group()
all = pygame.sprite.Group()

Pipe.containers = pipes, all

while mainloop:
    #Calculate time.
	milliseconds = clock.tick(FPS)
	seconds = milliseconds / 1000.0
	playtime += seconds
	
	#Watch for key events.
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		if event.type == pygame.KEYDOWN:
			keystate = pygame.key.get_pressed()
			for players in playerlist:
				if keystate[players.up]:
					players.movement([0, -1])
				elif keystate[players.down]:
					players.movement([0, 1])
				elif keystate[players.right]:
					players.movement([1, 0])
				elif keystate[players.left]:
					players.movement([-1, 0])
			if keystate[K_g]:
				print board.grid

	#Display FPS
	pygame.display.set_caption("[FPS]: %.2f" % clock.get_fps())

	#Calculate player movement
	for players in playerlist:
		if not board.collision(int(players.x), int(players.y)):
			players.x += players.velocity[0] * seconds
			players.y += players.velocity[1] * seconds
			players.rect.centerx = players.x
			players.rect.centery = players.y
		players.status()
		screen.blit(players.image, players.rect)
	pygame.display.flip()  
	
	dirty = pipes.draw(screen)
	pygame.display.update(dirty)
