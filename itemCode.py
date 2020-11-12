from dataclasses import make_dataclass #Testing testing testing
import pandas as pd
import os

weaponItem = make_dataclass('weaponItem', ['name', 'strength', 'damageType', 'durability',
                                         'special', 'rarity', 'value', 'amount','imageSource',
                                        'enchantment'])
junkItem = make_dataclass('junkItem', ['name', 'value', 'amount', 'imageSource'])
armorItem = make_dataclass('armorItem', ['name', 'type', 'value', 'amount', 'protectionVal', 'rarity',
                                         'imageSource', 'enchantment', 'special'])

def getWeaponItems():
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
        else:
            pathName = None
            print(index + ' is not here!')
        newWeapon = weaponItem(name = index, strength = strength, damageType = damageType,
                                durability = durability, special = special,
                                rarity = rarity, value = value, amount = 0,
                                imageSource = pathName, enchantment = None)
        weapons[index] = newWeapon
    return weapons

def getJunkItems():
    junk = dict()
    junkDf = pd.read_csv('items/junk/junkStats.csv', index_col = 'item')
    for i, row in junkDf.iterrows():
        index = i
        value = row['value']
        fileName = 'items/junk/junkImages/' + index + '.png'
        if not os.path.exists(fileName):
            fileName = None
            print(index + ' is not here!')
        newItem = junkItem(name = index, value = value, amount = 0, 
                            imageSource = fileName)
        junk[index] = newItem
    return junk

def getArmorItems():
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
        if not os.path.exists(fileName):
            fileName = None
            print(index + 'is not here!')
        newItem = armorItem(name = index, value = value, amount = 0, 
                            type = armorType, protectionVal = protection, 
                            rarity = rarity, special = special, enchantment = None,
                            imageSource = fileName)
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


