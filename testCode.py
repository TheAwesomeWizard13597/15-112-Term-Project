from helpfulFunctions import *
from enemyCode import *
import copy

def initTest(app):
    app.obstaclePlacement = False
    app.obstaclePlacementButton = (app.width - 10, 100, app.width - 100, 10, 'obstacle')
    app.enemyPlacement = False
    app.enemyPlacementButton = (app.width - 10, 200, app.width - 100, 110, 'enemy')
    app.arrowPlacement = False
    app.arrowPlacementButton = (app.width - 10, 300, app.width - 100, 210, 'arrow')
    app.teleport = False
    app.teleportButton = (app.width - 10, 400, app.width - 100, 310, 'teleport')
    app.refreshHealthButton = (app.width - 10, 500, app.width - 100, 410, 'health')
    app.godModeButton = (app.width - 10, 600, app.width - 100, 510, 'Godmode')
    app.addItemButton = (app.width - 10, 700, app.width - 100, 610, 'Add items')
    app.testButtons = [app.obstaclePlacementButton, app.enemyPlacementButton,
                       app.arrowPlacementButton, app.teleportButton, app.refreshHealthButton,
                       app.godModeButton, app.addItemButton]
    app.test = (app.obstaclePlacement, app.enemyPlacement, app.arrowPlacement, app.teleport)
    app.godMode = False


def drawTest(app, canvas):
    canvas.create_rectangle(app.width - 110, 0, app.width, app.height, fill = 'white')
    for x0, y0, x1, y1, text in app.testButtons:
        canvas.create_rectangle(x0, y0, x1, y1, fill = 'light blue')
        canvas.create_text(midpoint(x0, x1), midpoint(y0, y1), text = text)

def setAllTestFalse(app):
    app.obstaclePlacement = False
    app.enemyPlacement = False
    app.arrowPlacement = False
    app.teleport = False

def mousePressedTest(app, event):
    print(event.x, event.y)
    print(app.obstaclePlacement, app.enemyPlacement, app.arrowPlacement, app.teleport)
    if pointInRectangle((event.x, event.y), (app.width, app.height, app.width - 110, 0)):
        if pointInRectangle((event.x, event.y), app.obstaclePlacementButton[0:4]):
            setAllTestFalse(app)
            app.obstaclePlacement = True
        if pointInRectangle((event.x, event.y), app.enemyPlacementButton[0:4]):
            setAllTestFalse(app)
            app.enemyPlacement = True
        if pointInRectangle((event.x, event.y), app.arrowPlacementButton[0:4]):
            setAllTestFalse(app)
            app.arrowPlacement = True
        if pointInRectangle((event.x, event.y), app.teleportButton[0:4]):
            setAllTestFalse(app)
            app.teleport = True
        if pointInRectangle((event.x, event.y), app.refreshHealthButton[0:4]):
            app.charStats[app.currChar]['hitPoints'] = app.charStats[app.currChar]['initHitPoints']
        if pointInRectangle((event.x, event.y), app.godModeButton[0:4]):

            app.godMode = not app.godMode
            print('godMode!', app.godMode)
        if pointInRectangle((event.x, event.y), app.addItemButton[0:4]):
            item = app.getUserInput('item?')
            amount = int(app.getUserInput('amount?'))
            if item in app.junkItems:
                app.junkItems[item].amount += amount
            elif item in app.armorItems:
                app.armorItems[item].amount += amount
            elif item in app.weaponItems:
                app.weaponItems[item].amount += amount
            else:
                print('youre dumb as fuck')

    else:
        print('here!')
        if app.obstaclePlacement:
            app.map.generatedMap[app.mapRow][app.mapCol].obstacles.append((app.obstacles[1], event.x, event.y))
        if app.enemyPlacement:
            enemy = copy.copy(app.enemies[0])
            enemy.setInitialPos(event.x, event.y)
            app.map.generatedMap[app.mapRow][app.mapCol].enemies.append(enemy)
        if app.arrowPlacement:
            dx = int(app.getUserInput('dx'))
            dy = int(app.getUserInput('dy'))
            launcher = app.getUserInput('launcher')
            app.arrows.append(Arrow(event.x, event.y, dx, dy, launcher))
        if app.teleport:
            app.charX, app.charY = event.x, event.y
        setAllTestFalse(app)

