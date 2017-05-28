#By Spencer R.
#Idea and pygame instruction from Al Sweigart
#Levels by David W. Skinner
#createMapList() mostly by Mr. Minich
#Extra help from Stack Overflow community
import random, sys, copy, os, pygame
from pygame.locals import *
#This is essential for all pygame programs
pygame.init()
pygame.display.set_caption('Dungeon Escape')
#The color t'UP'le values
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (147, 147, 147)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
RED = (255,0,0)
ONE = 0
TWO = 0
direction = 'NONE'

DISPLAYSURF = pygame.display.set_mode((1240, 720))

FPSCLOCK = pygame.time.Clock()

#Pygame works where the graph has no negative
#The Y axis also starts at 0 ON TOP then GOES ''DOWN''
XMAPCORD = 0
YMAPCORD = 0
#Determines what level you are on
currentLevelIndex = 0
mapNeedsRedraw = True
def resetLevel():
    pygame.Surface.fill(DISPLAYSURF, BLACK)
def doNothing():
    redrawMap()
currentLevel = ['w']
#This creates the map by using a .txt file to create a list
def createMapList():
    global currentLevel
    global tilesWidth
    global currentLevelIndex
    file = open('dungeonescapelevels.txt', 'r')
    mainList = []
    nextList = []
    widthList = [14, 9, 15, 12, 9, 9, 7, 11, 9, 16, 13, 15, 13, 19, 13, 9, 18, 11, 27, 12, 10, 9, 15, 23, 8, 25, 9]

    for i, line in enumerate(file):  # line is a string 
        # get rid of semicolons, new line characters, and blank spaces
        line = line.replace(";", "")
        line = line.replace("\n", "")
        line = line.replace(" ", "")

        # if next line contains a digit, dump current list as next
        #list element of the main list and start a new list but
        #don't add the line with the digit itself to the new list
        if (line.isdigit() == True):
            nextList = []
            mainList.append(nextList)
        else:
            nextList.extend(list(line))
    #Determines which list to present as currentLevel by using the currentLevelIndex
    for i in range(currentLevelIndex + 1):
        tilesWidth = widthList[i]
        currentLevel = mainList[currentLevelIndex]



#is responsible for drawing the map
def redrawMap():
    global XMAPCORD
    global YMAPCORD
    global currentLevelIndex
    resetLevel()
    for i in range(0,len(currentLevel)):
        if playerPositionMap[i-1] == 'w':
            drawWall()
            XMAPCORD = XMAPCORD + 40
        elif playerPositionMap[i-1] == 's':
            drawStone()
            XMAPCORD = XMAPCORD + 40
        elif playerPositionMap[i-1] == 'g':
            drawGoal()
            XMAPCORD = XMAPCORD + 40
        elif playerPositionMap[i-1] == 'p':
            drawPlayer()
            XMAPCORD = XMAPCORD + 40
        elif playerPositionMap[i-1] == 'k':
            drawKey()
            XMAPCORD = XMAPCORD + 40
        elif playerPositionMap[i-1] == 'f':
            drawFinish()
            XMAPCORD = XMAPCORD + 40
        elif playerPositionMap[i-1] == 'G':
            drawPlayerGoal()
            XMAPCORD = XMAPCORD + 40
        if i % tilesWidth == 0:
            YMAPCORD = YMAPCORD + 40
            XMAPCORD = 0
        elif i == len(playerPositionMap) - 1:
            XMAPCORD = 0
            YMAPCORD = 0
        mapNeedsRedraw = False

