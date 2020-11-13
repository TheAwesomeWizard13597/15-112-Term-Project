from cmu_112_graphics import * 
from characterCode import *
from helpfulFunctions import *
from itemCode import *
from combatCode import * 
from mapCode import * 
import random, threading, ctypes, time, wave
#from pydub import AudioSegment
#from pydub.playback import play
cd "d:/Google Drive/Ze Ultimate Folder/CMU 2020-2021 (Fall)/Programming and Comp Sci/Homework/week4"


        
        
def appStarted(app):
    #Movement Variables
    app.charX = app.width / 2
    app.charY = app.height / 2
    app.speed = 5

    app.charAnimations, app.charStats = getCharacters()
    app.charWidth = app.width // 3
    app.charHeight = app.height // 3
    app.currChar = 'char0'

    app.timerDelay = 500
    getAppState(app)
    resetAnimations(app)


    app.weaponItems = getWeaponItems()
    app.armorItems = getArmorItems()     
    app.junkItems = getJunkItems()
    getItemDrops(app)

    app.mapCreationOffset = app.height / 6
    pass

def getItemDrops(app):
    app.drops = {'junk': list(app.junkItems.values()), 'uncommon': [], 'rare': []}
    app.rareProbability = 5
    app.uncommonProbability = 25
    for item in app.weaponItems.values():
        if item.rarity == 1:
            app.drops['uncommon'].append(item)
        elif item.rarity == 2:
            app.drops['rare'].append(item)
    for item in app.armorItems.values():
        if item.rarity == 1:
            app.drops['uncommon'].append(item)
        elif item.rarity == 2:
            app.drops['rare'].append(item)

def resetAnimations(app):

    app.normalMove = False
    app.charAttack = False
    app.pickUp = False
    app.idle = True
    defineMoveType(app)
    app.charAnimCount = 0
    app.currFrame = 0

def getAppState(app):
    app.charSelect = False
    app.isPaused = False
    app.isDeath = False
    app.testingMode = False
    app.normalPlay = False
    app.mapCreation = True

def keyPressed(app, event):
    if app.testingMode:
        audioThread.testFunc()
    if app.isPaused:
        if event.key == 'p':
            app.isPaused = not app.isPaused
        return
    if app.isDeath:
        return
    if app.charSelect:
        return
    if app.normalPlay:
        dx = 0
        dy = 0
        if event.key == 'w':
            dy -= app.speed
            app.normalMove = True
            defineMoveType(app)
        if event.key == 's':
            dy += app.speed
            app.normalMove = True
            defineMoveType(app)
        if event.key == 'd':
            dx += app.speed
            app.normalMove = True
            defineMoveType(app)
        if event.key == 'a':
            dx -= app.speed
            app.normalMove = True
            defineMoveType(app)
        if event.key == 'p':
            app.pickUp = not app.pickUp
            app.i = 0
            app.currFrame = 0
            defineMoveType(app)

        makeMove(app, dx, dy)

def mousePressed(app, event):
    if app.mapCreation:
        if event.y > app.mapCreationOffset:
            if event.x < app.width / 3:
                app.size = 'small'
            elif event.x < app.width * 2 / 3:
                app.size = 'medium'
            else:
                app.size = 'large'
        generateMapApp(app)

    if app.normalPlay:
        app.charAttack = not app.charAttack
        app.i = 0
        app.currFrame = 0
        defineMoveType(app)

def generateMapApp(app):
    seed = app.getUserInput('Enter a seed here! Leave blank for a random seed')
    app.map = mapData(app.size, app.width, app.height, seed = seed)
    app.mapCreation = False
    app.normalPlay = True

def defineMoveType(app):
    if app.pickUp:
        app.moveType = 'pickUp'
    elif app.charAttack:
        app.moveType = 'attack'
    elif app.normalMove:
        app.moveType = 'normalMove'
    else:
        app.moveType = 'idle'

def makeMove(app, dx, dy):
    if (app.charX > app.width or app.charX < 0 or app.charY > app.height   
        or app.charY < 0):
        return
    app.charX += dx
    app.charY += dy
        
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

def timerFired(app):
    if app.normalPlay:
        charAnimation(app)


def charAnimation(app):
    if app.charAnimCount >= len(app.charAnimations[app.currChar][app.moveType]):
        print('resetting!')
        resetAnimations(app)
        defineMoveType(app)
    app.currFrame = app.charAnimCount % len(app.charAnimations[app.currChar][app.moveType])
    app.charAnimCount += 1

def drawMapCreationScreen(app, canvas):
    canvas.create_rectangle(0, app.mapCreationOffset, app.width / 3, app.height)
    canvas.create_rectangle(app.width / 3, app.mapCreationOffset, app.width * 2 / 3, app.height)
    canvas.create_rectangle(app.width * 2 / 3, app.mapCreationOffset, app.width, app.height)
    canvas.create_line(0, app.mapCreationOffset, app.width, app.mapCreationOffset)
    canvas.create_text(app.width / 2, app.mapCreationOffset / 2, 
                        text = 'Map Creator',
                        font = 'Arial 20 bold') 
    canvas.create_text(app.width / 6, (app.height + app.mapCreationOffset) / 2, 
                        text = 'Small Map!')
    canvas.create_text(app.width / 2, (app.height + app.mapCreationOffset) / 2, 
                        text = 'Medium Map!')
    canvas.create_text(app.width * 5/ 6, (app.height + app.mapCreationOffset) / 2, 
                        text = 'Large Map!')
def drawFigure(app, canvas):
    pilImage = PIL.Image.open(app.charAnimations[app.currChar][app.moveType][app.currFrame])
    resizedImage = pilImage.resize((app.charWidth, app.charHeight))
    image = ImageTk.PhotoImage(resizedImage)
    imagesprite = canvas.create_image(app.charX, app.charY, image = image)

def redrawAll(app, canvas):
    if app.mapCreation:
        drawMapCreationScreen(app, canvas)
    if app.normalPlay:
        drawFigure(app, canvas)

        

class audioThread(threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.test = False
    def run(self):
        song = wave.open('song.wav', 'rb')
        print('here')
        chunk = 1024
        p = pyaudio.PyAudio
        print(song.getsampwidth())
        stream = p.open(format = p.get_format_from_width(song.getsampwidth()),#Ask about this later
                        channels = song.getnchannels(),
                        rate = song.getframerate(),
                        output = True)
        data = song.readframes(chunk)
        while data != '':
            stream.write(data)
            data = wf.readframes(chunk)
        stream.close()

    def testFunc(self):
        print('tested')
        self.test = True

audioThread = audioThread(2)
audioThread.start()
runApp(width = 300, height = 300)
time.sleep(2)

