import random
import pygame

ORIGIN = (351.96, 263.065)
HORIZ, VERT = 47.5/2, 27.4/2
up = (HORIZ, -VERT)
down = (-HORIZ, VERT)
left = (-HORIZ, -VERT)
right = (HORIZ, VERT)
stay = (0, 0)

#setup window
pygame.init()
screen = pygame.display.set_mode((750, 700))
pygame.display.set_caption("Balloono")

#load images
background = pygame.image.load('background.png')
bubble = pygame.image.load('bubble.png')
splash = pygame.image.load('splash.png')
red_up = pygame.image.load('red_up.png')
red_down = pygame.image.load('red_down.png')
red_left = pygame.image.load('red_left.png')
red_right = pygame.image.load('red_right.png')
white_up = pygame.image.load('white_up.png')
white_down = pygame.image.load('white_down.png')
white_left = pygame.image.load('white_left.png')
white_right = pygame.image.load('white_right.png')

class Board(object):
    """ A 17 x 11 board """
    board = []
    width = 11
    height = 11

    def __init__(self):
        """ Creates a 11 x 11 board of Place objects and fills them with the initial stones and bricks """
        if self.width < 11 or self.height < 11 or self.width % 2 == 0 or self.height % 2 == 0:
            raise Exception
        self.brick_count = 0
        Board.board = [[Place(x, y) for x in range(self.width)] for y in range(self.height)]
        self.places = []
        for x in range(self.width):
            for y in range(self.height):
                self.places.append((x, y))
                place = self.board[y][x]
                if x % 2 == 1 and y % 2 == 1:
                    place.add_obj(Stone(place))
                elif x == 0 or x == self.width-1:
                    if y <= 1 or y >= self.height-2:
                        continue
                    if abs(y - self.height/2) <= 1:
                        place.add_obj(Brick(place))
                        self.brick_count += 1
                elif y == 0 or y == self.height-1:
                    if x <= 1 or x >= self.width-2:
                        continue
                    if abs(x - self.width/2) <= 1:
                        place.add_obj(Brick(place))
                        self.brick_count += 1
                else:
                    r = random.random() 
                    if r <= 0.85:
                        place.add_obj(Brick(place))
                        self.brick_count += 1
        self.places = sorted(self.places, key=lambda tup: tup[0] + tup[1])
        self.monkeys = [Monkey(self.board[0][0], red_right), Monkey(self.board[self.height-1][self.width-1], white_left)]


class Place(object):
    """ A spot on the board with x and y coordinates and potentially an object, powerup, and monkeys """
    def __init__(self, x, y):
        self.monkey = None
        self.powerup = None
        self.obj = None
        self.splash = None
        self.x = x
        self.y = y
        self.pos = (ORIGIN[0] + (self.x - self.y) * HORIZ, ORIGIN[1] + (self.x + self.y) * VERT)

    def add_obj(self, obj):
        if isinstance(obj, Powerup):
            self.powerup = obj
        elif isinstance(obj, Monkey):
            self.monkey = obj
        elif isinstance(obj, Splash):
            self.splash = obj
        else: 
            self.obj = obj

    def remove_obj(self, obj):
        if isinstance(obj, Powerup):
            self.powerup = None
        elif isinstance(obj, Monkey):
            self.monkey = None
        elif isinstance(obj, Splash):
            self.splash = None
        else:
            self.obj = None


class Occupant(object):
    """ Occupants take up a space on the board. There can only be one occupant in a space at a time """
    def __init__(self):
        return


class Stone(Occupant):
    """ An occupant that does not break when splashed """
    def __init__(self, place):
        Occupant.__init__(self)
        self.img = pygame.image.load('stone.png')
        self.place = place


class Brick(Occupant):
    """ An occupant that breaks when splashed and may leave a powerup """
    def __init__(self, place):
        Occupant.__init__(self)
        self.img = pygame.image.load('brick.png')
        self.place = place
        r = random.random() * 100
        if r <= 13:
            self.powerup = Powerup("range", self.place)
        elif r <= 26:
            self.powerup = Powerup("balloons", self.place)
        elif r <= 39:
            self.powerup = Powerup("speed", self.place)
        else:
            self.powerup = None

    def splash(self):
        """ Remove the brick and leave any powerups it contains """
        board.brick_count -= 1
        self.place.remove_obj(self)
        if self.powerup:
            self.place.add_obj(self.powerup)


