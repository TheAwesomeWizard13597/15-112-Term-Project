from helpfulFunctions import *
from itemCode import *
from enemyCode import *
import random, copy
import PIL.Image


def generateMapApp(app):
    seed = app.getUserInput('Enter a seed here! Leave blank for a random seed')
    app.map = mapData(app.size, app.width, app.height, seed = seed)
    if app.size == 'large':
        app.mapRow = app.mapCol = 4
    elif app.size == 'medium':
        app.mapRow = app.mapCol = 3
    else:
        app.mapRow = app.mapCol = 2
    app.mapCreation = False
    app.normalPlay = True


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
    def __init__(self, size, chunkWidth, chunkHeight, seed = None):
        emptyMap = generateEmptyMap(size)
        if seed == None:
            seed = random.randint(0, 100000000000000)
        else:
            seed = hash(seed)
#            print('AAAAAAAAAA LOOK AT ME' + str(type(seed)))
        self.generatedMap = generateMap(emptyMap, chunkWidth, chunkHeight, seed)

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
    def __init__(self, width, height, seed):
        self.obstacles = generateChunkObstacles(width, height, seed)
        self.enemies = generateEnemies(width, height, seed)
        self.objectives = []
        self.treasure = []

def getObstacleImages():
    obstacles = dict()
    for imageFile in os.listdir('obstacles/images'):
        if imageFile.split('.')[-1] != 'ini':
            image = PIL.Image.open('obstacles/images/' + imageFile)
            obstacles[imageFile.split('.')[0]] = image
    return obstacles

def getObstacles():
    junkItems = getJunkItems()
    obstacleImages = getObstacleImages()
    largeRock = obstacle('large rock', 100, 100, obstacleImages['rock'].resize((100, 100)), 10, junkItems['rock'])
    mediumRock = obstacle('medium rock', 75, 75, obstacleImages['rock'].resize((75, 75)), 10, junkItems['rock'])
    smallRock = obstacle('small rock', 50, 50, obstacleImages['rock'].resize((50, 50)), 10, junkItems['rock'])
    largeTree = obstacle('large tree', 100, 100, obstacleImages['rock'].resize((100, 100)), 10, junkItems['wood'])
    mediumTree = obstacle('medium tree', 75, 75, obstacleImages['rock'].resize((75, 75)), 10, junkItems['wood'])
    smallTree = obstacle('small tree', 50, 50, obstacleImages['rock'].resize((50, 50)), 10, junkItems['wood'])
    return (largeRock, mediumRock, smallRock, largeTree, mediumTree, smallTree)

def generateEnemies(width, height, seed):
    random.seed(a = seed)
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
        if isLegalObstacle:
            enemies.append(tempEnemy)
    return enemies



def generateChunkObstacles(width, height, seed):
    obstacleLocations = []
    numObstacles = random.randint(1, 10)
    obstacles = getObstacles()
    obstacleCounts = dict()
    random.seed(a = seed)
    while len(obstacleLocations) < numObstacles:
        obstacleXPos = random.randint(0, width)
        obstacleYPos = random.randint(0, height)
        tempObstacle = copy.deepcopy(random.choice(obstacles))
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
        
        

def generateMap(emptyMap, width, height, seed):
    size = len(emptyMap)
    generatedMap = make2dList(size, size)
    random.seed(a = seed)
    for row in range(size):
        for col in range(size):
            if seed > 0:
                randomizer = random.randint(0, seed)
            else:
                randomizer = random.randint(seed, 0)
            generatedMap[row][col] = chunk(width, height, seed)
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
