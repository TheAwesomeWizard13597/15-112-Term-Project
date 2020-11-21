import os
import pandas as pd

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

    def getBounds(self): #Returns (x0, x1, y0, y1)
        return self.x + self.width / 2, self.x - self.width / 2, self.y + self.height / 2, self.y - self.height / 2

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def setInitialPos(self, x, y):
        self.x = x
        self.y = y

    def reset(self):
        self.moveType = 'idle'

    def attack(self):
        self.moveType = 'attack'

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
    for moveType in dir:
        frames[moveType] = []
        for frame in dir + '/' + moveType:
            if frame.split('.')[-1] == 'png':
                pathName = dir + '/' + moveType + '/' + frame
                image = PIL.Image.open(pathName)
                frames[moveType].append(image)
    return frame

print(getEnemies())
