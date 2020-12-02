from helpfulFunctions import *
from itemCode import *
from PIL import ImageTk
import copy, random

def initInventory(app):
    app.invMargin = 20
    app.invRows = 10
    app.invCols = 10
    app.invCoords = [(6, 0), (6, 1), (6, 2), (6, 4), (6, 3), (6, 5), (6, 6), (6, 7), (6, 8), (6, 9), (7, 9), (7, 9), (7, 8), (7, 7), (7, 5), (7, 5), (7, 4), (7, 2), (7, 0), (8, 0), (8, 2), (7, 1), (8, 1), (8, 3), (7, 3), (8, 4), (8, 5), (8, 6), (7, 6), (9, 8), (8, 7), (9, 7), (9, 9), (8, 9), (8, 8), (9, 6), (9, 5), (9, 4), (9, 3), (9, 2), (9, 1), (9, 0)]
    app.helmetCoords = (1, 6)
    app.chestCoords = (2, 6)
    app.leggingCoords = (3, 6)
    app.bootCoords = (4, 6)
    app.weaponCoords = (2, 8)
    app.inventory = False
    app.invAnimationCount = 0
    app.invCurrFrame = 0
    app.inv = []
    app.helmet = None
    app.chestplate = None
    app.leggings = None
    app.boots = None

def isCompatibleAtt(item, attackType):
    if attackType == 'sweep':
        return(item.damageType in ['crushing','slashing'])
    if attackType == 'magic':
        return(item.damageType in ['magic'])
    if attackType == 'ranged':
        return(item.damageType in ['range'])

def isCompatibleArmor(item, type):
    if item == None:
        return False
    if not isinstance(item, armorItem):
        return False
    if item.type != type:
        return False
    return True


def drawInventory(app, canvas):
    canvas.create_rectangle(0, 0, app.height, app.width, fill = app.colorPalette['grassColor'])
    gridWidth = app.width - 2 * app.invMargin
    cellWidth = gridWidth // app.invCols
    for row in range(app.invRows):
        for col in range(app.invCols):
            x0, y0, x1, y1 = getInvCellBounds(app, row, col)
            if (row, col) in [app.helmetCoords, app.chestCoords, app.leggingCoords, app.bootCoords]:
                color = 'white'
                canvas.create_rectangle(x0, y0, x1, y1, fill=color)
    inventory = copy.copy(app.inv)
    inventory.reverse()
    #print(inventory)
    for (row, col) in app.invCoords:
        x0, y0, x1, y1 = getInvCellBounds(app, row, col)
        canvas.create_rectangle(x0, y0, x1, y1, fill='white')
        if len(inventory) > 0:
            item = inventory.pop()
            resizedImage = item.imageSource.resize((cellWidth, cellWidth))
            image = ImageTk.PhotoImage(resizedImage)
            canvas.create_image(midpoint(x0, x1), midpoint(y0, y1), image = image)
            canvas.create_text(x1 - 10, y1 - 10, text = f'x{item.amount}')

    if app.helmet != None:
        x0, y0, x1, y1 = getInvCellBounds(app, app.helmetCoords[0], app.helmetCoords[1])
        resizedImage = app.helmet.imageSource.resize((cellWidth, cellWidth))
        image = ImageTk.PhotoImage(resizedImage)
        canvas.create_image(midpoint(x0, x1), midpoint(y0, y1), image = image)
    if app.chestplate != None:
        x0, y0, x1, y1 = getInvCellBounds(app, app.chestCoords[0], app.chestCoords[1])
        resizedImage = app.chestplate.imageSource.resize((cellWidth, cellWidth))
        image = ImageTk.PhotoImage(resizedImage)
        canvas.create_image(midpoint(x0, x1), midpoint(y0, y1), image = image)
    if app.leggings != None:
        x0, y0, x1, y1 = getInvCellBounds(app, app.leggingCoords[0], app.leggingCoords[1])
        resizedImage = app.leggings.imageSource.resize((cellWidth, cellWidth))
        image = ImageTk.PhotoImage(resizedImage)
        canvas.create_image(midpoint(x0, x1), midpoint(y0, y1), image = image)
    if app.boots != None:
        x0, y0, x1, y1 = getInvCellBounds(app, app.bootCoords[0], app.bootCoords[1])
        resizedImage = app.boots.imageSource.resize((cellWidth, cellWidth))
        image = ImageTk.PhotoImage(resizedImage)
        canvas.create_image(midpoint(x0, x1), midpoint(y0, y1), image = image)
    if app.equippedWeapon != None:
        x0, y0, x1, y1 = getInvCellBounds(app, app.weaponCoords[0], app.weaponCoords[1])
        resizedImage = app.equippedWeapon.imageSource.resize((cellWidth, cellWidth))
        image = ImageTk.PhotoImage(resizedImage)
        canvas.create_image(midpoint(x0, x1), midpoint(y0, y1), image = image)
    for char in ['char0']:
        resizedImage = app.charAnimations[char]['idle'][app.invCurrFrame].resize((4*cellWidth, 4*cellWidth))
        image = ImageTk.PhotoImage(resizedImage)
        x0, y0, trash, trash1 = getInvCellBounds(app, 1, 1)
        trash2, trash3, x1, y1 = getInvCellBounds(app, 4, 4)
        canvas.create_image(midpoint(x0, x1), midpoint(y0, y1), image = image)
def getInv(app):
    itemList = list(app.junkItems.values()) + list(app.armorItems.values()) + list(app.weaponItems.values())
    inventory = []
    for item in itemList:
        if item.amount > 0 and item.imageSource != None:
            inventory.append(item)
    print(inventory)
    app.inv = inventory

def doStepInv(app):
    inventoryAnimation(app)

def inventoryAnimation(app):
    if app.invAnimationCount >= 5:
        app.invAnimationCount = 0
    app.invCurrFrame = app.invAnimationCount % 5
    app.invAnimationCount += 1

#From course notes
def pointInGrid(app, x, y):
    # return True if (x, y) is inside the grid defined by app.
    return ((app.invMargin <= x <= app.width-app.invMargin) and
            (app.invMargin <= y <= app.height-app.invMargin))

def getInvCell(app, x, y):
    # aka "viewToModel"
    # return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
    if (not pointInGrid(app, x, y)):
        return (-1, -1)
    gridWidth  = app.width - 2*app.invMargin
    gridHeight = app.height - 2*app.invMargin
    cellWidth  = gridWidth / app.invCols
    cellHeight = gridHeight / app.invRows

    # Note: we have to use int() here and not just // because
    # row and col cannot be floats and if any of x, y, app.invMargin,
    # cellWidth or cellHeight are floats, // would still produce floats.
    row = int((y - app.invMargin) / cellHeight)
    col = int((x - app.invMargin) / cellWidth)

    return (row, col)

def getInvCellBounds(app, row, col):
    # aka "modelToView"
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    gridWidth  = app.width - 2*app.invMargin
    gridHeight = app.height - 2*app.invMargin
    cellWidth = gridWidth / app.invCols
    cellHeight = gridHeight / app.invRows
    x0 = app.invMargin + col * cellWidth
    x1 = app.invMargin + (col+1) * cellWidth
    y0 = app.invMargin + row * cellHeight
    y1 = app.invMargin + (row+1) * cellHeight
    return (x0, y0, x1, y1)


