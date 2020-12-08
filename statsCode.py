from helpfulFunctions import *
def initStats(app):
    app.enemyKilled = 0
    app.obstaclesDestroyed = 0
    app.stepsTaken = 0
    app.itemsCollected = 0
    app.deaths = 0


def drawStats(app, canvas):
    mid = app.width // 2
    stats = [('Enemies Killed', app.enemyKilled),
                 ('Obstacles Destroyed', app.obstaclesDestroyed),
                 ('Steps taken', app.stepsTaken),
                 ('Items Collected', app.itemsCollected),
                 ('Deaths', app.deaths)]
    for i in range(len(stats)):
        text, stat = stats[i]
        font = 'Arial 16 bold'
        canvas.create_text(midpoint(mid, 0), 3 * app.height / 4 + 30 * i, text = text, font = font)
        canvas.create_text(midpoint(mid, app.width), 3 * app.height / 4 + 30 * i, text = str(stat), font = font)