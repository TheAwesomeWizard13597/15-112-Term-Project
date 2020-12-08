from imports import *
import random, threading, ctypes, time, wave
#from pydub import AudioSegment
#from pydub.playback import play
#cd "d:/Google Drive/Ze Ultimate Folder/CMU 2020-2021 (Fall)/Programming and Comp Sci/Homework/week4"


        
def appStarted(app):
    #Movement Variables
    initColors(app)
    initChar(app)
    initItems(app)
    initMap(app)
    initTimer(app)
    getAppState(app)
    resetAnimations(app)
    initTest(app)
    initInventory(app)
    initCrafting(app)
    initKeyBindings(app)
    initDead(app)
    initPaused(app)
    initBuild(app)
    app.enemyKilled = 0
    app.obstaclesDestroyed = 0
    app.stepsTaken = 0
    app.itemsCollected = 0
    app.deaths = 0
    app.arrows = []
    app.testCount = 0
    app.won = False
    pass

def getAppState(app):
    app.charSelect = False
    app.isPaused = False
    app.isDeath = False
    app.testingMode = False
    app.normalPlay = False
    app.mapCreation = True



def keyPressed(app, event):
    if app.won:
        if event.key == 't':
            appStarted(app)
        return
    if app.isPaused:
        if event.key == app.keybindings['togglePause']:
            app.isPaused = not app.isPaused
            app.normalPlay = True
        return
    if app.isDeath:
        return
    if app.switchCharacters:
        return
    if event.key == '`':
        app.testingMode = not app.testingMode
        app.normalPlay = not app.normalPlay
    if app.testingMode:
        testingModeKey(app, event)
    if app.inventory:
        if event.key == app.keybindings['toggleInventory']:
            app.inventory = False
            app.normalPlay = True
            return
        if event.key == 'q':
            print(app.invTest)
    if app.crafting:
        if event.key == app.keybindings['toggleCrafting']:
            app.normalPlay = True
            for row in range(len(app.craftingGrid)):
                for col in range(len(app.craftingGrid[0])):
                    if app.craftingGrid[row][col] != None:
                        app.craftingGrid[row][col].amount += 1
                        app.craftingGrid[row][col] = None
            app.crafting = False
            return
    if app.normalPlay:
        dx = 0
        dy = 0
        if app.charAttack:
            return
        if event.key == app.keybindings['specialMove'] and app.specialMoveCd == 0:
            app.charSpecialMove = True
        if event.key == app.keybindings['toggleCrafting']:
            getInv(app)
            app.crafting = True
            app.normalPlay = False
        if event.key == app.keybindings['toggleInventory']:
            app.inventory = True
            getInv(app)
            app.normalPlay = False
        if event.key == app.keybindings['togglePause']:
            app.normalPlay = False
            app.isPaused = True
        if event.key == app.keybindings['moveUp']:
            dy -= app.speed
            app.normalMove = True
            app.charStats['dirFaced'] = 'up'
            defineMoveType(app)
        if event.key == app.keybindings['moveDown']:
            dy += app.speed
            app.normalMove = True
            app.charStats['dirFaced'] = 'down'
            defineMoveType(app)
        if event.key == app.keybindings['moveRight']:
            dx += app.speed
            app.normalMove = True
            app.charStats['dirFaced'] = 'left'
            defineMoveType(app)
        if event.key == app.keybindings['moveLeft']:
            dx -= app.speed
            app.normalMove = True
            app.charStats['dirFaced'] = 'right'
            defineMoveType(app)
        if event.key == app.keybindings['toggleBuild']:
            app.buildMode = not app.buildMode
        if event.key == app.keybindings['toggleCharSelect']:
            app.switchCharacters = True
            app.normalPlay = False

        makeMove(app, dx, dy)