#The main game loop
def movePlayer():
    createMapList()
    global currentLevel
    global tilesWidth
    global playerPositionMap
    global drawmap
    global playerPosition
    global mapNeedsRedraw
    global currentLevelIndex
    #I only edit playerPositionMap and keep currentLevel the same so the player
    #can reset the level by changing it to the original
    playerPositionMap = currentLevel
    redrawMap()

    running = True
    drawmap = True
    FPS = 30
    fpsClock = pygame.time.Clock()
    while running:
        #This looks to see if there are no 'g' elements
        #if there are none that that means the user has completed the level
        if 'g' not in playerPositionMap and 'G' not in playerPositionMap:
            currentLevelIndex = currentLevelIndex + 1
            createMapList()
            playerPositionMap = currentLevel
            redrawMap()
        #Allows the user to quit the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                sys.exit()
            #This moves the player according to the key pressed
            if event.type == KEYDOWN:
                #Tells python the players position in the list
                # 'G' and 'F' are simply the player on top of different tiles
                if 'p' in playerPositionMap:
                    playerPosition = playerPositionMap.index('p')
                elif 'G' in playerPositionMap:
                    playerPosition = playerPositionMap.index('G')
                elif 'F' in playerPositionMap:
                    playerPosition = playerPositionMap.index('F')
                if ((event.key == K_r) and (currentLevelIndex == 4)):
                    currentLevelIndex = currentLevelIndex + 1
                    createMapList()
                    playerPositionMap = currentLevel
                    redrawMap()
                #Resets the level
                elif (event.key == K_r):
                    createMapList()
                    playerPositionMap = currentLevel
                    redrawMap()
                elif ((event.key == K_n) and (currentLevelIndex > 6)):
                    currentLevelIndex = currentLevelIndex + 1
                    if currentLevelIndex > 26:
                        currentLevelIndex = 7
                    createMapList()
                    playerPositionMap = currentLevel
                    redrawMap()
                elif ((event.key == K_b) and (currentLevelIndex > 6)):
                    currentLevelIndex = currentLevelIndex - 1
                    if currentLevelIndex < 7:
                        currentLevelIndex = 26
                    createMapList()
                    playerPositionMap = currentLevel
                    redrawMap()
                #This determines where the player moves
                #It is so long because I have to code for every possible situation
                if ((event.key == K_LEFT or event.key == K_a) and (playerPositionMap[playerPosition - 1] != 'w')):
                    ONE = 1
                    TWO = 2
                    direction = 'LEFT'
                elif ((event.key == K_DOWN or event.key == K_s) and (playerPositionMap[playerPosition + tilesWidth] != 'w')):
                        ONE = tilesWidth
                        TWO = (tilesWidth*2)
                        direction = 'DOWN'
                elif ((event.key == K_RIGHT or event.key == K_d) and (playerPositionMap[playerPosition + 1] != 'w')):
                        ONE = 1
                        TWO = 2
                        direction = 'RIGHT'
                elif ((event.key == K_UP or event.key == K_w) and (playerPositionMap[playerPosition - tilesWidth] != 'w')):
                        ONE = tilesWidth
                        TWO = (tilesWidth*2)
                        direction = 'UP'
                if direction == 'NONE':
                    doNothing()
                elif direction == 'DOWN' or direction == 'RIGHT':
                    if playerPositionMap[playerPosition + ONE] == 'w':
                        doNothing()
                    elif playerPositionMap[playerPosition + ONE] == 'k':
                        if playerPositionMap[playerPosition + TWO] == 'g':
                            playerPositionMap[playerPosition + TWO] = 'f'
                            playerPositionMap[playerPosition + ONE] = 'p'
                            playerPositionMap[playerPosition] = 's'
                        elif playerPositionMap[playerPosition + TWO] == 'w' or playerPositionMap[playerPosition + TWO] == 'k' or playerPositionMap[playerPosition + TWO] == 'f':
                            doNothing()
                        elif playerPositionMap[playerPosition] == 'G':
                            playerPositionMap[playerPosition + TWO] = 'k'
                            playerPositionMap[playerPosition + ONE] = 'p'
                            playerPositionMap[playerPosition] = 'g'
                        else:
                            playerPositionMap[playerPosition + TWO] = 'k'
                            playerPositionMap[playerPosition + ONE] = 'p'
                            playerPositionMap[playerPosition] = 's'
                    elif playerPositionMap[playerPosition] == 'G':
                        if playerPositionMap[playerPosition + ONE] == 'g':
                            playerPositionMap[playerPosition + ONE] = 'G'
                            playerPositionMap[playerPosition] = 'g'
                        elif playerPositionMap[playerPosition + ONE] == 'f':
                            if playerPositionMap[playerPosition + TWO] == 'w' or playerPositionMap[playerPosition + TWO] == 'f' or playerPositionMap[playerPosition + TWO] == 'k':
                                doNothing()
                            elif playerPositionMap[playerPosition + TWO] == 'g':
                                playerPositionMap[playerPosition + TWO] = 'f'
                                playerPositionMap[playerPosition + ONE] = 'G'
                                playerPositionMap[playerPosition] = 'g'
                            else:
                                playerPositionMap[playerPosition + TWO] = 'k'
                                playerPositionMap[playerPosition + ONE] = 'G'
                                playerPositionMap[playerPosition] = 'g'
                        else:
                            playerPositionMap[playerPosition + ONE] = 'p'
                            playerPositionMap[playerPosition] = 'g'
                    elif playerPositionMap[playerPosition + ONE] == 'g':
                        playerPositionMap[playerPosition + ONE] = 'G'
                        playerPositionMap[playerPosition] = 's'
                    elif playerPositionMap[playerPosition + ONE] == 'f':
                        if playerPositionMap[playerPosition + TWO] == 'w' or playerPositionMap[playerPosition + TWO] == 'f' or playerPositionMap[playerPosition + TWO] == 'k':
                            doNothing()
                        elif playerPositionMap[playerPosition + TWO] == 'g':
                            playerPositionMap[playerPosition + TWO] = 'f'
                            playerPositionMap[playerPosition + ONE] = 'G'
                            playerPositionMap[playerPosition] = 's'
                        else:
                            playerPositionMap[playerPosition + TWO] = 'k'
                            playerPositionMap[playerPosition + ONE] = 'G'
                            playerPositionMap[playerPosition] = 's'
                    else:
                        playerPositionMap[playerPosition + ONE] = 'p'
                        playerPositionMap[playerPosition] = 's'
                    mapNeedsRedraw = True
                elif direction == 'UP' or direction == 'LEFT':
                    if playerPositionMap[playerPosition - ONE] == 'w':
                        doNothing()
                    elif playerPositionMap[playerPosition - ONE] == 'k':
                        if playerPositionMap[playerPosition - TWO] == 'g':
                            playerPositionMap[playerPosition - TWO] = 'f'
                            playerPositionMap[playerPosition - ONE] = 'p'
                            playerPositionMap[playerPosition] = 's'
                        elif playerPositionMap[playerPosition - TWO] == 'w' or playerPositionMap[playerPosition - TWO] == 'k' or playerPositionMap[playerPosition - TWO] == 'f':
                            doNothing()
                        elif playerPositionMap[playerPosition] == 'G':
                            playerPositionMap[playerPosition - TWO] = 'k'
                            playerPositionMap[playerPosition - ONE] = 'p'
                            playerPositionMap[playerPosition] = 'g'
                        else:
                            playerPositionMap[playerPosition - TWO] = 'k'
                            playerPositionMap[playerPosition - ONE] = 'p'
                            playerPositionMap[playerPosition] = 's'
                    elif playerPositionMap[playerPosition] == 'G':
                        if playerPositionMap[playerPosition - ONE] == 'g':
                            playerPositionMap[playerPosition - ONE] = 'G'
                            playerPositionMap[playerPosition] = 'g'
                        elif playerPositionMap[playerPosition - ONE] == 'f':
                            if playerPositionMap[playerPosition - TWO] == 'w' or playerPositionMap[playerPosition - TWO] == 'f' or playerPositionMap[playerPosition - TWO] == 'k':
                                doNothing()
                            elif playerPositionMap[playerPosition - TWO] == 'g':
                                playerPositionMap[playerPosition - TWO] = 'f'
                                playerPositionMap[playerPosition - ONE] = 'G'
                                playerPositionMap[playerPosition] = 'g'
                            else:
                                playerPositionMap[playerPosition - TWO] = 'k'
                                playerPositionMap[playerPosition - ONE] = 'G'
                                playerPositionMap[playerPosition] = 'g'
                        else:
                            playerPositionMap[playerPosition - ONE] = 'p'
                            playerPositionMap[playerPosition] = 'g'
                    elif playerPositionMap[playerPosition - ONE] == 'g':
                        playerPositionMap[playerPosition - ONE] = 'G'
                        playerPositionMap[playerPosition] = 's'
                    elif playerPositionMap[playerPosition - ONE] == 'f':
                        if playerPositionMap[playerPosition - TWO] == 'w' or playerPositionMap[playerPosition - TWO] == 'f' or playerPositionMap[playerPosition - TWO] == 'k':
                            doNothing()
                        elif playerPositionMap[playerPosition - TWO] == 'g':
                            playerPositionMap[playerPosition - TWO] = 'f'
                            playerPositionMap[playerPosition - ONE] = 'G'
                            playerPositionMap[playerPosition] = 's'
                        else:
                            playerPositionMap[playerPosition - TWO] = 'k'
                            playerPositionMap[playerPosition - ONE] = 'G'
                            playerPositionMap[playerPosition] = 's'
                    else:
                        playerPositionMap[playerPosition - ONE] = 'p'
                        playerPositionMap[playerPosition] = 's'
                    mapNeedsRedraw = True
                #Redraws the map if the player pressed a key
                if mapNeedsRedraw:
                    redrawMap()
        #This is the clock and display 'UP'date
        pygame.display.update()
        fpsClock.tick(FPS)
    
