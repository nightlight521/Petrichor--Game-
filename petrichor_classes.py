##############################
# Title: Petrichor classes   #
# Author: Paula Yuan         #
# Date: dec. 25, 2018        #
##############################
import pygame
import time

BLACK     = (  0,  0,  0)                       
RED       = (255,  0,  0)                     
GREEN     = (  0,255,  0)                     
BLUE      = (  0,  0,255)                     
ORANGE    = (255,127,  0)               
CYAN      = (  0,183,235)
BROWN     = (  46,21,  9)
MAGENTA   = (255,  0,255)                   
YELLOW    = (255,255,  0)
WHITE     = (255,255,255)
GOLD      = (212, 175, 55)
BRIGHT_BLUE =(82, 239, 255)
DARK_BLUE = (12, 4, 45)
BROWN = (160, 82, 45)

def playSFX(sfx):
    sfx.set_volume(0.5)
    sfx.play(0)
    
def readLevel(level): # reads the entire level from a level file
    fileIN = open("level" + str(level) + ".txt", "r")
    bkgd = pygame.image.load("bkgd" + str(level) + ".jpg")
    platforms, levers, coins, walls, doors, symbols = [], [], [], [], [], []
    line = fileIN.readline()
    while line != "":
        line = line[0:-1]
        line = line.split()
        if line[0] == "0":
            level = int(line[1])
        if line[0] == "2":
            leverID = line[1]
            leverX = int(line[2])
            leverY = int(line[3])
            leverW = int(line[4])
            leverH = int(line[5])
            leverState = line[6]
            levers.append(Lever(leverID, leverX, leverY, leverW, leverH, leverState))
        elif line[0] == "1":
            platformX = int(line[1])
            platformY = int(line[2])
            platformW = int(line[3])
            platformH = int(line[4])
            if line[5] != "e":
                platforms.append(Platform(platformX, platformY, platformW, platformH, WHITE))
            if line[5] == "e":
                boundary1 = int(line[6])
                boundary2 = int(line[7])
                platforms.append(Elevator(platformX, platformY, platformW, platformH, WHITE, boundary1, boundary2))
        elif line[0] == "3":
            coinX = int(line[1])
            coinY = int(line[2])
            coinR = int(line[3])
            coins.append(Coin(coinX, coinY, coinR, GOLD))
        elif line[0] == "4":
            wallX = int(line[1])
            wallY = int(line[2])
            wallW = int(line[3])
            wallH = int(line[4])
            walls.append(Wall(wallX, wallY, wallW, wallH, WHITE))
        elif line[0] == "5":
            doorX = int(line[1])
            doorY = int(line[2])
            doorW = int(line[3])
            doorH = int(line[4])
            doorDir = line[5]
            numSymbols = int(line[6])
            symbols = []
            for i in range(numSymbols):
                line = fileIN.readline()
                line = line[0:-1]
                line = line.split()
                symbolX = int(line[0])
                symbolY = int(line[1])
                symbolType = line[2]
                symbolState  = line[3]
                symbolCorrectState = line[4]
                numLevers = int(line[5])
                symbols.append(Symbol(symbolX, symbolY, symbolType, symbolState, symbolCorrectState))
                for i in range(numLevers):
                    line = fileIN.readline()
                    line = line.strip()
                    for lever in levers:
                        if lever.leverID == line:
                            symbols[-1].levers.append(lever)
                            lever.symbols.append(symbols[-1])
            doors.append(Door(doorX, doorY, doorW, doorH, BROWN, symbols, doorDir))
        elif line[0] == "6":
            portalX = int(line[1])
            portalY = int(line[2])
            portalW = int(line[3])
            portalH = int(line[4])
            portal = Portal(portalX, portalY, portalW, portalH)
        elif line[0] == "7":
            startingOffsetX = int(line[1])
            startingOffsetY = int(line[2])
        elif line[0] == "8":
            startingX = int(line[1])
            startingB = int(line[2])
        line = fileIN.readline()
    currentLevel = Level(platforms, levers, coins, walls, doors, symbols, bkgd, portal, level, startingOffsetX, startingOffsetY, startingX, startingB)
    return currentLevel

