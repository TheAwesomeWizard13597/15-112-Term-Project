from mapCode import *
from PIL import ImageTk

def initBuild(app):
    app.buildMode = False
    app.buildRows = 20
    app.buildCols = 20
    app.buildings = []
    app.buildTemplates = getBuildTemplates(app)
    app.craftingList = []
    app.currBuild = None
    app.hoverRow = app.hoverCol = 0
    app.hoverCount = 0

class Building(obstacle):
    def __init__(self, name, imageFile, hitPoints, requirements = []):
        self.name = name
        self.hitPoints = hitPoints
        self.imageFile = imageFile
        self.width, self.height = imageFile.size
        self.requirements = requirements

    def getBounds(self, x, y):
        return ((x + self.width / 2, y + self.height / 2,
                 x - self.width / 2, y - self.height / 2))

    def __eq__(self, other):
        return(isinstance(other, Building) and self.name == other.name)



def buildModeMousePressed(app, event):
    if ((app.charY >= app.height / 2 and pointInRectangle((event.x, event.y), (0, 0, app.width, 100))) or
         (app.charY <= app.height / 2 and pointInRectangle((event.x, event.y), (0, app.height, app.width, app.height - 100)))):
        for i in range(len(app.buildTemplates)):
            building = app.buildTemplates[i]
            if app.charY >= app.height / 2 and pointInRectangle((event.x, event.y), building.getBounds(75 * (i) + 50, 50)):
                if app.currBuild == building:
                    app.currBuild = None
                else:
                    app.currBuild = building
            if app.charY < app.height / 2 and pointInRectangle((event.x, event.y), building.getBounds(75 * (i) + 50, app.height - 50)):
                if app.currBuild == building:
                    app.currBuild = None
                else:
                    app.currBuild = building
    elif app.currBuild != None:
        if app.currBuild.name == 'destroy':
            for obstacle, x, y in app.map.generatedMap[app.mapRow][app.mapCol].obstacles:
                if pointInRectangle((event.x, event.y), obstacle.getBounds(x, y)) and isinstance(obstacle, Building):
                    row, col = getBuildCell(app, x, y)
                    app.buildings.remove((obstacle, row, col))
                    app.map.generatedMap[app.mapRow][app.mapCol].obstacles.remove((obstacle, x, y))
            return
        isBuild = True
        for item, req in app.currBuild.requirements:
            if item.amount < req:
                isBuild = False
            else:
                item.amount -= req
        row, col = getBuildCell(app, event.x, event.y)
        if isBuild and isLegalBuild(app, event.x, event.y):

            app.buildings.append((app.currBuild, row, col))
            x0, y0, x1, y1 = getBuildCellBounds(app, row, col)
            app.map.generatedMap[app.mapRow][app.mapCol].obstacles.append((app.currBuild, midpoint(x0, x1), midpoint(y0, y1)))
        else:
            print('flag!')
            app.hoverCol, app.hoverRow = col, row
            app.hoverCount = 5
            print(app.hoverCount)


def isLegalBuild(app, x, y):
    row, col = getBuildCell(app, x, y)
    for obstacle, x, y in app.map.generatedMap[app.mapRow][app.mapCol].obstacles:
        if rectangleIntersect(obstacle.getBounds(x, y), getBuildCellBounds(app, row, col)):
            return False
    return True

def getBuildTemplates(app):
    images = getBuildImages(app)
    stoneBrick = Building('stoneBrick', images['stoneBrick'], 500, requirements = [(app.junkItems['rock'], 3)])
    woodWall = Building('woodWall', images['woodWall'], 300)
    destroy = Building('destroy', images['destroy'], None)
    return[stoneBrick, woodWall, destroy]

def getBuildImages(app):
    width, height = getBuildCellSize(app)
    buildings = dict()
    for imageFile in os.listdir('buildImages'):
        if imageFile.split('.')[-1] != 'ini':
            image = PIL.Image.open('buildImages/' + imageFile)
            resizedImage = image.resize((width, height))
            buildings[imageFile.split('.')[0]] = resizedImage
    return buildings

def drawBuildScreen(app, canvas):
    if app.buildMode and (app.mapRow, app.mapCol) == (app.initMapRow, app.initMapCol):
        for row in range(app.buildRows):
            for col in range(app.buildCols):
                x0, y0, x1, y1 = getBuildCellBounds(app, row, col)
                canvas.create_rectangle(x0, y0, x1, y1)
        drawBuilds(app, canvas)
        x0, y0, x1, y1 = getBuildCellBounds(app, app.hoverRow, app.hoverCol)
        print(app.hoverCount)
        if app.hoverCount > 0:
            print('here!')
            canvas.create_rectangle(x0, y0, x1, y1, fill = 'red')

    elif (app.mapRow, app.mapCol) == (app.initMapRow, app.initMapCol):
        drawBuilds(app, canvas)
def drawBuilds(app, canvas):
    for building, row, col in app.buildings:
        x0, y0, x1, y1 = getBuildCellBounds(app, row, col)
        image = ImageTk.PhotoImage(building.imageFile)
        canvas.create_image(midpoint(x0, x1), midpoint(y0, y1), image = image)

def drawBuildMenu(app, canvas):
    if app.buildMode and (app.mapRow, app.mapCol) == (app.initMapRow, app.initMapCol):
        if app.charY >= app.height / 2:
            canvas.create_rectangle(0, 0, app.width, 100, fill = 'pink')
            for i in range(len(app.buildTemplates)):

                building = app.buildTemplates[i]
                image = ImageTk.PhotoImage(building.imageFile)
                canvas.create_image(75 * (i) + 50, 50, image=image)
        else:
            canvas.create_rectangle(0, app.height, app.width, app.height - 100, fill = 'pink')
            for i in range(len(app.buildTemplates)):

                building = app.buildTemplates[i]
                image = ImageTk.PhotoImage(building.imageFile)
                canvas.create_image(75 * (i) + 50, app.height - 50, image = image)
#From course notes
def pointInGrid(app, x, y):
    # return True if (x, y) is inside the grid defined by app.
    return ((app.invMargin <= x <= app.width-app.invMargin) and
            (app.invMargin <= y <= app.height-app.invMargin))

def getBuildCell(app, x, y):
    # aka "viewToModel"
    # return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
    if (not pointInGrid(app, x, y)):
        return (-1, -1)
    gridWidth  = app.width
    gridHeight = app.height
    cellWidth  = gridWidth / app.buildCols
    cellHeight = gridHeight / app.buildRows

    # Note: we have to use int() here and not just // because
    # row and col cannot be floats and if any of x, y, app.invMargin,
    # cellWidth or cellHeight are floats, // would still produce floats.
    row = int(y / cellHeight)
    col = int(x / cellWidth)

    return (row, col)

def getBuildCellSize(app):
    return (app.width // app.buildCols, app.height // app.buildRows)

def getBuildCellBounds(app, row, col):
    # aka "modelToView"
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    gridWidth  = app.width
    gridHeight = app.height
    cellWidth = gridWidth / app.buildCols
    cellHeight = gridHeight / app.buildRows
    x0 = col * cellWidth
    x1 = (col+1) * cellWidth
    y0 = row * cellHeight
    y1 = (row+1) * cellHeight
    return (x0, y0, x1, y1)

# Images from
# https://www.tynker.com/minecraft/blocks/view/stonebrick/stone-brick-2/59a18e2f1c36d1f0608b456b
# https://toppng.com/wood-tile-set-wooden-wall-pixel-art-PNG-free-PNG-Images_187884
# http://clipart-library.com/transparent-axe-cliparts.html