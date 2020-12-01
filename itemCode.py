from dataclasses import make_dataclass #Testing testing testing
import pandas as pd
import os, PIL.Image

def initItems(app):
    app.droppedItems = []
    app.junkItems = getJunkItems()
    app.weaponItems = getWeaponItems()
    app.invTest = []
    app.armorItems = getArmorItems()
    app.equippedWeapon = app.weaponItems['sword']
    getItemDrops(app)

def itemDrop(app):
    itemProbability = random.randint(0, 100)
    if itemProbability < (100 - app.uncommonProbability - app.rareProbability):
        item = random.choice(app.drops['junk'])
        app.uncommonProbability += 5
        app.rareProbability += 1
    elif itemProbability < (100 - app.rareProbability):
        item = random.choice(app.drops['uncommon'])
        app.uncommonProbability = 25
        app.rareProbability += 1
    else:
        item = random.choice(app.drops['rare'])
        app.uncommonProbability = 25
        app.rareProbability = 5
    return item

def getItemDrops(app):
    app.drops = {'junk': list(app.junkItems.values()), 'uncommon': [], 'rare': []}
    app.rareProbability = 5
    app.uncommonProbability = 25
    for item in app.weaponItems.values():
        if item.rarity == 1:
            app.drops['uncommon'].append(item)
        elif item.rarity == 2:
            app.drops['rare'].append(item)
    for item in app.armorItems.values():
        if item.rarity == 1:
            app.drops['uncommon'].append(item)
        elif item.rarity == 2:
            app.drops['rare'].append(item)


weaponItem = make_dataclass('weaponItem', ['name', 'strength', 'damageType', 'durability',
                                         'special', 'rarity', 'value', 'amount','imageSource',
                                        'enchantment'])
junkItem = make_dataclass('junkItem', ['name', 'value', 'amount', 'imageSource'])
armorItem = make_dataclass('armorItem', ['name', 'type', 'value', 'amount', 'protectionVal', 'rarity',
                                         'imageSource', 'enchantment', 'special'])

def getWeaponItems():
    factor = 10
    weapons = dict()
    weaponDf = pd.read_csv('items/weapons/weaponStats.csv', index_col = 'weapon')
    for i, row in weaponDf.iterrows():
        index = i
        strength = row['strength']
        for attackType in ['crushing', 'slashing', 'magic', 
                            'piercing']:
            if row[attackType] == 1:
                damageType = attackType
                break
        durability, special, rarity, value = row['durability'], row['special'], row['rarity'], row['value']
        fileName = index + '.png'
        if os.path.exists('items/weapons/weaponImages/' + fileName):
            pathName = 'items/weapons/weaponImages/' + fileName
            image = PIL.Image.open(pathName)
            width, height = image.size
            resizedImage = image.resize((width // factor, height // factor))
        else:
            resizedImage = None
            print(index + ' is not here!')
        newWeapon = weaponItem(name = index, strength = strength, damageType = damageType,
                                durability = durability, special = special,
                                rarity = rarity, value = value, amount = 0,
                                imageSource = resizedImage, enchantment = None)
        weapons[index] = newWeapon
    return weapons

def getJunkItems():
    factor = 10
    junk = dict()
    junkDf = pd.read_csv('items/junk/junkStats.csv', index_col = 'item')
    for i, row in junkDf.iterrows():
        index = i
        value = row['value']
        fileName = 'items/junk/junkImages/' + index + '.png'
        if os.path.exists(fileName):
            image = PIL.Image.open(fileName)
            width, height = image.size
            resizedImage = image.resize((width // factor, height // factor))
        else:
            resizedImage = None
            print(index + ' is not here!')
        newItem = junkItem(name = index, value = value, amount = 0, 
                            imageSource = resizedImage)
        junk[index] = newItem
    return junk

def getArmorItems():
    factor = 10
    armor = dict()
    armorDf = pd.read_csv('items/armor/armorStats.csv', index_col = 'armor')
    for i, row in armorDf.iterrows():
        index = i
        value = row['value']
        armorType = row['type']
        protection = row['protection']
        rarity = row['rarity']
        special = row['special']

        fileName = 'items/armor/armorImages/' + index + '.png'
        if os.path.exists(fileName):
            image = PIL.Image.open(fileName)
            width, height = image.size
            resizedImage = image.resize((width // factor, height // factor))
        else:
            resizedImage = None
            print(index + 'is not here!')
        newItem = armorItem(name = index, value = value, amount = 0, 
                            type = armorType, protectionVal = protection, 
                            rarity = rarity, special = special, enchantment = None,
                            imageSource = resizedImage)
        armor[index] = newItem
    return armor


### Images from
# https://www.pinclipart.com/pins/staff/
# http://clipart-library.com/free/sword-clipart-transparent.html
# https://www.pinclipart.com/pindetail/ihmoRTi_axe-clipart-two-handed-cartoon-mace-png-download/
# https://www.pinclipart.com/pindetail/hxJRR_image-free-download-archery-vector-word-clipart-bow/
# https://creazilla.com/nodes/26358-crossbow-clipart
# https://www.clipartmax.com/middle/m2K9A0d3d3i8i8G6_magic-wand-clipart/
# https://www.clipartmax.com/middle/m2i8G6d3d3d3i8K9_wood-clipart-wooden-log-log-clipart-png/
# http://clipart-library.com/free/rock-clipart-transparent.html
# https://www.clipartmax.com/middle/m2K9A0b1d3d3i8i8_green-grass-clip-art-lawn-green-grass-free-vector-graphic-illustration/


