from enemyCode import *
from arrowCode import *
from PIL import ImageTk

def initAdam(app):
    app.adamProj = []
    app.map.generatedMap[0][0].objectives.append(Adam(app))
    for obstacle, x, y in app.map.generatedMap[0][0].obstacles:
        if rectangleIntersect(obstacle.getBounds(x, y), app.map.generatedMap[0][0].objectives[0].getBounds()):
            app.map.generatedMap[0][0].obstacles.remove((obstacle, x, y))

class adamProj(Arrow):
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.image, self.width, self.height = getProjImgFile()
        self.y = y
        self.dx = dx
        self.dy = dy
        self.angleFace = math.atan2(self.dy, self.dx)
        self.point = (
            (self.width / 2) * math.cos(self.angleFace) + self.x, self.y - (self.width / 2) * math.sin(self.angleFace))
        self.launcher = 'enemy'


def getProjImgFile():
    image = PIL.Image.open('enemies/Adam/projectile.png')
    width, height = image.size
    factor = 10
    resizedImage = image.resize((width // factor, height // factor))
    return resizedImage, width / factor, height / factor

class Adam(Enemy):
    def __init__(self, app):
        self.x = app.width / 2
        self.y = app.height / 2
        self.frames = getAdamFrames()
        self.height = 100
        self.width = 100
        self.stats = getAdamStatistics()
        self.moveType = 'idle'
        self.currFrame = 0
        self.prevMoves = []
        self.cooldown = self.initCooldown = 30


    def move(self, app):
        rangedEnemyMove(app, 15, self)

    def attack(self, app):
        if self.cooldown == 0:
            app.adamProj.append(adamProj(self.x, self.y, (app.charX - self.x) // 10, (self.y - app.charY)//10))
            self.cooldown = self.initCooldown

    def draw(self, app, canvas):
        image = ImageTk.PhotoImage(self.frames[self.moveType][self.currFrame])
        canvas.create_image(self.x, self.y, image = image)
        self.currFrame += 1
        if self.currFrame >= len(self.frames[self.moveType]):
            self.reset()
        for proj in app.adamProj:
            rotatedImage = proj.image.rotate(proj.angleFace * (180 / math.pi), expand=True)
            image = ImageTk.PhotoImage(rotatedImage)
            canvas.create_image(proj.x, proj.y, image=image)


def moveProj(app):
    for proj in app.adamProj:
        proj.move()
        projRemoved = False
        for obstacle, x, y in app.map.generatedMap[app.mapRow][app.mapCol].obstacles:
            if pointInRectangle(proj.point, obstacle.getBounds(x, y)):
                obstacle.hitPoints -= 150
                if obstacle.hitPoints <= 100:
                    destroy(app, (obstacle, x, y))
                app.adamProj.remove(proj)
                projRemoved = True
                break
        if not projRemoved:
            if pointInRectangle(proj.point, (app.charX + 50, app.charY + 50, app.charX - 50, app.charY - 50)):
                app.charStats[app.currChar]['hitPoints'] -= 30
                if app.charStats[app.currChar]['hitPoints'] <= 0:
                    app.dead = True
                app.adamProj.remove(proj)
                projRemoved = True
        if not projRemoved:
            if proj.x >= app.width or proj.x <= 0 or proj.y >= app.height or proj.y <= 0:
                app.adamProj.remove(proj)

def getAdamFrames():
    frames = dict()
    dir = 'enemies/Adam/images'
    for moveType in os.listdir(dir):
        if moveType.split('.')[-1] != 'ini':
            frames[moveType] = []
            for frame in os.listdir(dir + '/' + moveType):
                if frame.split('.')[-1] == 'png':
                    pathName = dir + '/' + moveType + '/' + frame
                    image = PIL.Image.open(pathName)
                    resizedImage = image.resize((200, 200))
                    frames[moveType].append(resizedImage)

    return frames

def getAdamStatistics():
    stats = dict()
    stats['hitpoints'] = 100
    stats['strength'] = 20
    stats['constitution'] = 20
    stats['dexterity'] = 20
    stats['intelligence'] = 20
    stats['attType'] = 'magic'
    stats['weapon'] = None
    return stats

#Images from
# https://www.freeiconspng.com/img/42439