from itemCode import *

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