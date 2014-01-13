#!/usr/bin/python
import pygame
from pygame.locals import *
from sys import exit
import sys
from array import *

#Game Parameters
BALLS_PER_GAME = 3

#input mode
INPMODE_INPUT = 0
INPMODE_SOUND = 1
INPMODE_LIGHTS = 2

#game mode
GAME_ATTRACT = 0
GAME_PLAYING = 1

#Display constants
DISP_PLAYER1 = 0
DISP_PLAYER2 = 1
DISP_PLAYER3 = 2
DISP_PLAYER4 = 3
DISP_PLAYER_NUM = 4
DISP_CREDIT_BALL_NUM = 5

NO_KEY_PRESS = '\xff'
numCredits = 0
numPlayers = 0

#sound file list, note:  must be wav files
sndFile = ["sounds/wah_wuh.wav", "sounds/ding_ding.wav", "sounds/opendoor.wav",
           "sounds/jump.wav", "sounds/wfall1.wav", "sounds/wfall2.wav", "sounds/wfall3.wav"]

#feature lights list
#located using actual screen x,y coordinates (auto scaled to simulation)
lghtRadius = 20
featureLghtPos = [[200,200], [300,300], [400,300], [500,300],
                  [600,300], [700,300], [800,300], [900,300],
                  [1000,300], [1100,200]]

#General illumination lights list
#located using actual screen x,y coordinates (auto scaled to simulation)
giLghtPos = [[200,100], [300,100], [400,100], [500,100],
             [600,100], [700,100], [800,100], [900,100],
             [1000,100], [1100,100]]

#Switch input point values
#just simple values to add to the active player's score
scoreInc = [10, 1, 2, 3, 4, 5, 6, 7, 8, 9]

orangeColor = (255, 131, 0)
whiteColor = (255, 255, 255)

def updateDisp(player, value, blank):
  screen.blit(background, clearRect[player], clearRect[player])
  if (not blank):
    text = digiFont.render(str(value), 1, orangeColor)
    textpos = text.get_rect()
    textpos.midright = xPos[player], yPos[player]
    screen.blit(text, textpos)
  pygame.display.update(clearRect[player])

def createSndPlyr():
  for fileName in sndFile:
    sndPlyr.append(pygame.mixer.Sound(fileName))

def updateFeatLight(num):
  if (num < len(featOn)):
    if not featOn[num]:
      pygame.draw.circle(screen, whiteColor, (featureSimLghtPos[num][0], featureSimLghtPos[num][1]), simLghtRadius)
      featOn[num] = True
    else:
      screen.blit(background, clearFeatRect[num], clearFeatRect[num])
      featOn[num] = False
    pygame.display.update(clearFeatRect[num])

def giLightOn(on):
  if on:
    for tmpLghtPos in giSimLghtPos:
      pygame.draw.circle(screen, whiteColor, (tmpLghtPos[0], tmpLghtPos[1]), simLghtRadius)
  else:
    for tmpLghtRect in clearGiRect:
      screen.blit(background, tmpLghtRect, tmpLghtRect)
  for tmpLghtRect in clearGiRect:
    pygame.display.update(tmpLghtRect)

def playSound(num):
  if (num < len(sndPlyr)):
    sndPlyr[num].play()

normal = True
debug = False
end = False
simWidth = 1920
inpMode = INPMODE_INPUT
gameMode = GAME_ATTRACT
keyPress = NO_KEY_PRESS
sndPlyr = []
featureSimLghtPos = []
giSimLghtPos = []
featOn = []

mode = pygame.NOFRAME
fontSize = 36
actWidth = 0
for arg in sys.argv:
  if arg.startswith('-simWidth='):
    simWidth = int(arg[10:])
  elif arg.startswith('-actualWidth='):
    actWidth = int(arg[13:])
  elif arg.startswith('-fullscr'):
    mode |= pygame.FULLSCREEN
  elif arg.startswith('-debug'):
    debug = True
  elif arg.startswith('-?'):
    print "python startPin.py [OPTIONS]"
    print "    -?                 Options Help"
    print "    -simWidth=         Width of simulation screen in pixels (assumes HD format)"
    print "    -actualWidth=      Width of final screen in pixels (assumes HD format)"
    print "                       Used for scaling.  If not set, assume simWidth is final"
    print "    -fullscr           Full screen mode"
    print "    -debug             Create debug window"
    end = True
if end:
  exit()

#Set actual width if not entered
if (actWidth < simWidth):
  actWidth = simWidth
simRatio = float(simWidth)/float(actWidth)