def mousePressed(app, event):
    if app.dead and not app.godMode:
        if pointInRectangle((event.x, event.y), app.restartButtonDead[0:4]):
            appStarted(app)
            return
        if pointInRectangle((event.x, event.y), app.respawnButton[0:4]):
            respawn(app)
            return
    if app.testingMode:
        mousePressedTest(app, event)
    if app.switchCharacters:
        characterSelectionMousePresesd(app, event)
        return
    if app.crafting:
        craftingMousePressed(app, event)
    if app.inventory:
        equipNewItem = False
        cell = getInvCell(app, event.x, event.y)
        if cell in app.invCoords:
            index = app.invCoords.index(cell)
            if index < len(app.inv):
                app.currInvItem = app.inv[index]
        if cell == app.helmetCoords and isCompatibleArmor(app.currInvItem, 'head'):
            app.helmet = app.currInvItem
            equipNewItem = True
        if cell == app.chestCoords and isCompatibleArmor(app.currInvItem, 'chest'):
            app.chestplate = app.currInvItem
            equipNewItem = True
        if cell == app.leggingCoords and isCompatibleArmor(app.currInvItem, 'legs'):
            app.leggings = app.currInvItem
            equipNewItem = True
        if cell == app.bootCoords and isCompatibleArmor(app.currInvItem, 'feet'):
            app.boots = app.currInvItem
            equipNewItem = True
        if cell == app.weaponCoords and isCompatibleAtt(app.currInvItem, app.charStats[app.currChar]['attType']):
            app.equippedWeapon = app.currInvItem
            equipNewItem = True
        if equipNewItem:
            app.currInvItem.amount -= 1
            app.currInvItem = None
    if app.isPaused and not app.resetConfirmation and not app.keyBindingChange:
        pauseMousePressed(app, event)
        return
    if app.keyBindingChange:
        pass
    if app.resetConfirmation:
        if pointInRectangle((event.x, event.y), app.resetConfirmationButton[0:4]):
            appStarted(app)
            return
        if pointInRectangle((event.x, event.y), app.resetDenialButton[0:4]):
            app.resetConfirmation = False
            return
    if app.mapCreation:
        mapCreationMousePressed(app, event)
        return

    if app.normalPlay:
        if app.charAttack:
            return
        if app.buildMode:
            buildModeMousePressed(app, event)
            return
        if app.charSpecialMove:
            specialMove(app, event)
            app.specialMoveCd = app.initSpecialMoveCd
            app.charSpecialMove = False
            return
        app.charAttack = not app.charAttack
        app.i = 0
        app.currFrame = 0
        defineMoveType(app)
        destroyed = playerAttack(app, event)
        for elem in destroyed:
            destroy(app, elem)

def destroy(app, elem):
    if isinstance(elem, tuple):
        droppedItem = elem[0].drops
        app.obstaclesDestroyed += 1
        app.droppedItems.append((droppedItem, elem[1], elem[2]))
        app.map.generatedMap[app.mapRow][app.mapCol].obstacles.remove(elem)
    else:
        droppedItem = itemDrop(app)
        app.droppedItems.append((droppedItem, elem.x, elem.y))
        app.map.generatedMap[app.mapRow][app.mapCol].enemies.remove(elem)
        app.enemyKilled += 1

def timerFired(app):
    if app.isPaused:
        return
    if app.inventory:
        doStepInv(app)
    if app.normalPlay:
        dostep(app)
    if app.switchCharacters:
        doStepCharSelect(app)

def dostep(app):
    moveArrow(app)
    enemyMove(app)
    for enemy in app.map.generatedMap[app.mapRow][app.mapCol].enemies:
        if enemy.stats['attType'] in ['ranged', 'magic']:
            enemy.cooldown -= 1
    for objective in app.map.generatedMap[app.mapRow][app.mapCol].objectives:
        if isinstance(objective, Adam):
            objective.move(app)
            objective.attack(app)
            moveProj(app)
            if objective.cooldown > 0:
                objective.cooldown -= 1

    if app.timerCount % 4 == 0:
        charAnimation(app)
        enemAnimation(app)
    if app.specialMoveCd > 0:
        app.specialMoveCd -= 1
    if app.hoverCount > 0:
        print('here!')
        app.hoverCount -= 1
    app.timerCount += 1

