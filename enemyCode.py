class Enemy(object):
    def __init__(self, x, y, hitPoints, imageFile):
        self.x = x
        self.y = y
        self.hitPoints = hitPoints
        self.imageFile = imageFile
        self.height = 100
        self.width = 100

    def getBounds(self): #Returns (x0, x1, y0, y1)
        return self.x + self.width / 2, self.x - self.width / 2, self.y + self.height / 2, self.y - self.height / 2

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