#Make screen HD ratio, video will take up 80% of height/width
hdRatio = 1920.0/1080.0
simHeight = int((simWidth/hdRatio) + .5)
videoRatio = .8
vidHeight = int((simHeight * videoRatio) + .5)
vidWidth = int((simWidth * videoRatio) + .5)

#Check if the requested size can be displayed
pygame.init()
infoObject = pygame.display.Info()
if (simWidth > infoObject.current_w) or (simHeight > infoObject.current_h):
  print "Screen size: %d x %d not supported" % (simWidth, simHeight)
  exit()

#Figure out size of score boxes
plyrScoreHeight = int(((simHeight - vidHeight)/2.0) + .5)
creditWidth = 2 * plyrScoreHeight
plyrScoreWidth = int(((simWidth - creditWidth)/2.0) + .5)

#Calculate y position of rows
yPosRow1 = vidHeight + int((plyrScoreHeight/2.0) + .5)
yPosRow2 = yPosRow1 + plyrScoreHeight

#Calculate x position of player/credit
xPosCol1 = int((plyrScoreWidth/2.0) + .5)
xPosCol2 = int((simWidth/2.0) + .5)
xPosCol3 = plyrScoreWidth + creditWidth + xPosCol1

#Optimize font size to height to plyrScoreHeight
fontHeightGoal = int((plyrScoreHeight * .8) + .5)
fontSize = 10
fontHeight = 0
while (fontHeight < fontHeightGoal):
  fontSize += 1
  digiFont = pygame.font.Font("font/digitalFont.ttf", fontSize)
  text = digiFont.render("0", 1, (10, 10, 10))
  fontHeight = text.get_height()
  
#Figure out the player score width, create position arrays
xPos = array('i',[])
yPos = array('i',[])
text = digiFont.render("8888888888", 1, orangeColor)
scoreWidth = text.get_width()
scoreHeight = text.get_height()

#Player 1
yPos.append(yPosRow1)
xPos.append(xPosCol1 + int((text.get_width()/2.0) + .5))

#Player 2
yPos.append(yPosRow1)
xPos.append(xPosCol3 + int((text.get_width()/2.0) + .5))

#Player 3
yPos.append(yPosRow2)
xPos.append(xPosCol1 + int((text.get_width()/2.0) + .5))

#Player 4
yPos.append(yPosRow2)
xPos.append(xPosCol3 + int((text.get_width()/2.0) + .5))

#Create clear rect for player displays
clearRect = []
for index in range(0,4):
  tmpRect = pygame.Rect(0, 0, scoreWidth, scoreHeight)
  tmpRect.midright = xPos[index], yPos[index]
  clearRect.append(tmpRect)

#Active Player, single digit
text = digiFont.render("8", 1, orangeColor)
yPos.append(yPosRow1)
xPos.append(xPosCol2 + int((text.get_width()/2.0) + .5))

#Credits/Ball Num, two digits
text = digiFont.render("88", 1, orangeColor)
yPos.append(yPosRow2)
xPos.append(xPosCol2 + int((text.get_width()/2.0) + .5))
creditWidth = text.get_width()
creditHeight = text.get_height()

#Create clear rect for other displays
tmpRect = pygame.Rect(0, 0, creditWidth, creditHeight)
tmpRect.midright = xPos[4], yPos[4]
clearRect.append(tmpRect)
tmpRect = pygame.Rect(0, 0, creditWidth, creditHeight)
tmpRect.midright = xPos[5], yPos[5]
clearRect.append(tmpRect)

#Create feature light locations
clearFeatRect = []
simLghtRadius = int((float(lghtRadius) * simRatio) + .5)
for tmpLghtPos in featureLghtPos:
  tmpLghtXPos = int((float(tmpLghtPos[0]) * simRatio) + .5)
  tmpLghtYPos = int((float(tmpLghtPos[1]) * simRatio) + .5)
  featureSimLghtPos.append((tmpLghtXPos, tmpLghtYPos))
  featOn.append(False)
  tmpRect = pygame.Rect(tmpLghtXPos - simLghtRadius, tmpLghtYPos - simLghtRadius, simLghtRadius * 2, simLghtRadius * 2)
  clearFeatRect.append(tmpRect)

#Create general illumination light locations
clearGiRect = []
for tmpLghtPos in giLghtPos:
  tmpLghtXPos = int((float(tmpLghtPos[0]) * simRatio) + .5)
  tmpLghtYPos = int((float(tmpLghtPos[1]) * simRatio) + .5)
  giSimLghtPos.append((tmpLghtXPos, tmpLghtYPos))
  tmpRect = pygame.Rect(tmpLghtXPos - simLghtRadius, tmpLghtYPos - simLghtRadius, simLghtRadius * 2, simLghtRadius * 2)
  clearGiRect.append(tmpRect)

