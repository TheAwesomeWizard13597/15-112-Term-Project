from helpfulFunctions import *

def initKeyBindings(app):
    app.keybindings = {'togglePause': 'Escape',
                       'toggleTestMode': '`',
                       'toggleInventory':'i',
                       'toggleCrafting':'x',
                       'toggleCharSelect':'c',
                       'moveUp':'w',
                       'moveDown':'s',
                       'moveRight':'d',
                       'moveLeft':'a',
                       'toggleBuild': 'b',
                       'specialMove': 'e'
                        }
    app.keyBindingButtons = ([(50, 100*i + 25, app.width / 2 - 50, 100 * i + 75) for i in range(10)] +
                            [(app.width / 2 + 25, 100*i + 25, app.width - 50, 100*i + 75) for i in range(10)])

def drawChangeKeyBindings(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'light grey')
    keybindList = list(app.keybindings)
    for i in range(len(app.keyBindingButtons)):
        x0, y0, x1, y1 = app.keyBindingButtons[i]

        canvas.create_rectangle(x0, y0, x1, y1, fill = 'grey')
        midLine = midpoint(midpoint(x0, x1), x1)
        if i < len(keybindList):
            canvas.create_text(midpoint(x0, midLine), midpoint(y0, y1), text = keybindList[i],
                               font = 'Arial 16 bold')
            canvas.create_text(midpoint(midLine, x1), midpoint(y0, y1), text = app.keybindings[keybindList[i]],
                               font = 'Arial 16 bold')
