from player import Player
import random
import math
from constants import Resources, DevCard, Ports, Structures

class board_piece(object):
	def __init__(self, resource, number, robber):
		self.resource = resource
		self.number = number
		self.robber = robber
	
	def remove_robber(self):
		self.robber = False
	
	def place_robber(self):
		self.robber = True
		
class building(object):
	def __init__(self, player, structure):
		self.occupied = False
		self.player = player
		self.structure = structure
	
	def place(self, player, structure):
		self.occupied = True
		self.player = player
		self.structure = structure

class game(object):
	def __init__(self, num_players, rad, offset, names):
		heightT = math.sqrt(3)*rad
		widthT = rad
		hex_numbers = [2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 10, 10, 11, 11, 12, 7]
		hex_resources = [Resources.WOOD, Resources.WOOD, Resources.WOOD, Resources.WOOD, 
						 Resources.BRICK, Resources.BRICK, Resources.BRICK,         
		       			 Resources.WHEAT, Resources.WHEAT, Resources.WHEAT, Resources.WHEAT, 
						 Resources.STONE, Resources.STONE, Resources.STONE,
						 Resources.SHEEP, Resources.SHEEP, Resources.SHEEP, Resources.SHEEP,
						 Resources.DESERT]
		self.ports = [Ports.THREE_FOR_ONE, Ports.THREE_FOR_ONE, Ports.THREE_FOR_ONE, Ports.THREE_FOR_ONE, 
		              Ports.MORE_WOOD, Ports.BRICK_ME, Ports.WAKE_UP_SHEEPLE, Ports.HAY_IS_FOR_HORSES, Ports.BRB_GETTING_STONED]
		self.dev_cards = [DevCard.KNIGHT, DevCard.KNIGHT, DevCard.KNIGHT, DevCard.KNIGHT, DevCard.KNIGHT, DevCard.KNIGHT, DevCard.KNIGHT,
		                  DevCard.KNIGHT, DevCard.KNIGHT, DevCard.KNIGHT, DevCard.KNIGHT, DevCard.KNIGHT, DevCard.KNIGHT, DevCard.KNIGHT,
					      DevCard.ROAD_BUILDING, DevCard.ROAD_BUILDING, DevCard.MONOPOLY, DevCard.MONOPOLY,
					      DevCard.YEAR_OF_PLENTY, DevCard.YEAR_OF_PLENTY, DevCard.CHAPEL, DevCard.LIBRARY,
					      DevCard.UNIVERSITY, DevCard.MARKET, DevCard.PALACE]
		self.resources = {Resources.WOOD:19, Resources.BRICK:19, Resources.SHEEP:19, Resources.WHEAT: 19, Resources.STONE: 19}
		random.shuffle(hex_numbers)
		random.shuffle(hex_resources)
		random.shuffle(self.ports)
		random.shuffle(self.dev_cards)
		
		a = hex_resources.index(Resources.DESERT)
		b = hex_numbers.index(7)
		if a != b:
			hex_numbers[a], hex_numbers[b] = hex_numbers[b], hex_numbers[a]
		self.loc_robber = a
		self.board = []
		for x in range (19):
			self.board.append(board_piece(hex_resources[x], hex_numbers[x], x == self.loc_robber))
		
		self.players = []
		for x in range (num_players):
			self.players.append(Player(names[x]))
		
		self.buildings = []
		for x in range (54):
			self.buildings.append(building(0, Structures.NONE))
			
		self.adj = {1:[2, 30], 2:[1, 3], 3:[2, 4, 32], 4:[3, 5],  5:[4, 6, 34],
		            6:[5, 7],  7:[6, 8], 8:[7, 9, 35], 9:[8, 10], 10:[9, 11, 37],
					11:[10, 12], 12:[11, 13], 13:[12, 14, 38], 14:[13, 15], 15:[14, 16, 40],
					16:[15, 17], 17:[16, 18], 18:[17, 19, 41], 19:[18, 20], 20:[19, 21, 43],
					21:[20, 22], 22:[21, 23], 23:[22, 24, 44], 24:[23, 25], 25:[24, 26, 46],
					26:[25, 27], 27:[26, 28], 28:[27, 47, 29], 29:[28, 30], 30:[1, 29, 31],
					31:[30, 32, 48], 32:[3, 31, 33],  33:[32, 34, 50], 34:[5, 33, 35], 35:[8, 34, 36],
					36:[35, 37, 51], 37:[10, 36, 38], 38:[13, 37, 39], 39:[38, 40, 52], 40:[15, 39, 41], 
					41:[18, 40, 42], 42:[41, 43, 53], 43:[20, 42, 44], 44:[23, 43, 45], 45:[44, 46, 54],
					46:[25, 45, 47], 47:[28, 46, 48], 48:[31, 47, 49], 49:[48, 50, 54], 50:[33, 49, 51],
					51:[36, 50, 51], 52:[39, 51, 53], 53:[42, 52, 54], 54:[45, 49, 53]}
		
		self.vert = {1:[1, 2, 3, 30, 31, 32],    2:[28, 29, 30, 31, 47],     3:[25, 26, 27, 28, 46, 47], 
		             4:[23, 24, 25, 44, 45, 46], 5:[20, 21, 22, 23, 43, 44], 6:[18, 29, 20, 41, 42, 43], 
					 7:[15, 16, 17, 18, 40, 41], 8:[13, 14, 15, 38, 39, 40], 9:[10, 11, 12, 13, 37, 38], 
					 10:[8, 9, 10, 35, 36, 37],  11:[5, 6, 7, 8, 34, 35],    12:[3, 4, 5, 32, 33, 34],   
					 13:[31, 32, 33, 48, 49, 50], 14:[45, 46, 47, 48, 49, 54], 15:[42, 43, 44, 45, 53, 54], 
					 16:[39, 40, 41, 42, 52, 53], 17:[36, 37, 38, 39, 51, 52], 18:[33, 34, 35, 36, 50, 51], 
					 19:[49, 50, 51, 52, 53, 54]}

		self.pixelLoc = {1:[offset[0]-2*widthT, offset[1]-heightT*2],
						 2:[offset[0],          offset[1]-heightT*2],
						 3:[offset[0]+2*widthT, offset[1]-heightT*2],
						 4:[offset[0]+3*widthT, offset[1]-heightT],
						 5:[offset[0]+4*widthT, offset[1]],
						 6:[offset[0]+3*widthT, offset[1]+heightT],
						 7:[offset[0]+2*widthT, offset[1]+heightT*2],
						 8:[offset[0],          offset[1]+heightT*2],
						 9:[offset[0]-2*widthT, offset[1]+heightT*2],
						 10:[offset[0]-3*widthT, offset[1]+heightT],
						 11:[offset[0]-4*widthT, offset[1]],
						 12:[offset[0]-3*widthT, offset[1]-heightT],
						 13:[offset[0]-widthT,   offset[1]-heightT],
						 14:[offset[0]+widthT,   offset[1]-heightT],
						 15:[offset[0]+2*widthT, offset[1]],
						 16:[offset[0]+widthT,   offset[1]+heightT],
						 17:[offset[0]-widthT,   offset[1]+heightT],
						 18:[offset[0]-2*widthT, offset[1]],
						 19:[offset[0],          offset[1]]}
						 
		'''self.ports = {1:[29, 30], 2:[26, 27], 3:[23, 24], 4:[19, 20], 5:[16, 17],
		                 6:[13, 14], 7:[9, 10], 8:[6, 7], 9:[3, 4]}                   '''
		self.available_vert = [True] * 54
		
	def roll_die():
		return random.randint(1, 6) + random.randint(1, 6)
		
		
		