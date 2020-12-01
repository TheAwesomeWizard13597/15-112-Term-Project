import math
import PIL, random
from helpfulFunctions import *


class Arrow():
    def __init__(self, x, y, dx, dy, launcher):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.angleFace = math.atan2(self.dy, self.dx)
        self.image, self.width, self.height = getArrowImgFile()
        self.point = (
        (self.width / 2) * math.cos(self.angleFace) + self.x, self.y - (self.width / 2) * math.sin(self.angleFace))
        self.launcher = launcher

    def move(self):
        self.x += self.dx
        self.y -= self.dy
        self.point = (self.point[0] + self.dx, self.point[1] - self.dy)


def getArrowImgFile():
    image = PIL.Image.open('arrow.png')
    width, height = image.size
    factor = 10
    resizedImage = image.resize((width // factor, height // factor))
    return resizedImage, width / factor, height / factor


def moveArrow(app):
    for arrow in app.arrows:
        arrow.move()
        arrowRemoved = False
        for obstacle, x, y in app.map.generatedMap[app.mapRow][app.mapCol].obstacles:
            if pointInRectangle(arrow.point, obstacle.getBounds(x, y)):
                obstacle.hitPoints -= 100
                if obstacle.hitPoints <= 100:
                    destroy(app, (obstacle, x, y))
                app.arrows.remove(arrow)
                arrowRemoved = True
                break
        if not arrowRemoved:
            if arrow.launcher == 'player':
                for enemy in app.map.generatedMap[app.mapRow][app.mapCol].enemies:
                    if pointInRectangle(arrow.point, enemy.getBounds()):
                        enemy.stats['hitpoints'] -= 100
                        if enemy.stats['hitpoints'] <= 100:
                            destroy(app, enemy)
                        app.arrows.remove(arrow)
                        arrowRemoved = True
                        break
            elif arrow.launcher == 'enemy':
                if pointInRectangle(arrow.point, (app.charX + 50, app.charY + 50, app.charX - 50, app.charY - 50)):
                    app.charStats[app.currChar]['hitPoints'] -= 100
                    if app.charStats[app.currChar]['hitPoints'] <= 0:
                        app.dead = True
                    app.arrows.remove(arrow)
                    arrowRemoved = True
        if not arrowRemoved:
            if arrow.x >= app.width or arrow.x <= 0 or arrow.y >= app.height or arrow.y <= 0:
                app.arrows.remove(arrow)


def destroy(app, elem):
    if isinstance(elem, tuple):
        droppedItem = elem[0].drops
        app.droppedItems.append((droppedItem, elem[1], elem[2]))
        app.map.generatedMap[app.mapRow][app.mapCol].obstacles.remove(elem)
    else:
        droppedItem = itemDrop(app)
        app.droppedItems.append((droppedItem, elem.x, elem.y))
        app.map.generatedMap[app.mapRow][app.mapCol].enemies.remove(elem)
        app.enemyKilled += 1
        print(f'{app.enemyKilled}here!!!')
        if app.enemyKilled >= 10:
            print('flag!')
            app.won = True


def itemDrop(app):
    itemProbability = random.randint(0, 100)
    if itemProbability < (100 - app.uncommonProbability - app.rareProbability):
        item = random.choice(app.drops['junk'])
        app.uncommonProbability += 5
        app.rareProbability += 1
    elif itemProbability < (100 - app.rareProbability):
        item = random.choice(app.drops['uncommon'])
        app.uncommonProbability = 25
        app.rareProbability += 1
    else:
        item = random.choice(app.drops['rare'])
        app.uncommonProbability = 25
        app.rareProbability = 5
    return item

# Image from https://in.pinterest.com/pin/796363146601078700/
