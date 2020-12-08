from helpfulFunctions import *
from itemCode import *
from adamCode import *
from enemyCode import *
import random, copy
import PIL.Image
def initMap(app):
    app.mapCreationOffset = app.height / 6
    app.enemies = getEnemies()
    app.obstacles = getObstacles(app)

def drawMapCreationScreen(app, canvas):
    canvas.create_rectangle(0, app.mapCreationOffset, app.width / 3, app.height)
    canvas.create_rectangle(app.width / 3, app.mapCreationOffset, app.width * 2 / 3, app.height)
    canvas.create_rectangle(app.width * 2 / 3, app.mapCreationOffset, app.width, app.height)
    canvas.create_line(0, app.mapCreationOffset, app.width, app.mapCreationOffset)
    canvas.create_text(app.width / 2, app.mapCreationOffset / 2,
                        text = 'Map Creator',
                        font = 'Arial 20 bold')
    canvas.create_text(app.width / 6, (app.height + app.mapCreationOffset) / 2,
                        text = 'Small Map!')
    canvas.create_text(app.width / 2, (app.height + app.mapCreationOffset) / 2,
                        text = 'Medium Map!')
    canvas.create_text(app.width * 5/ 6, (app.height + app.mapCreationOffset) / 2,
                        text = 'Large Map!')

def generateMapApp(app):
    seed = app.getUserInput('Enter a seed here! Leave blank for a random seed')
    app.map = mapData(app.size, app.width, app.height, app, seed = seed)
    if app.size == 'large':
        app.mapRow = app.mapCol = app.initMapRow = app.initMapCol = 4
    elif app.size == 'medium':
        app.mapRow = app.mapCol = app.initMapRow = app.initMapCol = 3
    else:
        app.mapRow = app.mapCol = app.initMapRow = app.initMapCol = 2
    initSpecials(app)
    app.mapCreation = False
    app.normalPlay = True
    print(len(app.map.generatedMap))

def initSpecials(app):
    initAdam(app)
def mapCreationMousePressed(app, event):
    if event.y > app.mapCreationOffset:
        if event.x < app.width / 3:
            app.size = 'small'
        elif event.x < app.width * 2 / 3:
            app.size = 'medium'
        else:
            app.size = 'large'
    generateMapApp(app)


class obstacle():
    def __init__(self, name, height, width, imageFile, hitPoints, drops):
        self.height = height
        self.width = width
        self.imageFile = imageFile
        self.hitPoints = hitPoints
        self.drops = drops
        self.name = name
    
    def getBounds(self, xpos, ypos):
        return((xpos + self.width / 2, ypos + self.height / 2,
                xpos - self.width / 2, ypos - self.height / 2))

class mapData():
    def __init__(self, size, chunkWidth, chunkHeight, app, seed = None):
        emptyMap = generateEmptyMap(size)
        if seed == None:
            seed = random.randint(0, 100000000000000)
        else:
            seed = hash(seed)
#            print('AAAAAAAAAA LOOK AT ME' + str(type(seed)))
        self.generatedMap = generateMap(emptyMap, chunkWidth, chunkHeight, seed, app)

def generateEmptyMap(size):
    print('generating empty map')
    if size == 'small':
        mapSize = 3
    elif size == 'medium':
        mapSize = 5
    elif size == 'large':
        mapSize = 7
    
    return make2dList(mapSize, mapSize)

class chunk():
    def __init__(self, width, height, seed, app):
        self.obstacles = generateChunkObstacles(width, height, seed, app)
        self.enemies = generateEnemies(width, height, seed, self.obstacles)
        self.objectives = []
        self.treasure = []

def getObstacleImages():
    obstacles = dict()
    for imageFile in os.listdir('obstacles/images'):
        if imageFile.split('.')[-1] != 'ini':
            image = PIL.Image.open('obstacles/images/' + imageFile)
            obstacles[imageFile.split('.')[0]] = image
    return obstacles