#The tiles used in the project
def drawWall():
    pygame.draw.rect(DISPLAYSURF, WHITE, (XMAPCORD, YMAPCORD, 40, 40), 0)
def drawStone():
    pygame.draw.rect(DISPLAYSURF, GRAY, (XMAPCORD, YMAPCORD, 40, 40), 0)
def drawGoal():
    pygame.draw.rect(DISPLAYSURF, ORANGE, (XMAPCORD, YMAPCORD, 40, 40), 0)
def drawPlayer():
    pygame.draw.rect(DISPLAYSURF, GRAY, (XMAPCORD, YMAPCORD, 40, 40), 0)
    pygame.draw.rect(DISPLAYSURF, BLACK, (XMAPCORD + 10, YMAPCORD + 10, 20, 20), 0)
def drawKey():
    pygame.draw.rect(DISPLAYSURF, YELLOW, (XMAPCORD, YMAPCORD, 40, 40), 0)
def drawFinish():
    pygame.draw.rect(DISPLAYSURF, RED, (XMAPCORD, YMAPCORD, 40, 40), 0)
def drawPlayerGoal():
    pygame.draw.rect(DISPLAYSURF, ORANGE, (XMAPCORD, YMAPCORD, 40, 40), 0)
    pygame.draw.rect(DISPLAYSURF, BLACK, (XMAPCORD + 10, YMAPCORD + 10, 20, 20), 0)
def drawReset():
    pygame.draw.rect(DISPLAYSURF, BLACK, (XMAPCORD, YMAPCORD, 40, 40), 0)

#Executes the program
movePlayer()
