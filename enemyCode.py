import os, math
import pandas as pd
import PIL
from helpfulFunctions import *

class Enemy(object):
    def __init__(self, x, y, frames, statistics):
        self.x = x
        self.y = y
        self.frames = frames
        self.height = 100
        self.width = 100
        self.stats = statistics
        self.moveType = 'idle'
        self.currFrame = 0
        self.prevMoves = []

    def getBounds(self): #Returns (x0, x1, y0, y1)
        return self.x + self.width / 2, self.x - self.width / 2, self.y + self.height / 2, self.y - self.height / 2

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def setInitialPos(self, x, y):
        self.x = x
        self.y = y
        self.startX = x
        self.startY = y

    def reset(self):
        self.moveType = 'idle'
        self.currFrame = 0

    def attack(self, app):
        self.moveType = 'attack'
        if self.stats['attType'] == 'magic':
            for obstacle, x, y in app.map.generatedMap[app.mapRow][app.mapCol].obstacles:
                if lineInRectangle((app.charX, app.charY), (event.x, event.y), obstacle.getBounds(x, y)):
                    obstacle.hitPoints -= damageCalculator(app.charStats[app.currChar], app.weaponStats[self.stats['weapon']])
                    if obstacle.hitPoints <= 0:
                        destroyed.append((obstacle, x, y))
            app.charStats[app.currChar]['hitPoints'] -= damageCalculator(enemy.stats, app.weaponStats[self.stats['weapon']])
        elif self.stats['attType'] == 'ranged':
            smallestDist = None
            closestObj = None
            app.charStats[app.currChar]['hitPoints'] -= damageCalculator(enemy.stats, app.weaponStats[self.stats['weapon']])
        elif self.stats['attType'] == 'sweep':

            for obstacle, x, y in app.map.generatedMap[app.mapRow][app.mapCol].obstacles:
                if distance(self.x, self.y, x, y) <= 100:
                    print('obstacle!', obstacle.hitPoints)
                    obstacle.hitPoints -= damageCalculator(app.charStats[app.currChar], app.weaponStats[self.stats['weapon']])
                    if obstacle.hitPoints <= 0:
                        destroyed.append((obstacle, x, y))
        else:
            pass

def getEnemies():
    enemyList = []
    enemyDf = pd.read_csv('enemies/enemyStats.csv', index_col='Enemy')
    for enemyName, enemyStats in enemyDf.iterrows():
        frames = getFrames(enemyName)
        enemyList.append(Enemy(None, None, frames, enemyStats))
    return enemyList

def getFrames(name):
    frames = dict()
    dir = 'enemies/images/' + name
    for moveType in os.listdir(dir):
        if moveType.split('.')[-1] != 'ini':

            frames[moveType] = []
            for frame in os.listdir(dir + '/' + moveType):
                if frame.split('.')[-1] == 'png':
                    pathName = dir + '/' + moveType + '/' + frame
                    image = PIL.Image.open(pathName)
                    resziedImage = image.resize((100, 100))
                    frames[moveType].append(resziedImage)
    return frames

def enemyMove(app, theta, enemy):
    possibleMoves = []
    for i in range(360 // theta):
        testX, testY = enemy.x + 10 * math.cos(i * theta), enemy.y + 10 * math.sin(i * theta)
        for obstacle, x, y in app.map.generatedMap[app.mapRow][app.mapCol].obstacles:
            if (not pointInRectangle((testX, testY), obstacle.getBounds(x, y)) and 0 < testX < app.width and 0 < testY < app.height and not (int(testX), int(testY)) in enemy.prevMoves):
                possibleMoves.append((testX, testY))
    smallestF = None
    bestMove = None
    print(possibleMoves)
    print(enemy.startX, enemy.startY)
    for x, y in possibleMoves:
        #g = distance(enemy.startX, enemy.startY, x, y)
        g = 10 * len(enemy.prevMoves) + 10
        h = distance(x, y, app.charX, app.charY)
        f = g + h
        if smallestF == None or f < smallestF:
            smallestF = f
            bestMove = (x, y)
    print(bestMove, smallestF)
    enemy.x = bestMove[0]
    enemy.y = bestMove[1]
    enemy.prevMoves.append((int(bestMove[0]), int(bestMove[1])))

print(getEnemies())
