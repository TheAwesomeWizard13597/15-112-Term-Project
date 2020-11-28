import os, math
import pandas as pd
import PIL
from helpfulFunctions import *
from combatCode import *

def enemyMove(app):
    for enemy in app.map.generatedMap[app.mapRow][app.mapCol].enemies:
        if enemy.stats['attType'] in ['sweep', 'stab']:
            if distance(enemy.x, enemy.y, app.charX, app.charY) <= 100:
                enemy.attack(app)
            else:
                meleeEnemyMove(app, 15, enemy)
        else:
            attack = True
            if 150 < distance(enemy.x, enemy.y, app.charX, app.charY) < 300:
                rangedEnemyMove(app, 15, enemy)
                attack = False
            for obstacle, x, y in app.map.generatedMap[app.mapRow][app.mapCol].obstacles:
                if lineInRectangle2((enemy.x, enemy.y), (app.charX, app.charY), obstacle.getBounds(x, y)):
                    rangedEnemyMove(app, 15, enemy)
                    attack = False
            if attack:
                enemy.attack(app)


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
        return self.x + self.width / 2, self.y + self.height / 2, self.x - self.width / 2, self.y - self.height / 2

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
        destroyed = []
        if self.stats['attType'] == 'magic':
            for obstacle, x, y in app.map.generatedMap[app.mapRow][app.mapCol].obstacles:
                if lineInRectangle((app.charX, app.charY), (self.x, self.y), obstacle.getBounds(x, y)):
                    obstacle.hitPoints -= damageCalculator(app.charStats[app.currChar], app.weaponItems[self.stats['weapon']])
                    if obstacle.hitPoints <= 0:
                        destroyed.append((obstacle, x, y))
            app.charStats[app.currChar]['hitPoints'] -= damageCalculator(self.stats, app.weaponItems[self.stats['weapon']])
        elif self.stats['attType'] == 'ranged':
            smallestDist = None
            closestObj = None
            app.charStats[app.currChar]['hitPoints'] -= damageCalculator(self.stats, app.weaponItems[self.stats['weapon']])
        elif self.stats['attType'] == 'sweep':

            for obstacle, x, y in app.map.generatedMap[app.mapRow][app.mapCol].obstacles:
                if distance(self.x, self.y, x, y) <= 100:
                    print('obstacle!', obstacle.hitPoints)
                    obstacle.hitPoints -= damageCalculator(app.charStats[app.currChar], app.weaponItems[self.stats['weapon']])
                    if obstacle.hitPoints <= 0:
                        destroyed.append((obstacle, x, y))
        else:
            pass
        print(app.charStats[app.currChar]['hitPoints'])

    def getBoundsTestLoc(self, x, y):
        return (x + self.width / 2, y + self.height / 2, x - self.width / 2, y - self.height / 2 )

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

def meleeEnemyMove(app, theta, enemy):
    possibleMoves = []
    for i in range(360 // theta):
        testX, testY = enemy.x + 10 * math.cos(i * theta), enemy.y + 10 * math.sin(i * theta)
        legalMove = True
        for obstacle, x, y in app.map.generatedMap[app.mapRow][app.mapCol].obstacles:
            if (rectangleIntersect(obstacle.getBounds(x, y), enemy.getBoundsTestLoc(testX, testY)) and 0 < testX < app.width and 0 < testY < app.height):
                legalMove = False
        for x, y in enemy.prevMoves:
            if distance(x, y, testX, testY) < 1:
                legalMove = False
        if legalMove:
            possibleMoves.append((testX, testY))

    smallestF = None
    bestMove = None
    for x, y in possibleMoves:
        #g = distance(enemy.startX, enemy.startY, x, y)
        g = 10 * len(enemy.prevMoves) + 10
        h = distance(x, y, app.charX, app.charY)
        f = g + h
        if smallestF == None or f < smallestF:
            smallestF = f
            bestMove = (x, y)
    enemy.x = bestMove[0]
    enemy.y = bestMove[1]
    print(enemy.getBoundsTestLoc(enemy.x, enemy.y))
    enemy.prevMoves.append((int(bestMove[0]), int(bestMove[1])))

def rangedEnemyMove(app, theta, enemy):
    possibleMoves = []
    for i in range(360 // theta):
        print('flag2')
        testX, testY = enemy.x + 10 * math.cos(i * theta), enemy.y + 10 * math.sin(i * theta)
        legalMove = True
        for obstacle, x, y in app.map.generatedMap[app.mapRow][app.mapCol].obstacles:
            if (rectangleIntersect(obstacle.getBounds(x, y), enemy.getBoundsTestLoc(testX, testY)) and 0 < testX < app.width and 0 < testY < app.height):
                legalMove = False
                print('here!')
        for x, y in enemy.prevMoves:
            if distance(x, y, testX, testY) < 1:
                print('here2!')
                legalMove = False
        if legalMove:
            possibleMoves.append((testX, testY))
    print(possibleMoves)
    if distance(enemy.x, enemy.y, app.charX, app.charY) > 300: #try to get closer
        smallestF = None
        bestMove = None
        for x, y in possibleMoves:
            # g = distance(enemy.startX, enemy.startY, x, y)
            g = 10 * len(enemy.prevMoves) + 10
            h = distance(x, y, app.charX, app.charY)
            f = g + h
            if smallestF == None or f < smallestF:
                smallestF = f
                bestMove = (x, y)
        enemy.x = bestMove[0]
        enemy.y = bestMove[1]
        enemy.prevMoves.append((int(bestMove[0]), int(bestMove[1])))
    elif distance(enemy.x, enemy.y, app.charX, app.charY) < 200: #too close
        smallestF = None
        bestMove = None
        for x, y in possibleMoves:
            # g = distance(enemy.startX, enemy.startY, x, y)
            g = 10 * len(enemy.prevMoves) + 10
            h = distance(x, y, app.charX, app.charY)
            f = g - h
            if smallestF == None or f < smallestF:
                smallestF = f
                bestMove = (x, y)
        enemy.x = bestMove[0]
        enemy.y = bestMove[1]
        enemy.prevMoves.append((int(bestMove[0]), int(bestMove[1])))
    else: #Out of line of sight
        bestMove = None
        smallestDiff = None
        for x, y in possibleMoves:
            dist = abs(distance(x, y, app.charX, app.charY) - 200)
            if smallestDiff == None or dist < smallestDiff:
                bestMove = (x, y)
                smallestDiff = dist
        enemy.x = bestMove[0]
        enemy.y = bestMove[1]
        enemy.prevMoves.append((int(bestMove[0]), int(bestMove[1])))