def redrawAll(app, canvas):
    if app.won:
        drawWinScreen(app, canvas)
        return
    if app.dead and not app.godMode:
        drawDeathScreen(app, canvas)
        return
    if app.crafting:
        drawCrafting(app, canvas)
        return
    if app.inventory:
        drawInventory(app, canvas)
    if app.mapCreation:
        drawMapCreationScreen(app, canvas)
    if app.switchCharacters:
        drawCharacterSelectionScreen(app, canvas)
    if app.normalPlay or app.testingMode or app.isPaused:
        drawBackground(app, canvas)
        drawBuildScreen(app, canvas)
        drawMap(app, canvas)
        drawEnemies(app, canvas)
        drawFigure(app, canvas)
        drawArrows(app, canvas)
        drawHealthBar(app, canvas)
        drawDrops(app, canvas)
        drawSpecials(app, canvas)
        drawSpecialMoveCd(app, canvas)
        drawBuildMenu(app, canvas)
        if app.testingMode:
            drawTest(app, canvas)
        if app.isPaused or app.resetConfirmation or app.keyBindingChange:
            drawPaused(app, canvas)
            if app.resetConfirmation:
                drawResetConfirmation(app, canvas)
            if app.keyBindingChange:
                drawChangeKeyBindings(app, canvas)

    # if app.testingMode:
    #     drawArrows(app, canvas)



def drawFigure(app, canvas):
#    pilImage = PIL.Image.open(app.charAnimations[app.currChar][app.moveType][app.currFrame])
#    resizedImage = pilImage.resize((app.charWidth, app.charHeight))
    image = ImageTk.PhotoImage(app.charAnimations[app.currChar][app.moveType][app.currFrame])
    imagesprite = canvas.create_image(app.charX, app.charY, image = image)

def drawBackground(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill=app.colorPalette['grassColor'])

def drawMap(app, canvas):
    for obstacle, x, y in app.map.generatedMap[app.mapRow][app.mapCol].obstacles:
        if not isinstance(obstacle, Building):
            image = ImageTk.PhotoImage(obstacle.imageFile)
            canvas.create_image(x, y, image = image)



def drawArrows(app, canvas):
    for arrow in app.arrows:
        rotatedImage = arrow.image.rotate(arrow.angleFace * (180/math.pi), expand = True)
        image = ImageTk.PhotoImage(rotatedImage)
        canvas.create_image(arrow.x, arrow.y, image = image)

def drawHealthBar(app, canvas):
    fullWidth = 150
    healthRatio = app.charStats[app.currChar]['hitPoints']/app.charStats[app.currChar]['initHitPoints']
    if healthRatio >= 0:
        healthWidth = 150 * healthRatio
    else:
        healthWidth = 0
    canvas.create_rectangle(app.width - 200, app.height - 50, app.width - (200 - fullWidth), app.height - 30, fill = 'white')
    canvas.create_rectangle(app.width - 200, app.height - 50, app.width - (200 - healthWidth), app.height - 30, fill = 'red')

def drawDrops(app, canvas):
    for item, x, y  in app.droppedItems:
        if item.imageSource != None:
            image = ImageTk.PhotoImage(item.imageSource)
            canvas.create_image(x, y, image = image)

def testingModeKey(app, event):
    if event.key == 'c':
        app.map.generatedMap[app.mapRow][app.mapCol].obstacles.clear()
    elif event.key == 'Space':
        dostep(app)
def drawEnemies(app, canvas):
    for enemy in app.map.generatedMap[app.mapRow][app.mapCol].enemies:
        image = ImageTk.PhotoImage(enemy.frames[enemy.moveType][enemy.currFrame])
        canvas.create_image(enemy.x, enemy.y, image = image)

def drawWinScreen(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = app.colorPalette['backgroundUI'])
    canvas.create_text(midpoint(0, app.width), midpoint(0, app.height),
                       text = 'YOU WON!', font = 'Arial 48 bold', fill = app.colorPalette['textColor'])
    canvas.create_text(midpoint(0, app.width), midpoint(midpoint(0, app.height), app.height),
                       text = 'Press t to restart!', font = 'Arial 24 bold',
                       fill = app.colorPalette['textColor'])

def initTimer(app):
    app.timerDelay = 50
    app.timerCount = 0

def drawSpecials(app, canvas):
    for objective in app.map.generatedMap[app.mapRow][app.mapCol].objectives:
        objective.draw(app, canvas)
'''
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
audioThread.start()'''
runApp(width = 1000, height = 1000)

