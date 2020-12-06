##################################################
#intended to create a list of characters using os directories
#Included on a different file for conciseness
#Programed by Ryan Bao
##################################################

import os
from PIL import ImageTk
import PIL.Image
from tkinter import *
import random
from helpfulFunctions import *
def initChar(app):
    app.charX = app.width / 2
    app.charY = app.height / 2
    app.speed = 15
    app.charAnimations, app.charStats = getCharacters()
    app.charWidth = app.width // 3
    app.charHeight = app.height // 3
    app.currChar = 'char0'

def makeMove(app, dx, dy):
    legalMove = True
    print(app.mapRow, app.mapCol)
    if app.charX + dx >= app.width:
        if app.mapRow == len(app.map.generatedMap) - 1:
            app.charX -= 10
            return
        app.mapRow += 1
        app.charX = 10
        app.droppedItems = []
    elif app.charX + dx <= 0:
        if app.mapRow == 0:
            app.charX += 10
            return
        app.mapRow -= 1
        app.droppedItems = []
        app.charX = app.width - 10
    elif app.charY + dy >= app.height:
        if app.mapCol == 0:
            print('here!')
            app.charY -= 10
            return
        app.mapCol -= 1
        app.charY = 10
        app.droppedItems = []
    elif app.charY + dy <= 0:
        if app.mapCol == len(app.map.generatedMap) -1:
            print('here3!')
            app.charY += 10
            print(app.charY)
            return
        app.mapCol += 1
        app.charY = app.height - 10
        app.droppedItems = []
    testX, testY = app.charX + dx, app.charY + dy
    for obstacle, x, y in app.map.generatedMap[app.mapRow][app.mapCol].obstacles:
        if rectangleIntersect((testX + 50, testY + 50, testX - 50, testY - 50), obstacle.getBounds(x, y)):
            legalMove = False
    for item, x, y in app.droppedItems:
        if distance(testX, testY, x, y) <= 40:
            item.amount += 1
            app.droppedItems.remove((item, x, y))
    if legalMove:
        app.charX += dx
        app.charY += dy
    else:
        app.charX -= dx
        app.charY -= dy

#Creates a dictionary of characters with the keys mapping to 
#Lists of the frames of each character
def getCharacters():
    characterAnimations = {}
    characterStats = {}
    i = 0
    for character in os.listdir('charImages'):
        if not os.path.isfile(character):
            characterAnimations[character] = dict()
            characterStats[character] = charStats(character)
            for moveType in os.listdir('charImages/' + character):
                if not os.path.isfile('charImages/' + character + '/' + moveType):
                    moves = moveType.split('.')
                    if moves[-1] != 'ini':
                        characterAnimations[character][moveType] = getFrames(
                                                                character, moveType)
    #cleanThisShitUp(characterAnimations)
    return characterAnimations, characterStats

#Loops through each of the frames in the character folder and returns a list
#of the frames
def getFrames(character, moveType):
    frames = []
    for frame in os.listdir('charImages/' + character + '/' + moveType):
        if frame.split('.')[-1] != 'ini':
            frameImage = PIL.Image.open('charImages/' + character + '/' + moveType + '/' + frame)
            resizedImage = frameImage.resize((100, 100))
            frames.append(resizedImage)
    return frames

#Cleans up the character list by removing any files that are not .png
def cleanThisShitUp(characters):
    for character in characters:
        for moveType in characters[character]:
            for frame in characters[character][moveType]:
                if frame.split('.')[-1] != 'png':
                    characters[character][moveType].remove(frame)
    return characters

def makeTheseUsable(characters, width, height):
    for character in characters:
        for frame in range(len(characters[character])):

            characters[character][frame] = tempImage

#Each character will have five stats. Strength, constitution, dexterity, 
#intelligence, and luck. The first four are predetermined, and luck will be 
#Left to random chance from 0-10. 
def charStats(char):
    stats = None
    ldict = {}
    exec('stats = ' +  char + 'Stats()\nprint(locals())', globals(), ldict)
    stats = ldict['stats']
    stats['luck'] = random.randint(0, 10)
    stats['dirFaced'] = 'up'
    return stats

#Character 1 is imagined to be a larger male, with high strength
#and constitution, but low dexterity, intelligence
def char0Stats():
    stats = dict()
    stats['strength'] = 7
    stats['constitution'] = 6
    stats['dexterity'] = 4
    stats['intelligence'] = 3
    stats['attType'] = 'sweep'
    stats['hitPoints'] = 120
    stats['initHitPoints'] = 120
    return stats

#Character 2 is imagined to be a smaller female, designed as a mage 
#Low strength, mid constitution and dexterity, and high intelligence
def char1Stats():
    stats = dict()
    stats['strength'] = 3
    stats['constitution'] = 5
    stats['dexterity'] = 6
    stats['intelligence'] = 10
    stats['attType'] = 'magic'
    stats['hitPoints'] = 90
    stats['initHitPoints'] = 90
    return stats

#Character 3 is imagined to be a middle-sized androgynous male, designed as a
#archer. 
#Mid strength and constitution and intelligence, high dexterity
def char2Stats():
    stats = dict()
    stats['strength'] = 5
    stats['constitution'] = 5
    stats['intelligence'] = 6
    stats['dexterity'] = 8
    stats['attType'] = 'ranged'
    stats['hitPoints'] = 100
    stats['initHitPoints'] = 100
    return stats

#Character 4 is imagined to be a smaller female, designed as an assassin/rogue
#Mid strength, high intelligence, dexterity, mid constitution
def char3Stats():
    stats = dict()
    stats['strength'] = 5
    stats['intelligence'] = 7
    stats['dexterity'] = 7
    stats['constitution'] = 4
    stats['attType'] = 'stab'
    stats['hitPoints'] = 120
    stats['initHitPoints'] = 120
    return stats