def getObstacles(app):
    obstacleImages = getObstacleImages()
    largeRock = obstacle('large rock', 100, 100, obstacleImages['largeRock'].resize((100, 100)), 10, app.junkItems['rock'])
    mediumRock = obstacle('medium rock', 75, 75, obstacleImages['mediumRock'].resize((75, 75)), 10, app.junkItems['rock'])
    smallRock = obstacle('small rock', 50, 50, obstacleImages['smallRock'].resize((50, 50)), 10, app.junkItems['rock'])
    largeTree = obstacle('large tree', 100, 100, obstacleImages['largeTree'].resize((100, 100)), 10, app.junkItems['wood'])
    mediumTree = obstacle('medium tree', 75, 75, obstacleImages['mediumTree'].resize((75, 75)), 10, app.junkItems['wood'])
    smallTree = obstacle('small tree', 50, 50, obstacleImages['tree'].resize((50, 50)), 10, app.junkItems['wood'])
    return (largeRock, mediumRock, smallRock, largeTree, mediumTree, smallTree)

def generateEnemies(width, height, seed, obstacles):
    #random.seed(a = seed)
    enemies = []
    enemyList = getEnemies()
    numEnemies = random.randint(1, 3)
    while len(enemies) <= numEnemies:
        xPos = random.randint(0, width) + 300
        yPos = random.randint(0, height) + 300
        tempEnemy = copy.deepcopy(random.choice(enemyList))
        tempEnemy.setInitialPos(xPos, yPos)
        isLegalObstacle = True
        for pos in tempEnemy.getBounds():
            if pos < 0 or pos > max(width, height):
                isLegalObstacle = False
                break
        for enemy in enemies:
            if rectangleIntersect(enemy.getBounds(), tempEnemy.getBounds()):
                isLegalObstacle = False
                break
        for obstacle, x, y in obstacles:
            if rectangleIntersect(tempEnemy.getBounds(), obstacle.getBounds(x, y)):
                isLegalObstacle = False
                break
        if isLegalObstacle:
            enemies.append(tempEnemy)
    return enemies



def generateChunkObstacles(width, height, seed, app):
    obstacleLocations = []
    numObstacles = random.randint(1, 10)
    obstacleCounts = dict()
    #random.seed(a = seed)
    while len(obstacleLocations) < numObstacles:
        obstacleXPos = random.randint(0, width)
        obstacleYPos = random.randint(0, height)
        tempObstacle = copy.copy(random.choice(app.obstacles))
        isLegalObstacle = True
        bounds = tempObstacle.getBounds(obstacleXPos, obstacleYPos)
        for elem in bounds:
            if elem < 0 or elem > max(width, height):
                isLegalObstacle = False
                break
        for obstacle, xpos, ypos in obstacleLocations:
            obstacleBounds = obstacle.getBounds(xpos, ypos)
            tempObstacleBounds = tempObstacle.getBounds(obstacleXPos, obstacleYPos)
            if rectangleIntersect(obstacleBounds, tempObstacleBounds):
                isLegalObstacle = False
                break
        if isLegalObstacle:
            obstacleLocations.append((tempObstacle, obstacleXPos, obstacleYPos))
    return obstacleLocations
        
        

def generateMap(emptyMap, width, height, seed, app):
    size = len(emptyMap)
    generatedMap = make2dList(size, size)
    random.seed(a = seed)
    for row in range(size):
        for col in range(size):
            if seed > 0:
                randomizer = random.randint(1, seed)
            else:
                randomizer = random.randint(seed, 0)
            generatedMap[row][col] = chunk(width, height, seed/randomizer, app)
    return generatedMap
            

def printMap(generatedMap):
    size = len(generatedMap)
    for row in range(size):
        for col in range(size):
            for obstacle, xpos, ypos in generatedMap[row][col]:
                print(obstacle.name, xpos, ypos) 

def printChunk(chunk):
    for obstacle, x, y in chunk:
        print('(' + obstacle.name + str(x) + str(y) + ')', end = ' ')

def areChunksEqual(chunk1, chunk2):
    if len(chunk1) != len(chunk2):
        return False
    for i in range(len(chunk1)):
        obstacle0, x0, y0 = chunk1[i]
        obstacle1, x1, y1 = chunk2[i]
        if obstacle0.name != obstacle1.name:
            return False
        elif x0 != x1:
            return False
        elif y0 != y1:
            return False
    return True

def areMapsEqual(map1, map2):
    if len(map1) != len(map2):
        return False
    if len(map1[0]) != len(map2[0]):
        return False
    rows, cols = len(map1), len(map1[0])
    for row in range(rows):
        for col in range(cols):
            if not areChunksEqual(map1[row][col], map2[row][col]):
                return False
    return True

####Image Citations
# http://pngimg.com/imgs/nature/stone/
# http://pngimg.com/download/3498
