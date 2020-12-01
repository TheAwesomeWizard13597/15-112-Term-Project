from helpfulFunctions import *

def initDead(app):
    app.restartButtonDead = (100, app.height/2, app.width - 100, app.height - 100, 'Restart!')
    app.dead = False

def drawDeathScreen(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'grey')
    x0, y0, x1, y1, text = app.restartButtonDead
    canvas.create_rectangle(x0, y0, x1, y1, fill = 'red')
    canvas.create_text(midpoint(x0, x1), midpoint(y0, y1), text = text, font = 'Arial 36 bold')
    canvas.create_text(midpoint(x0, x1), midpoint(0, y0), text = 'You Died',fill = 'red', font = 'Arial 36 bold')