class Powerup(object):
    """ Powerups can occupy the same space as an occupant (a block, or a monkey) """
    def __init__(self, power, place):
        self.power = power
        self.place = place
        if self.power == "range":
            self.img = pygame.image.load('range_powerup.png')
        elif self.power == "balloons":
            self.img = pygame.image.load('balloon_powerup.png')
        else:
            self.img = pygame.image.load('speed_powerup.png')

    def remove(self):
        """ Remove the powerup when picked up """
        self.place.remove_obj(self)


class Monkey(object):
    """ Monkey controlled by a player that moves around and drops balloons """
    def __init__(self, place, img):
        self.img = img
        self.rng = 1
        self.speed = 5 #large numbers = slow
        self.balloons = 1
        self.bubble = 0
        self.place = place
        self.place.monkey = self
        self.coordinates = (self.place.x, self.place.y)
        self.pos = place.pos
        self.change = (0, 0)
        self.lost = False

    def move(self):
        """ Handles monkey movements if they are valid based upon surroundings.
        Also handles any powerups or popping bubbled monkeys """
        if self.change == stay:
            return
        if self.bubble:
            return
        new_pos = (self.pos[0] + self.change[0]/self.speed, self.pos[1] + self.change[1]/self.speed)
        y = (new_pos[1] - ORIGIN[1]) / (VERT * 2) + (ORIGIN[0] - new_pos[0]) / (HORIZ * 2)
        x = (1 / HORIZ) * (new_pos[0] - ORIGIN[0]) + y
        if y >= 10.2 or x >= 10.2 or y < -0.3 or x < -0.3:
            return
        new_place = Board.board[round(y)][round(x)]
        if new_place.monkey and new_place.monkey.bubble:
            new_place.monkey.pop()
        elif (new_place == self.place) or (not new_place.obj and not new_place.monkey):
            if new_place != self.place:
                self.place.monkey = None
                new_place.monkey = self
                self.place = new_place
            self.pos = new_pos
            if self.place.powerup:
                self.get_powerup(self.place.powerup)

    def get_powerup(self, powerup):
        """ Processes the powerup on that spot and removes it """
        if powerup.power == "range":
            if self.rng < 11:
                self.rng += 1
        elif powerup.power == "balloons":
            self.balloons += 1
        elif powerup.power == "speed":
            if self.speed > 1:
                self.speed -= 0.5
        powerup.remove()

    def drop_balloon(self):
        """ Drops a balloon if there are any """
        if not self.bubble and self.balloons:
            self.balloons -= 1
            Balloon(self.rng, self.place, self)

    def splash(self):
        """ Splashes the monkey and puts it in a bubble if it isn't already in one """
        if not self.bubble:
            self.bubble = pygame.time.get_ticks() + 5000

    def tick(self):
        if self.bubble < pygame.time.get_ticks():
            self.bubble = 0

    def pop(self):
        """ Removes the monkey if it is popped while in a bubble """
        if self.bubble:
            self.place.monkey = None
            self.lost = True
            return

