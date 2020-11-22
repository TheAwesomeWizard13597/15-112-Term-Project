from itemCode import *
from helpfulFunctions import *

def damageCalculator(charStats, item):
    print(charStats, item)
    if item.damageType == 'magic':
        damage = charStats['intelligence'] * item.strength
    if item.damageType == 'piercing':
        damage = 0.5 * charStats['dexterity'] * item.strength
    if item.damageType == 'slashing':
        damage = 0.3 * charStats['dexterity'] * charStats['strength'] * item.strength
    if item.damageType == 'crushing':
        damage = 0.5 * charStats['strength'] * item.strength
    return damage
'''
def doesHit(charX, charY, enemyX, enemyY, currObstaclePositions):
    slope = (enemyY - charY) / (enemyX - charX)
    for (x, y) in currObstaclePositions:
'''
def attack(app):
    destroyed = []
    if app.charStats[app.currChar]['attType'] == 'magic':

        for obstacle, x, y in app.map.generatedMap[app.mapRow][app.mapCol].obstacles:
            if lineInRectangle((app.charX, app.charY), (event.x, event.y), obstacle.getBounds(x, y)):
                obstacle.hitPoints -= damageCalculator(app.charStats[app.currChar], app.equippedWeapon)
                if obstacle.hitPoints <= 0:
                    destroyed.append((obstacle, x, y))
        for enemy in app.map.generatedMap[app.mapRow][app.mapCol].enemies:
            if lineInRectangle((app.charX, app.charY), (event.x, event.y), enemy.getBounds()):
                enemy.stats['hitpoints'] -= damageCalculator(app.charStats[app.currChar], app.equippedWeapon)
                if enemy.stats['hitpoints'] <= 0:
                    destroyed.append(enemy)
        return destroyed
    elif app.charStats[app.currChar]['attType'] == 'magic':
        smallestDist = None
        closestObj = None
        for obstacle, x, y in app.map.generatedMap[app.mapRow][app.mapCol].obstacles:
            if lineInRectangle((app.charX, app.charY), (event.x, event.y), obstacle.getBounds(x, y)):
                obsX1, obsY1, obsX2, obsY2 = obstacle.getBounds(x, y)
                minDistance = min(distance(app.charX, app.charY, obsX1, obsY1),
                                  distance(app.charX, app.charY, obsX2, obsY2),
                                  distance(app.charX, app.charY, obsX1, obsY2),
                                  distance(app.charX, app.charY, obsX2, obsY1))
                if minDistance < smallestDist:
                    smallestDist = minDistance
                    closestObj = obstacle, x, y
        for enemy in app.map.generatedMap[app.mapRow][app.mapCol].enemies:
            if lineInRectangle((app.charX, app.charY), (event.x, event.y), enemy.getBounds):
                enemX1, enemY1, enemX2, enemY2 = (enemy.getBounds())
                minDistance = min(distance(app.charX, app.charY, enemX1, enemY1),
                                  distance(app.charX, app.charY, enemX2, enemY2),
                                  distance(app.charX, app.charY, enemX1, enemY2),
                                  distance(app.charX, app.charY, enemX2, enemY1))
                if minDistance < smallestDist:
                    smallestDist = minDistance
                    closestObj = enemy
        if type(closestObj) == tuple:
            closestObj[0].hitPoints -= damageCalculator(app.charStats[app.currChar], app.equippedWeapon)
            if closestObj[0].hitPoints <= 0:
                destroyed.append(closestObj)
        else:
            closestObj.hitPoints -= damageCalculator(app.charStats[app.currChar], app.equippedWeapon)
            if closestObj.hitPoints <= 0:
                destroyed.append(closestObj)
    elif app.charStats[app.currChar]['attType'] == 'sweep':
        print('here!')
        for obstacle, x, y in app.map.generatedMap[app.mapRow][app.mapCol].obstacles:
            if distance(app.charX, app.charY, x, y) <= 100:
                print('obstacle!', obstacle.hitPoints)
                obstacle.hitPoints -= damageCalculator(app.charStats[app.currChar], app.equippedWeapon)
                if obstacle.hitPoints <= 0:
                    destroyed.append((obstacle, x, y))
        for enemy in app.map.generatedMap[app.mapRow][app.mapCol].enemies:
            if distance(app.charX, app.charY, enemy.x, enemy.y) <= 30:
                enemy.stats['hitpoints'] -= damageCalculator(app.charStats[app.currChar], app.equippedWeapon)
                if enemy.stats['hitpoints'] <= 0:
                    destroyed.append(enemy)
    else: pass
    return destroyed