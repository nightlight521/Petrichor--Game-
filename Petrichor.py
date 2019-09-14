###########################
# Title: Petrichor        #
# Subject: Final Game     #
# Author: Paula Yuan      #
# Date: Dec 23, 2018      #
###########################

from petrichor_classes import * 
import pygame

pygame.mixer.pre_init(44100, -16, 2, 1024)
pygame.init()
HEIGHT = 600
WIDTH = 800
BORDER = 100
gameWindow = pygame.display.set_mode((WIDTH, HEIGHT))
    
#--------------------------------#
# functions                      #
#--------------------------------#
def drawText(font, text, colour, x, y):
    graphics = font.render(text, 1, colour)
    gameWindow.blit(graphics, (x, y))

def playMenuSong():
    pygame.mixer.music.load("menuSong.ogg")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(loops=-1)

def playMainSong():
    pygame.mixer.music.load("mainMix.ogg")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(loops=-1)

def redrawGameWindow():
    level.draw(gameWindow, leverPic, symbolPic, offsetX, offsetY, portalPic)
    sprite.draw(gameWindow, offsetX, offsetY)
    tokenBackground = pygame.Surface((150, 30), pygame.SRCALPHA)
    tokenBackground.fill((0, 0, 0, 100))
    gameWindow.blit(tokenBackground, (10, 20))
    timeBackground = pygame.Surface((230, 30), pygame.SRCALPHA)
    timeBackground.fill((0, 0, 0, 100))
    gameWindow.blit(timeBackground, (570, 20))
    drawText(medFont, "Tokens: " + str(level.points) + "/" + str(level.COINS_TOTAL), WHITE, 20, 20)
    drawText(medFont, "Time elapsed: " + str(level.elapsed), WHITE, 600, 20)
    pygame.display.update()

def calcOffset(sprite, offsetX, offsetY, platforms):
    # calculates the offset between the world coordinates and view coordinates
    if sprite.x + offsetX < BORDER and sprite.x > BORDER: #pans left (move right)
        offsetX = offsetX + RUN_SPEED    
    if sprite.x + sprite.w + offsetX > WIDTH - BORDER and (sprite.x + sprite.w) < 1500 - BORDER: #pans right (move left)
        offsetX = offsetX - RUN_SPEED
    if sprite.b + offsetY > HEIGHT - BORDER and sprite.b < 1500 - BORDER: #pans up (move down)
        for elevator in platforms:
            if elevator.elevator and sprite.detectDown(platforms) and elevator.speed > 0:
                offsetY = offsetY - elevator.speed
        offsetY = offsetY - sprite.v
    if sprite.b - sprite.h + offsetY < BORDER and sprite.b - sprite.h > BORDER + 2: #pans down (move up) # +2 is a simple hack to fix panning issues
        for elevator in platforms:
            if elevator.elevator and sprite.detectDown(platforms) and elevator.speed < 0:
                offsetY = offsetY - elevator.speed
        offsetY = offsetY - sprite.v
    return (offsetX, offsetY)

def drawMenu():
    gameWindow.blit(menuBkgd, (0, 0))
    drawText(bigFont, "PETRICHOR", WHITE, 300, 100)
    drawText(medFont, "how to play", WHITE, 330, 400)
    pygame.draw.rect(gameWindow, WHITE, (320, 400, 150, 30), 2)
    drawText(medFont, "START", WHITE, 350, 200)
    pygame.draw.rect(gameWindow, WHITE, (340, 200, 80, 30), 2)

