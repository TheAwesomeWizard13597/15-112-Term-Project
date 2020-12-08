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

def randomFunction(x0, y0, x1, y1):
    return math.sqrt((x0 + x1)**2 + (y0 + y1)**2)
def doesHitMelee(app, target, targetX, targetY):
    dist = distance(app.charX, app.charY, targetX, targetY)
    targetWidth, targetHeight = target.imageFile.size
    charWidth, charHeight = 100, 100
    if randomFunction(targetWidth // 2, targetHeight // 2, charWidth // 2, charHeight //2) > dist:
        return True
    return False

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
            if doesHitMelee(app, obstacle, x, y):
                obstacle.hitPoints -= damageCalculator(app.charStats[app.currChar], app.equippedWeapon)
                if obstacle.hitPoints <= 0:
                    destroyed.append((obstacle, x, y))
        for enemy in app.map.generatedMap[app.mapRow][app.mapCol].enemies:
            if distance(app.charX, app.charY, enemy.x, enemy.y) <= 80:
                enemy.stats['hitpoints'] -= damageCalculator(app.charStats[app.currChar], app.equippedWeapon)
                if enemy.stats['hitpoints'] <= 0:
                    destroyed.append(enemy)
        if app.mapRow == app.mapCol == 0:
            Adam = app.map.generatedMap[app.mapRow][app.mapCol].objectives[0]
            if distance(app.charX, app.charY, Adam.x, Adam.y) <= 80:
                Adam.stats['hitpoints'] -= damageCalculator(app.charStats[app.currChar], app.equippedWeapon)
                print(Adam.stats['hitpoints'])
                if Adam.stats['hitpoints'] <= 0:
                    app.won = True
                    return []
    else: pass
    return destroyed

