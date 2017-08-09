import socket
import pygame
from game import game
import math
from player import Player
from constants import Resources

def coord_hexagon(radius, position):
		return [[position[0], position[1]-2*radius/math.sqrt(3)],
                [position[0]+radius, position[1]-radius/math.sqrt(3)],
                [position[0]+radius, position[1]+radius/math.sqrt(3)],
				[position[0], position[1]+2*radius/math.sqrt(3)],
				[position[0]-radius, position[1]+radius/math.sqrt(3)],
                [position[0]-radius, position[1]-radius/math.sqrt(3)]]
				
class Catan():
	def __init__(self):
		pass
		pygame.init();
		self.width, self.height, self.radius = 1000, 750, 60
		BLACK = (0,   0,   0)
		WHITE = (255, 255, 255)
		self.screen = pygame.display.set_mode((self.width, self.height))
		self.screen.fill(WHITE)
		wood = pygame.image.load('wood_final.png').convert_alpha()
		brick = pygame.image.load('brick_final.png').convert_alpha()
		sheep = pygame.image.load('sheep_final.png').convert_alpha()
		wheat = pygame.image.load('wheat_final.png').convert_alpha()
		stone = pygame.image.load('stone_final.png').convert_alpha()
		desert = pygame.image.load('desert_final.png').convert_alpha()
		self.board = pygame.image.load('board.png').convert_alpha()
		numbers = []
		for i in range(2, 13):
			numbers.append(pygame.image.load(str(i) + '.png').convert_alpha())
		self.tiles = dict(zip([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], numbers))
		self.images = {Resources.WOOD:wood, Resources.BRICK:brick, Resources.SHEEP:sheep,
					   Resources.WHEAT:wheat, Resources.STONE:stone, Resources.DESERT:desert}
		self.catan = game(4, self.radius, [self.width/2-30, self.height/2], ["Anna", "Bob", "Charlie", "David"])
		self.screen.blit(self.board, [69, 22])
		for i in range(19):
			self.screen.blit(self.images[self.catan.board[i].resource], [self.catan.pixelLoc[i+1][0]-self.radius, self.catan.pixelLoc[i+1][1]-self.radius*2/math.sqrt(3)])
			self.screen.blit(self.tiles[self.catan.board[i].number], [self.catan.pixelLoc[i+1][0]-14, self.catan.pixelLoc[i+1][1]-14])
		for i in range(19):
			pygame.draw.polygon(self.screen, WHITE, coord_hexagon(self.radius, self.catan.pixelLoc[i+1]), 4)
		
		self.hello = pygame.display.get_surface()
		self.new = pygame.Surface((1000, 750))

		#This is some weird 3D magic, don't mess with it plz :)
		'''for y in range (-self.height//2, self.height//2):
			for x in range (-self.width//2, self.width//2):
				horizon = 50 #adjust if needed
				fov = 10

				px = x;
				py = fov; 
				pz = y + horizon 
				
				if pz != 0:
					#projection 
					sx = px / pz
					sy = py / pz;

					scaling = 10; #adjust if needed, depends of texture size
					if round(sx * scaling) >= -self.width//2 and round(sx * scaling) < self.width//2 and round(sy * scaling) >= -self.height//2 and round(sy * scaling) < self.height//2:
						color = hello.get_at((round(sx * scaling) + self.width//2, round(sy * scaling) + self.height//2))
						self.new.set_at((x+self.width//2, y+self.height//2), color)'''
						
		#self.screen.fill(0)
		#self.screen.blit(self.new, [0, 0])
    
		pygame.display.set_caption("Catan")
		self.clock = pygame.time.Clock()
		print(pygame.display.list_modes())
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
	def update(self):
		#sleep to make the game 60 fps
		self.clock.tick(60)

		#clear the screen
		#self.screen.fill(0)
		#self.screen.blit(self.hello, [0, 0])
		
		for event in pygame.event.get():
			#quit if the quit button was pressed
			if event.type == pygame.QUIT:
				exit()

		#update the screen
		pygame.display.flip()
		
letsgo = Catan()
while 1:
    letsgo.update()