def drawWinMenu(currentLevel, level):
    pygame.draw.rect(gameWindow, BROWN, (200, 200, 400, 200), 0)
    drawText(bigFont, "LEVEL COMPLETED!", WHITE, 260, 230)
    if currentLevel == 2:
        drawText(medFont, "previous level", WHITE, 260, 440)
        gameWindow.blit(leftArrow, (270, 480))
        drawText(medFont, "next level", WHITE, 480, 440)
        gameWindow.blit(rightArrow, (480, 480))
    if currentLevel == 1:
        drawText(medFont, "next level", WHITE, 480, 440)
        gameWindow.blit(rightArrow, (480, 480))
    if currentLevel == 3:
        drawText(medFont, "previous level", WHITE, 220, 440)
        gameWindow.blit(leftArrow, (270, 480))
    gameWindow.blit(home, (360, 480))
    if level.points >= 0.5 * level.COINS_TOTAL and level.elapsed <= 180:
        gameWindow.blit(star, (250, 300))
        gameWindow.blit(star, (350, 300))
        gameWindow.blit(emptyStar, (450, 300))
    if level.points <= 0.5 * level.COINS_TOTAL or level.elapsed >= 180:
        gameWindow.blit(emptyStar, (250, 300))
        gameWindow.blit(emptyStar, (350, 300))
        gameWindow.blit(emptyStar, (450, 300))
    if level.points == level.COINS_TOTAL and level.elapsed <= 60:
        gameWindow.blit(star, (250, 300))
        gameWindow.blit(star, (350, 300))
        gameWindow.blit(star, (450, 300))
    
def drawInstructionsMenu():
    gameWindow.blit(instructionsMenu, (0, 0))
    drawText(medFont, "Petrichor - the earthy scent produced when rain falls on dry soil.", BLACK, 100, 100)
    drawText(medFont, "A smell of adventure and discovery, and what this game was meant to be.", BLACK, 50, 150)
    drawText(medFont, "One where you pull levers to light symbols corretcly.", BLACK, 150, 200)
    drawText(medFont, "Controls: A and D - left and right. W to jump.", BLACK, 200, 300)
    drawText(medFont, "F to interact with levers. Press 'p' to pause.", BLACK, 240, 350)
    drawText(medFont, "Note: Jumping on elevators is prohibited.", BLACK, 220, 400)
    drawText(medFont, "BACK", WHITE, 400, 450)
    pygame.draw.rect(gameWindow, WHITE, (390, 450, 80, 40), 2)

def drawLevelsMenu():
    gameWindow.blit(levelsMenu, (0, 0))
    drawText(medFont, "Level Select", WHITE, 350, 50)
    drawText(medFont, "BACK", WHITE, 100, 500)
    pygame.draw.rect(gameWindow, WHITE, (90, 500, 80, 40), 2)
    pygame.draw.rect(gameWindow, WHITE, (60, 100, 140, 380), 2)
    pygame.draw.rect(gameWindow, WHITE, (250, 100, 200, 380), 2)
    pygame.draw.rect(gameWindow, WHITE, (530, 100, 180, 380), 2)

def drawPauseMenu():
    gameWindow.blit(pauseMenu, (0, 0))
    drawText(bigFont, "PAUSED", WHITE, 350, 150)
    drawText(medFont, "unpause", WHITE, 360, 300)
    pygame.draw.rect(gameWindow, WHITE, (350, 300, 110, 30), 2)
    
#--------------------------------#
# main program                   #
#--------------------------------#

#------------------------------------------------------------#
# defining variables/constants, loading pictures and sound   #
#------------------------------------------------------------#

RUN_SPEED = 10
JUMP_SPEED = -30
GRAVITY = 2

# Loading pictures
leverPic = [0]*2
for i in range(2):
    leverPic[i] = pygame.image.load("small levers/lever" + str(i) + ".png")

symbolPic = [0]*8
for i in range(8):
    symbolPic[i] = pygame.image.load("small symbols/symbol" + str(i) + ".png")

portalPic = pygame.image.load("portal.png")
menuBkgd = pygame.image.load("menuBkgd.jpg")
instructionsMenu = pygame.image.load("instructionsMenu.jpg")
levelsMenu = pygame.image.load("levelsMenu.jpg")
pauseMenu = pygame.image.load("pauseMenu.jpg")
home = pygame.image.load("home.png")
star = pygame.image.load("star.png")
emptyStar = pygame.image.load("star1.png")
rightArrow = pygame.image.load("right.png")
leftArrow = pygame.image.load("left.png")

