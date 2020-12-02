from itemCode import *
from helpfulFunctions import *
from arrowCode import *

def damageCalculator(charStats, item, targetArmor = None):
    if item.damageType == 'magic':
        damage = charStats['intelligence'] * item.strength
    if item.damageType == 'piercing':
        damage = 0.5 * charStats['dexterity'] * item.strength
    if item.damageType == 'slashing':
        damage = 0.3 * charStats['dexterity'] * charStats['strength'] * item.strength
    if item.damageType == 'crushing':
        damage = 0.5 * charStats['strength'] * item.strength
    return (damage)
'''
def doesHit(charX, charY, enemyX, enemyY, currObstaclePositions):
    slope = (enemyY - charY) / (enemyX - charX)
    for (x, y) in currObstaclePositions:
'''
def playerAttack(app, event):
    factor = 10
    destroyed = []
    if app.charStats[app.currChar]['attType'] == 'magic':

        for obstacle, x, y in app.map.generatedMap[app.mapRow][app.mapCol].obstacles:
            if lineInRectangle((app.charX, app.charY), (event.x, event.y), obstacle.getBounds(x, y)):
                obstacle.hitPoints -= damageCalculator(app.charStats[app.currChar], app.equippedWeapon)
                if obstacle.hitPoints <= 0:
                    destroyed.append((obstacle, x, y))
        for enemy in app.map.generatedMap[app.mapRow][app.mapCol].enemies:
            if lineInRectangle((app.charX, app.charY), (event.x, event.y), enemy.getBounds()):
                print('here!')
                enemy.stats['hitpoints'] -= damageCalculator(app.charStats[app.currChar], app.equippedWeapon)
                if enemy.stats['hitpoints'] <= 0:
                    destroyed.append(enemy)
        return destroyed
    elif app.charStats[app.currChar]['attType'] == 'ranged':
        dy = -(event.y - app.charY) / factor
        dx = (event.x - app.charX) / factor
        app.arrows.append(Arrow(app.charX, app.charY, dx, dy, 'player'))
    elif app.charStats[app.currChar]['attType'] == 'sweep':
        for obstacle, x, y in app.map.generatedMap[app.mapRow][app.mapCol].obstacles:
            if distance(app.charX, app.charY, x, y) <= 100:
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