class Character(object):
    """A sprite representing the protagonist of the game
       data:                               behaviour:
           x - x-coordinate of leftmost         detect collision with doors, walls, platforms, portals
           b - y-coordinate of bottommost       draw
           width - width of the sprite          detect whether in range to interact with levers
           height - height of the sprite
           groundLevel - ground level
           spriteV - vertical velocity
           spritePicNum - which picture to draw
           spriteDir - direction sprite is facing
           spritePic - the specific image to draw
    """
    def __init__(self, x, b):
        self.h = 100
        self.w = 100
        self.x = x
        self.b = b
        self.v = 0
        self.picNum = 0
        self.dir = "front"
        self.pic =[0]*8
        
    def draw(self, surface, offsetX, offsetY):
        surface.blit(self.pic[self.picNum], (self.x + offsetX, self.b - self.h + offsetY))

    def eatCoins(self, coins, points, sfx):
        x = self.x
        w = self.w
        b = self.b
        h = self.h
        if points < 1:
            points = 0
        for i in range(len(coins)-1, -1, -1):
            coinTop = coins[i].y - coins[i].r
            coinBottom = coins[i].y + coins[i].r
            coinRight = coins[i].x + coins[i].r
            coinLeft = coins[i].x - coins[i].r
            if (coinLeft < (x + w) and coinRight > x) and (coinTop < b and coinBottom > b - h):
                playSFX(sfx)
                coins.pop(i)
                points = points + 1
        return points
    
    def detectUp(self, platforms):
        middle = self.x + self.w/2
        x = self.x
        y = self.b - self.h
        b = self.b
        v = self.v
        for platform in platforms:
            platformRight = platform.x + platform.width
            platformB = platform.y + platform.height
            if ((y > platformB and y + v <= platformB) or (y <= platformB)) and y > platform.y - self.h and (middle < platformRight and middle > platform.x):
                if v < 0:
                    v = 0
                if v >= 0:
                    v = v + 2
        return v
            
    def detectDown(self, targets):
        middle = self.x + self.w/2
        x = self.x
        y = self.b - self.h
        b = self.b
        v = self.v
        for target in targets:
            targetRight = target.x + target.width
            targetB = target.y + target.height
            if b < target.y and b + v >= target.y and (middle < targetRight and middle > target.x):
                return target
            elif (b >= target.y and b < targetB)  and (middle < targetRight and middle > target.x):
                return target

    def detectWallsRight(self, walls):
        middle = self.x + self.w/2
        x = self.x
        y = self.b - self.h
        b = self.b
        right = self.x + self.w
        for wall in walls:
            wallB = wall.y + wall.height
            if (b <= wallB and y >= wall.y) and (right >= wall.x and x < wall.x):
                return True

    def detectWallsLeft(self, walls):
        x = self.x
        y = self.b - self.h
        b = self.b
        right = self.x + self.w
        for wall in walls:
            wallRight = wall.x + wall.width
            wallB = wall.y + wall.height
            if (b <= wallB and y >= wall.y) and (x <= wallRight and right > wallRight):
                return True

    def detectDoorsRight(self, doors):
        x = self.x
        y = self.b - self.h
        b = self.b
        right = self.x + self.w
        for door in doors:
            doorB = door.y + door.height
            if door.direction == "vertical":
                if (b <= doorB and b >= door.y) and (right >= door.x and x < door.x):
                    return True
            
    def detectDoorsLeft(self, doors):
        x = self.x
        y = self.b - self.h
        b = self.b
        right = self.x + self.w
        for door in doors:
            doorRight = door.x + door.width
            doorB = door.y + door.height
            if door.direction == "vertical":
                if (b <= doorB and y >= door.y) and (x <= doorRight and right > doorRight):
                    return True

    def detectDoorsUp(self, doors):
        b = self.b
        v = self.v
        y = self.b - self.h
        middle = self.x + self.w/2
        for door in doors:
            doorRight = door.x + door.width
            doorB = door.y + door.height
            if door.direction == "horizontal":
                if ((y > doorB and y + v <= doorB) or (y <= doorB)) and y > door.y - self.h and (middle < doorRight and middle > door.x):
                    if v < 0:
                        v = 0
                    if v >= 0:
                        v = v + 2
        return v
    
    def detectPortal(self, portal):
        x = self.x
        y = self.b - self.h
        b = self.b
        middle = self.x + self.w/2
        portalRight = portal.x + portal.width
        portalB = portal.y + portal.height
        if (b <= portalB and y >= portal.y) and (x <= portalRight and middle > portal.x):
            return True

    def detectFlip(self, targets, sfx): # detects whether in range to flip a lever and does so
        for target in targets:
            targetRight = target.x + target.width
            targetB = target.y + target.height
            if self.b in range(targetB - 10, targetB + 10) and (self.x + self.w >= target.x and self.x <= targetRight):
                playSFX(sfx)
                target.flip()