# Displaying Menus
showInstructionsMenu = False
showLevelSelection = False

# Character animation pictures
nextStandingPic = [1, 0, 0, 0, 0, 0, 0] # these numbers represent which pictures are supposed to be loaded 
nextLeftPic = [2, 2, 3, 2, 2, 2, 2]     # for each animation position of the character sprite
nextRightPic = [4, 4, 4, 4, 5, 4, 4, 4]
nextDownPic = [6, 6, 6, 6, 6, 7, 6, 6]

# Time and Clock
clock = pygame.time.Clock()
FPS = 30
frameCount = 0

# Level Completion
win = False

# Pausing
unpaused = False
pauseElapsed = 0
inPlay = False

# Fonts
medFont = pygame.font.SysFont("Century Gothic", 20)
bigFont = pygame.font.SysFont("Century Gothic", 30)

# Sound Effects
leverSFX = pygame.mixer.Sound("lever.wav")
winSFX = pygame.mixer.Sound("win.wav")
coinSFX = pygame.mixer.Sound("coin.wav")

#---------------------------------------#

#-----------------#
# Starting menus  #
#-----------------#

# Play menu music
playMenuSong()

# Draw starting menu
showMenu = True
while showMenu:
    pygame.event.clear()
    drawMenu()
    clock.tick(60)

    mouseX, mouseY = pygame.mouse.get_pos()
    if mouseX >= 320 and mouseX <= 470 and mouseY >= 400 and mouseY <= 430: # if mouse is in the range of the given rect
        pygame.draw.rect(gameWindow, BRIGHT_BLUE, (320, 400, 150, 30), 2)   # highlighting instructions menu
    if mouseX >= 340 and mouseX <= 420 and mouseY >= 200 and mouseY <= 230: # highlighting level selection menu
        pygame.draw.rect(gameWindow, BRIGHT_BLUE, (340, 200, 80, 30), 2) 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN: 
            if mouseX >= 320 and mouseX <= 470 and mouseY >= 400 and mouseY <= 430: # if mouse is in the range of the given rect
                showInstructionsMenu = True                                         # selecting instructions menu
            if mouseX >= 340 and mouseX <= 420 and mouseY >= 200 and mouseY <= 230:   
                showLevelSelection = True                                           # selecting level selection menu
    
    pygame.display.update()

    # draw instructions menu
    while showInstructionsMenu:
        pygame.event.clear()
        drawInstructionsMenu()
        clock.tick(60)

        mouseX, mouseY = pygame.mouse.get_pos()
        if mouseX >= 390 and mouseX <= 470 and mouseY >= 450 and mouseY <= 490: # "BACK" button highlighting
            pygame.draw.rect(gameWindow, BRIGHT_BLUE, (390, 450, 80, 40), 2)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN: # mouse button pressed
                if mouseX >= 390 and mouseX <= 470 and mouseY >= 450 and mouseY <= 490: # "BACK" button selction
                    showInstructionsMenu = False
        
        pygame.display.update()

    while showLevelSelection:
        pygame.event.clear()
        drawLevelsMenu()
        clock.tick(60)

        mouseX, mouseY = pygame.mouse.get_pos()
        if mouseX >= 90 and mouseX <= 170 and mouseY >= 500 and mouseY <= 540: # "BACK" button highlighting
            pygame.draw.rect(gameWindow, BRIGHT_BLUE, (90, 500, 80, 40), 2)
        if mouseX >= 60 and mouseX <= 200 and mouseY >= 100 and mouseY <= 480: # level 1 box highlighting
            pygame.draw.rect(gameWindow, BRIGHT_BLUE, (60, 100, 140, 380), 2)
        if mouseX >= 250 and mouseX <= 430 and mouseY >= 100 and mouseY <= 480: # level 2 box highlighting
            pygame.draw.rect(gameWindow, BRIGHT_BLUE, (250, 100, 200, 380), 2)
        if mouseX >= 530 and mouseX <= 670 and mouseY >= 100 and mouseY <= 480: # level 3 box highlighting
            pygame.draw.rect(gameWindow, BRIGHT_BLUE, (530, 100, 180, 380), 2)
                    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if mouseX >= 90 and mouseX <= 170 and mouseY >= 500 and mouseY <= 540: # "BACK" button selction
                    showLevelSelection = False
                if mouseX >= 60 and mouseX <= 200 and mouseY >= 100 and mouseY <= 480: # Selecting level 1, setting presets
                    currentLevel = 1
                    level = readLevel(currentLevel)
                    startingX = level.startingX
                    startingB = level.startingB
                    sprite = Character(startingX, startingB)
                    offsetX = level.startingOffsetX
                    offsetY = level.startingOffsetY        
                    inPlay = True
                    showLevelSelection = False
                if mouseX >= 250 and mouseX <= 430 and mouseY >= 100 and mouseY <= 480: # Selecting level 2
                    currentLevel = 2
                    level = readLevel(currentLevel)
                    startingX = level.startingX
                    startingB = level.startingB
                    sprite = Character(startingX, startingB)
                    offsetX = level.startingOffsetX
                    offsetY = level.startingOffsetY
                    inPlay = True
                    showLevelSelection = False
                if mouseX >= 530 and mouseX <= 670 and mouseY >= 100 and mouseY <= 480: # Selecting level 3
                    currentLevel = 3
                    level = readLevel(currentLevel)
                    startingX = level.startingX
                    startingB = level.startingB
                    sprite = Character(startingX, startingB)
                    offsetX = level.startingOffsetX
                    offsetY = level.startingOffsetY
                    inPlay = True
                    showLevelSelection = False
        pygame.display.update()
            
    if inPlay:
        for i in range(8): # loads character images
            sprite.pic[i] = pygame.image.load("small sprite/sprite" + str(i) + ".png")
        
        # stop menu music, load and play main game music        
        pygame.mixer.music.stop()
        playMainSong()

        # Start Timing:
        isTiming = True
        if isTiming:
            BEGIN = time.time()
            referenceTime = BEGIN
        
    #------------------#
    # Main Game        #
    #------------------#
    while inPlay:
        # detect platforms, doors, and walls for landing
        platform = sprite.detectDown(level.platforms)
        door = sprite.detectDown(level.doors)
        wall = sprite.detectDown(level.walls)
        
        # sets ground level to detected platforms, doors, and walls
        if platform != None:
            groundLevel = platform.y
        elif door != None:
            groundLevel = door.y
        elif wall != None:
            groundLevel = wall.y
        else:
            groundLevel = 1100

        # calculate points accumulated in the level so far
        level.points = sprite.eatCoins(level.coins, level.points, coinSFX)
            
        redrawGameWindow()
        clock.tick(FPS)
        frameCount = frameCount + 1
        

        # pausing
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p]:
            pause = True
            pauseStart = time.time() # records when pause started
            while pause:
                pygame.event.clear()
                drawPauseMenu()
                keys = pygame.key.get_pressed()
                mouseX, mouseY = pygame.mouse.get_pos()
                if mouseX >= 350 and mouseX <= 460 and mouseY >= 300 and mouseY <= 330:
                    pygame.draw.rect(gameWindow, BRIGHT_BLUE, (350, 300, 110, 30), 2)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            pause = False
                            unpaused = True
                pygame.display.update()
            pauseElapsed = pauseElapsed + round(time.time() - pauseStart, 1) # records amount of time paused
        level.elapsed = round(time.time() - referenceTime, 1)
        level.elapsed = level.elapsed - pauseElapsed # updates time elapsed, subtracting time while paused
        
        # Keyboard Input

        if keys[pygame.K_a] == keys[pygame.K_d]:
            # either both a and d are pressed, or neither are pressed
            # when both are pressed, we could try to move in the direction last pressed, but it doesn't seem to be worth the complexity
            sprite.dir = "front"
            if frameCount % 3 == 0:
                sprite.picNum = nextStandingPic[sprite.picNum]
        elif keys[pygame.K_a] and sprite.x >= 0 and not sprite.detectWallsLeft(level.walls) and not sprite.detectDoorsLeft(level.doors):
            sprite.dir = "left"
            sprite.x = sprite.x - RUN_SPEED
            if frameCount % 3 == 0:
                sprite.picNum = nextLeftPic[sprite.picNum]
        elif keys[pygame.K_d] and sprite.x + sprite.w <= 1500 - RUN_SPEED and not sprite.detectWallsRight(level.walls) and not sprite.detectDoorsRight(level.doors):
            sprite.dir = "right"
            sprite.x = sprite.x + RUN_SPEED
            if frameCount % 3 == 0:
                sprite.picNum = nextRightPic[sprite.picNum]
            
        if keys[pygame.K_w] and sprite.b == groundLevel:
            sprite.v = JUMP_SPEED
            if sprite.dir == "right":
                sprite.picNum = nextRightPic[sprite.picNum]
            if sprite.dir == "left":
                sprite.picNum = nextLeftPic[sprite.picNum]
                
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_f:
                    sprite.detectFlip(level.levers, leverSFX)
                    for door in level.doors:
                        door.maybeUnlock()
            if event.type == pygame.QUIT:
               pygame.quit()
                            
        for elevator in level.platforms:
            if elevator.elevator: # checks to see if a platform is an elevator
                elevator.y = elevator.move()
                    
    # update sprite's vertical velocity
        sprite.v = sprite.detectUp(level.platforms)
        sprite.v = sprite.detectDoorsUp(level.doors)
        sprite.v = sprite.v + GRAVITY
    # move sprite in vertical direction
        sprite.b = sprite.b + sprite.v
        # update horizontal and vertical offsets to account for previous movement
        offsetX, offsetY = calcOffset(sprite, offsetX, offsetY, level.platforms)
        if sprite.b >= groundLevel:
            # makes sure the character does not keep falling through the ground/other platforms
            # since we need to shift the character up to groundlevel, also shift the view up by the same amount if necessary
            if sprite.b + offsetY > HEIGHT - 100:
                offsetY = offsetY + sprite.b - groundLevel
            if sprite.b - sprite.h + offsetY < 100 and sprite.b - sprite.h > 100:
                offsetY = offsetY + sprite.v # i get why it works but there should be a better way
            sprite.b = groundLevel
            sprite.v = 0
        if level.isCompleted():
            if not level.popped: # pops last door for aesthetic reasons
                level.doors.pop(-1)
                level.popped = True 
            if sprite.detectPortal(level.portal):
                playSFX(winSFX)
                win = True
                isTiming = False # stop timing once level completed
                while win:
                    drawWinMenu(currentLevel, level)
                    mouseX, mouseY = pygame.mouse.get_pos()
                    if mouseX >= 270 and mouseX <= 339 and mouseY >= 480 and mouseY <= 546: # going to previous level
                        for event in pygame.event.get():
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                # resets to the starting information for the correct level
                                level = readLevel(currentLevel - 1)
                                sprite.x = level.startingX
                                sprite.b = level.startingB
                                offsetX = level.startingOffsetX
                                offsetY = level.startingOffsetY
                                currentLevel = currentLevel - 1
                                win = False
                    if mouseX >= 480 and mouseX <= 549 and mouseY >= 480 and mouseY <= 546: # going to next level
                        for event in pygame.event.get():
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                # resets to the starting information for the correct level
                                level = readLevel(currentLevel + 1)
                                sprite.x = level.startingX
                                sprite.b = level.startingB
                                offsetX = level.startingOffsetX
                                offsetY = level.startingOffsetY
                                currentLevel = currentLevel + 1
                                win = False
                    if mouseX >= 360 and mouseX <= 440 and mouseY >= 480 and mouseY <= 560:
                        for event in pygame.event.get():
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                # back to home menu
                                win = False
                                inPlay = False
                    else:
                        pygame.event.clear()
                    pygame.display.update()
                    referenceTime = time.time() # resets reference time

pygame.quit()
