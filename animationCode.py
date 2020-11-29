from enemyCode import *

def resetAnimations(app):

    app.normalMove = False
    app.charAttack = False
    app.pickUp = False
    app.idle = True
    defineMoveType(app)
    app.charAnimCount = 0
    app.currFrame = 0

def charAnimation(app):
    if app.charAnimCount >= len(app.charAnimations[app.currChar][app.moveType]):
        resetAnimations(app)
        defineMoveType(app)
    app.currFrame = (app.charAnimCount % len(app.charAnimations[app.currChar][app.moveType]))
    app.charAnimCount += 1



def enemAnimation(app):
    for enemy in app.map.generatedMap[app.mapRow][app.mapCol].enemies:
        if enemy.currFrame >= len(enemy.frames[enemy.moveType]) - 1:
            enemy.reset()
        else:
            enemy.currFrame += 1

def defineMoveType(app):
    if app.pickUp:
        app.moveType = 'pickUp'
    elif app.charAttack:
        app.moveType = 'attack'
    elif app.normalMove:
        app.moveType = 'normalMove'
    else:
        app.moveType = 'idle'