class Platform(object):
    """A piece of flooring
       data:                                   behaviour:
           x - x-coordinate of leftmost side        move left/right
           y - y-coordinate of uppermost side       draw
           width - width of the platform
           height - height of the platform
           clr - colour of the platform
    """
    def __init__(self, x, y, width, height, clr):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.clr = clr
        self.elevator = False
        
    def draw(self, surface, offsetX, offsetY):
        x = self.x
        y = self.y
        width = self.width
        height = self.height
        pygame.draw.rect(surface, self.clr, (x + offsetX, y + offsetY, width, height), 0)

class Elevator(Platform):
    """A vertical moving platform"""
    def __init__(self, x, y, width, height, clr, boundary1, boundary2): 
        Platform.__init__(self, x, y, width, height, clr)
        self.elevator = True
        self.boundary1 = boundary1
        self.boundary2 = boundary2
        self.speed = 5
        
    def move(self):
        if self.y > self.boundary1 or self.y < self.boundary2:
            self.speed = -self.speed
        self.y = self.y + self.speed
        return self.y

class Lever(object):
    """A toggle/switch
       data:                                          behaviour:
           x - x-coordinate of the leftmost side           draw
           y - y-coordinate of the uppermost side          switch pictures
           leverDir - direction the lever is pointing      open doors/unlock other game features
    """
    def __init__(self, leverID, x, y, width, height, state):
        self.leverID = leverID
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.state = state
        self.symbols = []

    def draw(self, surface, target, offsetX, offsetY):
        x = self.x
        y = self.y
        state = self.state
        if state == "off":
            leverPicNum = 0
        else:
            leverPicNum = 1
        surface.blit(target[leverPicNum], (x + offsetX, y + offsetY))

    def flip(self):
        if self.state == "off":
            self.state = "on"
        else:
            self.state = "off"
        for symbol in self.symbols:
            symbol.flip()
        

