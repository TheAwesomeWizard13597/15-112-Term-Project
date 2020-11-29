def initInventory(app):
    app.invMargin = 20
    app.invRows = 10
    app.invCols = 10
    app.invCoords = [(6, 0), (6, 1), (6, 2), (6, 4), (6, 3), (6, 5), (6, 6), (6, 7), (6, 8), (6, 9), (7, 9), (7, 9), (7, 8), (7, 7), (7, 5), (7, 5), (7, 4), (7, 2), (7, 0), (8, 0), (8, 2), (7, 1), (8, 1), (8, 3), (7, 3), (8, 4), (8, 5), (8, 6), (7, 6), (9, 8), (8, 7), (9, 7), (9, 9), (8, 9), (8, 8), (9, 6), (9, 5), (9, 4), (9, 3), (9, 2), (9, 1), (9, 0)]
    app.helmetCoords = (1, 6)
    app.chestCoords = (2, 6)
    app.leggingCoords = (3, 6)
    app.bootCoords = (4, 6)
    app.inventory = False

def drawInventory(app, canvas):
    canvas.create_rectangle(0, 0, app.height, app.width, fill = 'red')
    for row in range(app.invRows):
        for col in range(app.invCols):
            x0, y0, x1, y1 = getInvCellBounds(app, row, col)
            if (row, col) in app.invTest:
                color = 'blue'
            else:
                color = 'white'
            canvas.create_rectangle(x0, y0, x1, y1, fill = color)


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


