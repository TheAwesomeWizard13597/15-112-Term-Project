from helpfulFunctions import *

def initPaused(app):
    app.keyBindingsButton = (50, 3*app.height / 5, app.width / 2 - 50, 4*app.height / 5, 'Change Keybindings!')
    app.resetButton = (app.width / 2 + 50, 3*app.height / 5, app.width - 50, 4*app.height / 5, 'Start Over!')
    app.pauseButtons = [app.keyBindingsButton, app.resetButton]
    app.resetConfirmationButton = (100, app.height / 2 , app.width / 2 - 50, app.height / 2 + 300,
                                   'Yes!')
    app.resetDenialButton = (app.width / 2 + 50, app.height / 2 , app.width - 100, app.height / 2 + 300,
                                   'No!')
    app.resetConfirmation = False
    app.keyBindingChange = False

def drawPaused(app, canvas):
    canvas.create_rectangle(50, app.height / 5, app.width - 50, 2 * app.height / 5, fill = 'grey')
    canvas.create_text(midpoint(app.width, 0), midpoint(app.height / 5, 2 * app.height / 5),
                       text = 'Paused!', font = 'Arial 24 bold')
    for x0, y0, x1, y1, text in app.pauseButtons:
        canvas.create_rectangle(x0, y0, x1, y1, fill = 'grey')
        canvas.create_text(midpoint(x0, x1), midpoint(y0, y1), text = text,
                           font = 'Arial 24 bold')

def drawResetConfirmation(app, canvas):
    canvas.create_rectangle(50, 150, app.width - 50, app.height - 150, fill = 'light grey')
    canvas.create_text(midpoint(app.width, 0), midpoint(0, app.height / 2),
                       text = 'Are you sure you want to start over?', font = 'Arial 24 bold')
    canvas.create_text(midpoint(app.width, 0), midpoint(0, app.height / 2 + 80),
                       text='This cannot be undone!', font = 'Arial 16 bold')
    for x0, y0, x1, y1, text in [app.resetConfirmationButton, app.resetDenialButton]:
        canvas.create_rectangle(x0, y0, x1, y1, fill = 'grey')
        canvas.create_text(midpoint(x0, x1), midpoint(y0, y1), text = text, font = 'Arial 24 bold')

def pauseMousePressed(app, event):
    if pointInRectangle((event.x, event.y), app.resetButton[0:4]):
        print('here!')
        app.resetConfirmation = True
    if pointInRectangle((event.x, event.y), app.keyBindingsButton[0:4]):
        app.keyBindingChange = True