class Map(object):
    """The background for the level
       data:                              behaviour:
            x - x-coordinate of leftmost       draw
            y - y-coordinate of uppermost   
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, surface, target, offsetX, offsetY):
        x = self.x
        y = self.y
        surface.blit(target, (x + offsetX, y + offsetY))

class Wall(object):
    """A vertical platform
       data:                               behaviour:
           x - x-ccordinate of leftmost        draw
           y - y-coordinate of uppermost       move up/down
           width - width of the wall
           height - how tall the wall is
           clr - colour of the wall
    """
    def __init__(self, x, y, width, height, clr):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.clr = clr
        
    def draw(self, surface, offsetX, offsetY):
        x = self.x
        y = self.y
        width = self.width
        height = self.height
        pygame.draw.rect(surface, self.clr, (x + offsetX, y + offsetY, width, height), 0)

    def moveLeft(self):
        x = self.x
        x = x - 1

    def moveRight(self):
        x = self.x
        x = x + 1
        
    def moveUp(self):
        y = self.y
        y = y - 1
        
    def moveDown(self):
        y = self.y
        y = y + 1   

class Door(object):
    """A door into another area of the map
       data:                                    behaviour:
           x - x-coordinate of leftmost side        open (move left/right/up/down)
           y - y-coordinate of uppermost side       draw
           width - width of the platform
           height - height of the platform
           clr - colour of the platform
           symbols - symbol(s) assigned to that door
           dir - direction of opening
    """
    def __init__(self, x, y, width, height, clr, symbols, direction):
        self.initialWidth = width
        self.initialHeight = height
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.clr = clr
        self.symbols = symbols
        self.direction = direction

    def draw(self, surface, offsetX, offsetY):
        x = self.x
        y = self.y
        width = self.width
        height = self.height
        pygame.draw.rect(surface, self.clr, (x + offsetX, y + offsetY, width, height), 0)

    def isSolved(self):
        for symbol in self.symbols:
            if not symbol.isSolved():
                return False
        return True

    def maybeUnlock(self):
        direction = self.direction
        if self.isSolved():
            if direction == "horizontal":
                self.width = 10
            if direction == "vertical":
                self.height = 10
        else:
            self.height = self.initialHeight
            self.width = self.initialWidth

class Symbol(object):
    """A light that is/is part of a puzzle; all lights must be lighted in one area to unlock the next door
    data:                                              behaviour:
        x - x-coordinate of leftmost                       draw
        y - y-coordinate of uppermost                      determine picture to draw
        pos - correct position of corresponding lever
        kind - type of symbol
        picNum - different pictured states of each symbol
    """
    def __init__(self, x, y, kind, state, correctState):
        self.x = x
        self.y = y
        self.kind = kind
        self.levers = []
        self.state = state
        self.correctState = correctState

    def draw(self, surface, target, offsetX, offsetY,):
        x = self.x
        y = self.y
        state = self.state
        kind = self.kind
        if kind == "square1":
            if state == "on":
                picNum = 1
            else:
                picNum = 0
        if kind == "triangle1":
            if state == "on":
                picNum = 4
            else:
                picNum = 2
        if kind == "triangle2":
            if state == "on":
                picNum = 5
            else:
                picNum = 3
        if kind == "circle1":
            if state == "on":
                picNum = 7
            else:
                picNum = 6
        surface.blit(target[picNum], (x + offsetX, y + offsetY))
            
    def flip(self):
        if self.state == "on":
            self.state = "off"
        else:
            self.state = "on"
            
    def isSolved(self):
        return self.state == self.correctState

        
class Coin(object):
    """A small token to collect for points
    data:                                  behaviour:
        x - x-coordinate of leftmost           draw
        y - y-coordinate of uppermost          
        r - radius of the token
        clr - colour of the token
        points - how many collected so far
    """
    def __init__(self, x, y, r, clr):
        self.x = x
        self.y = y
        self.r = r
        self.clr = clr

    def draw(self, surface, offsetX, offsetY):
        x = self.x
        y = self.y
        r = self.r
        pygame.draw.circle(surface, self.clr, (x + offsetX, y + offsetY), r, 0)

class Portal(object):
    """A door leading to another level
    data:                               behaviour:
        x - x-coordinate of leftmost         draw   
        y - y-coordinate of uppermost
        width - width of the portal
        height - height of the portal
    """
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def draw(self, surface, target, offsetX, offsetY):
        x = self.x
        y = self.y
        surface.blit(target, (x + offsetX, y + offsetY))

class Level(object):
    """All the data for a level
       data:                              behaviour:
           platforms (list of objects)        draw
           levers  (list of objects)
           coins (list of objects)
           walls (list of objects)
           symbols (list of objects)
           portal (object)
           Background (background image to draw)
           level - what level it is
    """
    def __init__(self, platforms, levers, coins, walls, doors, symbols, background, portal, level, startingOffsetX, startingOffsetY, startingX, startingB):
        self.platforms = platforms
        self.levers = levers
        self.background = background
        self.coins = coins
        self.walls = walls
        self.doors = doors
        self.symbols = symbols
        self.portal = portal
        self.level = level
        self.COINS_TOTAL = len(coins)
        self.points = 0
        self.popped = False
        self.elapsed = 0
        self.startingOffsetX = startingOffsetX
        self.startingOffsetY = startingOffsetY
        self.startingX = startingX
        self.startingB = startingB
                 
    def draw(self, surface, leverPic, symbolPic, offsetX, offsetY, portalTarget):
        platforms = self.platforms
        levers = self.levers
        coins = self.coins
        walls = self.walls
        doors = self.doors
        portal = self.portal
        surface.blit(self.background, (offsetX, offsetY))
        for platform in platforms:
            platform.draw(surface, offsetX, offsetY)
        for lever in levers:
            lever.draw(surface, leverPic, offsetX, offsetY)
            for symbol in lever.symbols:
                symbol.draw(surface, symbolPic, offsetX, offsetY)
        for coin in coins:
            coin.draw(surface, offsetX, offsetY)
        for wall in walls:
            wall.draw(surface, offsetX, offsetY)
        for door in doors:
            door.draw(surface, offsetX, offsetY)
        for i in range(len(self.doors)):
            if i == len(self.doors) - 1 and self.doors[i].isSolved:
                portal.draw(surface, portalTarget, offsetX, offsetY)

    def isCompleted(self):
        doors = self.doors
        for door in doors:
            if not door.isSolved():
                return False
        return True
    
