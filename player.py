from constants import Resources, DevCard, Structures

class Player(object):	
	def __init__(self, name):
		self.name = name;
		self.victory_points = 0
		self.num_cards = 0
		self.cards = {Resources.WOOD:0, Resources.BRICK:0, Resources.SHEEP:0, Resources.WHEAT:0, Resources.STONE:0}
		self.dev_cards = {DevCard.KNIGHT:0, DevCard.ROAD_BUILDING:0, DevCard.MONOPOLY:0, DevCard.YEAR_OF_PLENTY:0,
						  DevCard.CHAPEL:0, DevCard.LIBRARY: 0, DevCard.UNIVERSITY: 0, DevCard.MARKET: 0, DevCard.PALACE: 0}
		self.VP_dev_cards = 0
		self.roads = zip(range(54), [[] for _ in range(54)])
		self.brickR = 4
		self.stoneR = 4
		self.wheatR = 4
		self.woodR = 4
		self.sheepR = 4
		self.road = 0
		self.longest_ROAD = False;
		self.largest_ARMY = False;
		
		self.num_cities = 0
		self.num_settlements = 0
		self.num_roads = 0
	
	def get_cards(self, resource, amount):
		self.cards[resource] += amount
		self.num_cards += amount
	
	def update_robber(self):
		if self.num_cards > 7 :
			#interaction with UI
			return
	
	def build_structure(self, structure):
		return 1
		#TODO
		
	def DFS(G, v, seen = None, path = None):
		if seen is None: seen = []
		if path is None: path = [v]

		seen.append(v)

		paths = []
		for t in G[v]:
			if t not in seen:
				t_path = path + [t]
				paths.append(tuple(t_path))
				paths.extend(DFS(G, t, seen[:], t_path))
		return paths
		
	def get_longest_road(G):
		all_paths = DFS(G, '1')
		max_len   = max(len(p) for p in all_paths)
		return max_len

		
	
	