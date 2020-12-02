from inventoryCode import *
from helpfulFunctions import *

def initCrafting(app):
    app.crafting = False
    app.craftingGridCoords = [(1, 1), (1, 2), (1, 3), (2, 1),
                        (2, 2), (2, 3), (3, 1), (3, 2), (3, 3)]
    resetCraftGrid(app)
    app.craftingRecipes = getCraftingRecipes(app)
    app.craftingResults = None

def resetCraftGrid(app):
    app.craftingGrid = make2dList(3, 3)

def drawCrafting(app, canvas):
    canvas.create_rectangle(0, 0, app.height, app.width, fill = app.colorPalette['grassColor'])
    gridWidth = app.width - 2 * app.invMargin
    cellWidth = gridWidth // app.invCols
    inventory = copy.copy(app.inv)
    inventory.reverse()
    #print(inventory)
    for (row, col) in app.invCoords:
        x0, y0, x1, y1 = getInvCellBounds(app, row, col)
        if len(inventory) > 0:
            item = inventory.pop()
            resizedImage = item.imageSource.resize((cellWidth, cellWidth))
            image = ImageTk.PhotoImage(resizedImage)
            canvas.create_image(midpoint(x0, x1), midpoint(y0, y1), image = image)
            canvas.create_text(x1 - 10, y1 - 10, text = f'x{item.amount}')
        else:
            canvas.create_rectangle(x0, y0, x1, y1, fill = 'white')
    for (row, col) in app.craftingGridCoords:
        x0, y0, x1, y1 = getInvCellBounds(app, row, col)
        if app.craftingGrid[row - 1][col - 1] == None:
            canvas.create_rectangle(x0, y0, x1, y1, fill = 'white')
        else:
            resizedImage = app.craftingGrid[row-1][col-1].imageSource.resize((cellWidth, cellWidth))
            image = ImageTk.PhotoImage(resizedImage)
            canvas.create_image(midpoint(x0, x1), midpoint(y0, y1), image=image)
    if app.craftingResults != None:
        x0, y0, x1, y1 = getInvCellBounds(app, 2, 8)
        resizedImage = app.craftingResults.imageSource.resize((cellWidth, cellWidth))
        image = ImageTk.PhotoImage(resizedImage)
        canvas.create_image(midpoint(x0, x1), midpoint(y0, y1), image = image)

def getCraftingRecipes(app):
    clubRecipe = [[None, app.junkItems['rock'], None],
                  [None, app.junkItems['rock'], None],
                  [None, app.junkItems['wood'], None],
                  app.weaponItems['club']]
    clubRecipe1 = [[None, None, app.junkItems['rock']],
                  [None, None, app.junkItems['rock']],
                  [None, None, app.junkItems['wood']],
                  app.weaponItems['club']]
    clubRecipe2 = [[app.junkItems['rock'], None, None],
                   [app.junkItems['rock'], None, None],
                   [app.junkItems['wood'], None, None],
                   app.weaponItems['club']]

    return([clubRecipe, clubRecipe1, clubRecipe2])

def craftingRecipesEq(recipe1, recipe2):
    for row in range(3):
        for col in range(3):
            if recipe1[row][col] == None and recipe2[row][col] != None:
                return False
            if recipe2[row][col] == None and recipe1[row][col] != None:
                return False
            if recipe1[row][col] == None and recipe2[row][col] == None:
                continue
            if recipe1[row][col].name != recipe2[row][col].name:
                return False
    return True

def craftingMousePressed(app, event):
    cell = getInvCell(app, event.x, event.y)
    if cell in app.invCoords:
        index = app.invCoords.index(cell)
        if index < len(app.inv):
            app.currInvItem = app.inv[index]
    if cell == (2, 8) and app.craftingResults != None:
        app.craftingResults.amount += 1
        getInv(app)
        resetCraftGrid(app)
        app.craftingResults = None
    if cell in app.craftingGridCoords and app.currInvItem != None:
        if app.craftingGrid[cell[0] - 1][cell[1] - 1] != None:
            app.craftingGrid[cell[0] - 1][cell[1] - 1].amount += 1
            app.craftingGrid[cell[0] - 1][cell[1] - 1] = None
        if app.currInvItem.amount >= 1:
            app.craftingGrid[cell[0] - 1][cell[1] - 1] = app.currInvItem
            app.currInvItem.amount -= 1
            app.currInvItem = None
            for recipe in app.craftingRecipes:
                print(app.craftingGrid, recipe)
                if craftingRecipesEq(recipe[0:3], app.craftingGrid):
                    app.craftingResults = recipe[3]
    elif cell in app.craftingGridCoords and app.currInvItem == None:
        if app.craftingGrid[cell[0] - 1][cell[1] - 1] != None:
            app.craftingGrid[cell[0] - 1][cell[1] - 1].amount += 1
            app.craftingGrid[cell[0] - 1][cell[1] - 1] = None


