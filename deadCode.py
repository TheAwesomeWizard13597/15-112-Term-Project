from helpfulFunctions import *
from characterCode import *
from statsCode import *
def initDead(app):
    app.restartButtonDead = (50, app.height/3, app.width / 2 - 50, app.height /2, 'Restart!')
    app.respawnButton = (app.width / 2 + 50, app.height / 3, app.width - 50, app.height /2, 'Respawn!')
    app.dead = False

def respawn(app):
    app.mapRow = app.initMapRow
    app.mapCol = app.initMapCol
    app.charX = app.width / 2
    app.charY = app.height / 2
    inventoryClear(app)
    app.charAnimations, app.charStats = getCharacters()
    app.deaths += 1
    app.normalPlay = True
    app.testingMode = False
    app.dead = False
    app.won = False


def inventoryClear(app):
    for item in app.junkItems:
        app.junkItems[item].amount = 0
    for item in app.weaponItems:
        app.weaponItems[item].amount = 0
    for item in app.armorItems:
        app.armorItems[item].amount = 0

def drawWinScreen(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'purple')
    x0, y0, x1, y1, text = app.restartButtonDead
    canvas.create_rectangle(x0, y0, x1, y1, fill = 'red')
    canvas.create_text(midpoint(x0, x1), midpoint(y0, y1), text = text, font = 'Arial 36 bold')
    x0, y0, x1, y1, text = app.respawnButton
    canvas.create_rectangle(x0, y0, x1, y1, fill='red')
    canvas.create_text(midpoint(x0, x1), midpoint(y0, y1), text='Continue!', font='Arial 36 bold')
    canvas.create_text(midpoint(0, app.width), midpoint(0, y0), text = 'You win!', font = 'Arial 36 bold')
    drawStats(app, canvas)

def drawDeathScreen(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'grey')
    x0, y0, x1, y1, text = app.restartButtonDead
    canvas.create_rectangle(x0, y0, x1, y1, fill = 'red')
    canvas.create_text(midpoint(x0, x1), midpoint(y0, y1), text = text, font = 'Arial 36 bold')
    x0, y0, x1, y1, text = app.respawnButton
    canvas.create_rectangle(x0, y0, x1, y1, fill='red')
    canvas.create_text(midpoint(x0, x1), midpoint(y0, y1), text=text, font='Arial 36 bold')
    canvas.create_text(midpoint(0, app.width), midpoint(0, y0), text = 'You Died',fill = 'red', font = 'Arial 36 bold')
    drawStats(app, canvas)