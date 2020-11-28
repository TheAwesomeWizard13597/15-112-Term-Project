import math
import PIL
from helpfulFunctions import *

class Arrow():
    def __init__(self, x, y, dx, dy, launcher):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.angleFace = math.atan2(self.dy, self.dx)
        self.image, self.width, self.height = getArrowImgFile()
        self.point = ((self.width / 2)*math.cos(self.angleFace), (self.width / 2) * math.sin(self.angleFace))
        self.launcher = launcher

    def move(self):
        self.x += self.dx
        self.y += self.dy
        self.point = (self.point[0] + self.dx, self.point[1] + self.dy)


def getArrowImgFile():
    image = PIL.Image.open('arrow.png')
    width, height = image.size
    factor = 10
    resizedImage = image.resize((width // factor, height // factor))
    return resizedImage, width / factor, height / factor

def moveArrow(app):
    for arrow in app.arrows:
        arrow.move()
        for obstacle, x, y in app.map.generatedMap[app.mapRow][app.mapCol].obstacles:
            if pointInRectangle(arrow.point, obstacle.getBounds(x, y)):
                obstacle.hitPoints -= 100
                if obstacle.hitPoints <= 100:
                    app.map.generatedMap[app.mapRow][app.mapCol].obstacles.remove((obstacle, x, y))
                app.arrows.remove(arrow)
        if arrow.launcher == 'player':
            for enemy in app.map.generatedMap[app.mapRow][app.mapCol].enemies:
                if pointinRectangle(arrow.point, enemy.getBounds()):
                    enemy.stats['hitpoints'] -= 100
                    if enemy.stats['hitpoints'] <= 100:
                        app.map.generatedMap[app.mapRow][app.mapCol].enemies.remove(enemy)
                    app.arrows.remove(arrow)
        elif arrow.launcher == 'enemy':
            if pointInRectangle(arrow.point, (app.charX + 50, app.charY + 50, app.charX - 50, app.charY - 50)):
                app.charStats[app.currChar]['hitPoints'] -= 100
        
