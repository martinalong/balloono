import random

board = []
brickCount = 0
monkeys

class Board(object):
	""" A minimum 11 x 11 board (odd sides only) """
	def __init__(self, players, dimensions=(13, 11)):
		""" Create a board with (x, y) dimensions
			0 represents an empty space 
		"""
		fillBoard(dimensions)
		#make monkeys and place them

	def fillBoard(self, dimensions):
		""" Fills the board with the initial stones and bricks """
		self.width, self.height = dimensions[0], dimensions[1]
		if width < 11 or height < 11 or width % 2 == 0 or height % 2 == 0:
			raise Exception
		global board
		global brickCount
		board += [[Place(x, y) for x in self.width] for y in self.height]
		for x in range(self.width):
			for y in range(self.height):
				place = board[y][x]
				if x % 2 == 1 and y % 2 == 1:
					place.addObj(Stone(place))
				elif x == 0 or x == self.width-1:
					if y <= 1 or y >= self.height-2:
						continue
					elif abs(y - self.height/2) <= 1:
						place.addObj(Brick(place))
						brickCount += 1
				elif y == 0 or y == self.height-1:
					if x <= 1 or x >= self.width-2:
						continue
					elif abs(x - self.width/2) <= 1:
						place.addObj(Brick(place))
						brickCount += 1
				else:
					r = random.random() 
					if r <= 0.75:
						place.addObj(Brick(place))
						brickCount += 1
		self.players = [Monkey(board[0][0]), Monkey(board[0][width]), Monkey(board[height][0]), Monkey(board[height][width])]
		#later, figure out how to make monkey bots and move them (maybe call ltheir move function every turn?)

	def runGame(self):
		while (true):
			if brickCount == 0:
				#initiate bricks closing in. If brick falls on monkey, it dies
			if monkeyCount == 1:
				#initiate win sequence for that monkey
			#turn keystrokes into monkey.move, and can only move if there's no obstacle there
			if key == "DOWN" and self.players[0]:
				self.players[0]



class Place(object):
	def __init__(self, x, y):
		self.monkeys = []
		self.powerup = None
		self.obj = None
		self.x = x
		self.y = y

	def addObj(self, obj):
		if type(obj) == Monkey:
			self.monkeys.append(obj)
		elif type(obj) == Occupant:
			self.obj = obj
		elif type(obj) == Powerup:
			self.powerup = obj

	def removeObj(self, obj):
		if type(obj) == Monkey:
			self.monkeys.remove(obj)
		elif type(obj) == Occupant:
			self.obj = None
		elif type(obj) == Powerup:
			self.powerup = None


class Stone(Occupant):
	def __init__(self, place):
		#draw stone in that spot


class Brick(Occupant):
	def __init__(self, place):
		#draw brick in that spot
		self.place = place
		r = random.random() * 10
		if r <= 1:
			self.powerup = "range"
		elif r <= 2:
			self.powerup = "balloons"
		elif r <= 3:
			self.powerup == "speed"
		else:
			self.powerup = None

	def splash(self):
		#delete image
		#leave a powerup in the place 
		global brickCount
		brickCount -= 1
		self.place.removeObj(self)
		if self.powerup:
			self.place.addObj(self.powerup)
			self.powerup.show()


class Powerup(object):
	""" Powerups can occupy the same space as an occupant (a block, or a monkey) """
	def __init__(self, type, place):
		self.type = type
		#do not show (not until brick is splashed)

	def show(self):
		#draw the powerup depending on the type

	def remove(self):
		self.place.removeObj(self)
		#undraw the powerup

class Occupant(object):
	""" Occupants take up a space on the board. There can only be one occupant in a space at a time """

class Monkey(object):
	def __init__(self, place):
		self.rng = 1
		self.speed = 1
		self.balloons = 1
		self.bubble = False
		self.place = place

	def move(self, x, y):
		#handles the frame changes and then reassigns x and y
		#gets called from some game engine watching keystrokes
		#i think in this method will be where speed is applied
		if self.bubble:
			return
		global board
		self.place = board[y][x]
		#animate movement
		if self.place.powerup:
			getPowerup(self.place.powerup)
		if (self.place.monkeys):
			for monkey in self.place.monkeys:
				monkey.pop() #does nothing if not in a bubble

	def getPowerup(self, powerup):
		""" Processes the powerup on that spot and removes it """
		if powerup.type == "range":
			self.rng += 1
		elif powerup.type == "balloons":
			self.balloons += 1
		elif powerup.type == "speed":
			self.speed += 1
		powerup.remove()


	def dropBalloon(self):
		if self.balloons:
			self.balloons -= 1
			self.place.addObj(Balloon(self.rng, self.place, self))

	def splash(self):
		if !self.bubble:
			self.bubble = True
			#animate bubble monkey
			#delay time, then unbubble

	def pop(self):
		if self.bubble:
			#undraw the monkey
			global monkeyCount
			monkeyCount -= 1

class MonkeyBot(Monkey):
	def __init__(self, place):
		Monkey.__init__(self, place)

	def strategy():
		""" Dictates how the bot moves and drops balloons """

class Balloon(Occupant):
	def __init__(self, rng, place, monkey):
		""" Balloon is rendered, there is a delay while it gets ready to explode """
		#draw the balloon on that place. few seconds delay, animate bouncing
		self.rng = rng
		self.monkey = monkey
		self.splash()

	def splash(self):
		""" Balloon pops and splashes nearby objects """
		reach = [-1] * 4 #represents [up, down, left, right]
		x, y = self.place.x, self.place.y
		def splashSpot(x, y, d, i):
			if reach[d] == -1:
				if y-i == 0:
					reach[d] = i
				obj = board[y][x].obj
				if obj:
					if (type(obj) == Stone):
						reach[d] = i-1
					elif (type(obj) == Brick):
						obj.splash()
						reach[d] = i
				for monkey in board[y][x].monkeys:
					monkey.splash()
			#animate the splash in here?
		for i in range(1, self.rng + 1):
			splashSpot(x, y - i, 0, i)
			splashSpot(x, y + i, 1, i)
			splashSpot(x - i, y, 2, i)
			splashSpot(x + i, y, 3, i)
		#use reach to animate the splash (and if a value is -1, that means it is the full i)
		#also animate the pop for a second and remove the balloon
		self.monkey.balloons += 1