class Balloon(Occupant):
    """ An exploding balloon that splashes nearby objects """
    def __init__(self, rng, place, monkey):
        """ Balloon is rendered, there is a delay while it gets ready to explode """
        Occupant.__init__(self)
        self.rng = rng
        self.monkey = monkey
        self.place = place
        self.place.add_obj(self)
        self.img = pygame.image.load('balloon.png')
        self.counter = 70
        self.splashed = False

    def tick(self):
        if not self.counter:
            self.splash()
        else:
            self.counter -= 1

    def splash(self):
        """ Balloon pops and splashes nearby objects """
        self.splashed = True
        self.monkey.balloons += 1
        reach = [-1] * 4 #represents [up, down, left, right]
        x, y = self.place.x, self.place.y
        def splash_spot(x, y, d, i):
            if x < 0 or y < 0 or x >= Board.width or y >= Board.height:
                reach[d] = i - 1
                return
            p = Board.board[y][x]
            if not p.obj and not p.monkey:
                p.add_obj(Splash(p))
            if p.obj:
                if isinstance(p.obj, Stone):
                    reach[d] = i-1
                elif isinstance(p.obj, Brick):
                    p.obj.splash()
                    p.add_obj(Splash(p))
                    reach[d] = i
                elif isinstance(p.obj, Balloon):
                    if not p.obj.splashed:
                        p.obj.splash()
                    reach[d] = i
            if p.monkey:
                p.monkey.splash()
                p.add_obj(Splash(p))
        if self.place.monkey:
            self.place.monkey.splash()
        self.place.add_obj(Splash(p))
        for i in range(1, self.rng + 1):
            if reach[0] == -1:
                splash_spot(x, y - i, 0, i)
            if reach[1] == -1:
                splash_spot(x, y + i, 1, i)
            if reach[2] == -1:
                splash_spot(x - i, y, 2, i)
            if reach[3] == -1:
                splash_spot(x + i, y, 3, i)
        self.place.remove_obj(self)

class Splash(Occupant):
    """ The splash from a balloon """
    def __init__(self, place):
        self.place = place
        self.counter = 5
        self.img = splash
    
    def tick(self):
        if self.counter:
            self.counter -= 1
        else:
            self.place.remove_obj(self)
        


###############################################
############### GAME OPERATIONS ###############
###############################################

#game setup
screen.blit(background, (0, -50))
board = Board()
p1 = board.monkeys[0]
p2 = board.monkeys[1]

pygame.display.update()

#game loop
running = True 
while running: 
    screen.blit(background, (0, -50))
    if p1.lost:
        print("p2 wins!")
    elif p2.lost:
        print("p1 wins!")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    p1.change = up
                    p1.img = red_up
                elif event.key == pygame.K_DOWN:
                    p1.change = down
                    p1.img = red_down
                elif event.key == pygame.K_LEFT:
                    p1.change = left
                    p1.img = red_left
                elif event.key == pygame.K_RIGHT:
                    p1.change = right
                    p1.img = red_right
                elif event.key == pygame.K_SPACE:
                    p1.drop_balloon()
                if event.key == pygame.K_w:
                    p2.change = up
                    p2.img = white_up
                elif event.key == pygame.K_s:
                    p2.change = down
                    p2.img = white_down
                elif event.key == pygame.K_a:
                    p2.change = left
                    p2.img = white_left
                elif event.key == pygame.K_d:
                    p2.change = right
                    p2.img = white_right
                elif event.key == pygame.K_z:
                    p2.drop_balloon()   
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    if p1.change == up:
                        p1.change = stay
                elif event.key == pygame.K_DOWN:
                    if p1.change == down:
                        p1.change = stay
                elif event.key == pygame.K_LEFT:
                    if p1.change == left:
                        p1.change = stay
                elif event.key == pygame.K_RIGHT:
                    if p1.change == right:
                        p1.change = stay
                if event.key == pygame.K_w:
                    if p2.change == up:
                        p2.change = stay
                elif event.key == pygame.K_s:
                    if p2.change == down:
                        p2.change = stay
                elif event.key == pygame.K_a:
                    if p2.change == left:
                        p2.change = stay
                elif event.key == pygame.K_d:
                    if p2.change == right:
                        p2.change = stay
    p1.move()
    p2.move()
    for tup in board.places:
        p = board.board[tup[0]][tup[1]] 
        if p.obj:
            screen.blit(p.obj.img, p.pos)
            if isinstance(p.obj, Balloon):
                p.obj.tick()
        elif p.powerup:
            screen.blit(p.powerup.img, p.pos)
        if p.monkey:
            screen.blit(p.monkey.img, p.monkey.pos)
            if p.monkey.bubble:
                screen.blit(bubble, p.monkey.pos)
                p.monkey.tick()
        if p.splash: 
            screen.blit(p.splash.img, p.pos)
            p.splash.tick()
    pygame.display.update()
pygame.quit()