#create the screen
screen=pygame.display.set_mode((simWidth, simHeight),mode, 24)
clock = pygame.time.Clock()
done = False

# Fill background
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0, 0, 0))
screen.blit(background, (0, 0))

# Show score positions
text = digiFont.render("8888888888", 1, orangeColor)
for index in range(0,4):
  textpos = text.get_rect()
  textpos.midright = xPos[index], yPos[index]
  screen.blit(text, textpos)

# Show player/credit positions
text = digiFont.render("8", 1, orangeColor)
textpos = text.get_rect()
textpos.midright = xPos[4], yPos[4]
screen.blit(text, textpos)
text = digiFont.render("88", 1, orangeColor)
textpos = text.get_rect()
textpos.midright = xPos[5], yPos[5]
screen.blit(text, textpos)

#Show screen
pygame.display.update()

# run the game loop
score = [0, 0, 0, 0]

#Playing a sound
pygame.mixer.init()
createSndPlyr()
giLightOn(True)
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
            elif event.key == pygame.K_i:
                inpMode = INPMODE_INPUT
                print "Input mode"
            elif event.key == pygame.K_s:
                inpMode = INPMODE_SOUND
                print "Sound mode"
            elif event.key == pygame.K_l:
                inpMode = INPMODE_LIGHTS
                print "Light mode"
            elif event.key == pygame.K_c:
                numCredits += 1
                if (gameMode == GAME_ATTRACT):
                  updateDisp(DISP_CREDIT_BALL_NUM, numCredits, False)
            elif event.key == pygame.K_g:
                #Check if starting a game
                if (gameMode == GAME_ATTRACT) and (numCredits > 0):
                  numCredits -= 1
                  gameMode = GAME_PLAYING
                  numPlayers = 1
                  currBall = 0
                  currPlayer = 0
                  score[0] = 0
                  
                  #Set up player 1 score
                  updateDisp(DISP_PLAYER1, score[0], False)
                  
                  #Clear player 2, 3, 4 scores
                  updateDisp(DISP_PLAYER2, numCredits, True)
                  updateDisp(DISP_PLAYER3, numCredits, True)
                  updateDisp(DISP_PLAYER4, numCredits, True)

                  #Set player number, ball number
                  updateDisp(DISP_PLAYER_NUM, currPlayer + 1, False)
                  updateDisp(DISP_CREDIT_BALL_NUM, 1, False)
                  
                  #Play background music
                  pygame.mixer.music.load("sounds/bgndtrack.mp3")
                  pygame.mixer.music.play(-1)
                #Check if another player is being added  
                elif (gameMode == GAME_PLAYING) and (numCredits > 0):
                  #Only allow adding players if during first ball
                  if (currBall < 1) and (numPlayers < 4):
                    numCredits -= 1
                    score[numPlayers] = 0
                    updateDisp(numPlayers, score[numPlayers], False)
                    numPlayers += 1
            elif event.key == pygame.K_d:
                #Drain the current ball
                if (gameMode == GAME_PLAYING):
                    #If more players, increment currPlayers
                    if (currPlayer + 1 < numPlayers):
                      currPlayer += 1
                      updateDisp(DISP_PLAYER_NUM, currPlayer + 1, False)
                    elif (currBall + 1 < BALLS_PER_GAME):
                      currPlayer = 0
                      updateDisp(DISP_PLAYER_NUM, currPlayer + 1, False)
                      currBall += 1
                      updateDisp(DISP_CREDIT_BALL_NUM, currBall + 1, False)
                    else:
                      #Game over, blank player number
                      updateDisp(DISP_PLAYER_NUM, 0, True)
                      updateDisp(DISP_CREDIT_BALL_NUM, numCredits, False)
                      pygame.mixer.music.stop()
                      gameMode = GAME_ATTRACT
            elif (event.key >= pygame.K_0) and (event.key <= pygame.K_9):
                keyPress = event.key - pygame.K_0
    if keyPress != NO_KEY_PRESS:
      #keypress processing here
      if inpMode == INPMODE_SOUND:
        playSound(keyPress)
      elif inpMode == INPMODE_LIGHTS:
        updateFeatLight(keyPress)
      if gameMode == GAME_PLAYING:
        score[currPlayer] += scoreInc[keyPress]
        updateDisp(currPlayer, score[currPlayer], False)
      keyPress = NO_KEY_PRESS
    clock.tick(100)    

#background music should use following
#pygame.mixer.music.load("sounds/wah_wuh.mp3")
#pygame.mixer.music.play()
