from helpfulFunctions import *
from itemCode import *
import random, copy


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
        self.enemies = []
        self.objectives = []
        self.treasure = []

def getObstacles():
    junkItems = getJunkItems()
    largeRock = obstacle('large rock', 100, 100, '/obstacles/images/rock', 10, junkItems['rock'])
    mediumRock = obstacle('medium rock', 75, 75, '/obstacles/images/rock', 10, junkItems['rock'])
    smallRock = obstacle('small rock', 50, 50, '/obstacles/images/rock', 10, junkItems['rock'])
    largeTree = obstacle('large tree', 100, 100, '/obstacles/images/tree', 10, junkItems['wood'])
    mediumTree = obstacle('medium tree', 75, 75, '/obstacles/images/tree', 10, junkItems['wood'])
    smallTree = obstacle('small tree', 50, 50, '/obstacles/images/tree', 10, junkItems['wood'])
    return (largeRock, mediumRock, smallRock, largeTree, mediumTree, smallTree)

def generateChunkObstacles(width, height, seed):
    print('chunk generating!')
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
            if pointInRectangle(obstacleBounds, tempObstacleBounds):
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

map1 = mapData('large', 500, 500, seed = 1239875123)
print(map1.generatedMap[1][1].obstacles[1][0].name)
print(map1.generatedMap)

        