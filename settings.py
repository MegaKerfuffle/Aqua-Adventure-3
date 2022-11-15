'''
Robert Brzostek
Date: 1/22/2020
Aqua Adventure 3
'''

# Import needed modules, functions, and settings
import pygame as pg, os, sys

# Init Pygame
pg.init()

# # # # THIS FILE IS FOR STORING VARIABLES/SETTINGS COMMON ACROSS FILES # # # # 

# # # COLOUR INIT # # #
global black
black = (0, 0, 0)
global black_transparent
black_transparent = (0, 0, 0, 150)
global white
white = (255, 255, 255)
global red
red = (255, 0, 0)
global darker_red
darker_red = (200, 0, 0)
global green
green = (0, 255, 0)
global darker_green
darker_green = (0, 200, 0)
global blue
blue = (0, 0, 255)
global darker_blue
darker_blue = (0, 0 , 200)
global space_gray
space_gray = (167, 173, 186)
global doorBrown
doorBrown = (182, 153, 110)
global floorBrown
floorBrown = (91, 68, 62)

# # # MISC GAME OPTIONS # # #

global fadingTextActive
fadingTextActive = False

global fadeActive
fadeActive = True

global projectileSpeed
projectileSpeed = 12

global npcSpeed
npcSpeed = 3

global bossSpeed
bossSpeed = 5

global npcList
npcList = []

global gameObjectList
gameObjectList = []

# # # PLAYER OPTIONS # # #
# Player speed 
global playerSpeed
playerSpeed = 4

# Player health
global playerHealth
playerHealth = 100

# Player action points
global playerActionPoints
playerActionPoints = 100

# Player maximum action points
global playerMaxAP
playerMaxAP = 100

# # PLAYER NEEDS SYSTEM # #
# Time (in milliseconds) to update hunger
global hungerIterator
hungerIterator = 30000

# Time (in milliseconds) to update thirst
global thirstIterator
thirstIterator = 20000

# Time (in milliseconds) to update health
global healthIterator
healthIterator = 5000

# Time (in milliseconds) for enemies to shoot
global enemyShootIterator
enemyShootIterator = 1000

# Time (in ms) for the boss to shoot
global bossShootIterator
bossShootIterator = 5000

# Time (in milliseconds) to subtract AP while using targetAwareness
global targetAwareIterator
targetAwareIterator = 1000

# Time (in milliseconds) to make NPCs speak
global npcSpeakIterator
npcSpeakIterator = 8000



# # PLAYER BODYPART SYSTEM # #
# Bodypart list
global bodyparts
bodyparts = []

# Populate bodypart list
'''
bodypart = ["name", stateTxt, effectActive]
name - the name of the bodypart
stateTxt - display state of the bodypart
effectActive - bool value indicating whether the limb's injury effect is active
'''
bodypart = ["Head", "Healthy", False]
bodyparts.append(bodypart)

bodypart = ["Torso", "Healthy", False]
bodyparts.append(bodypart)

bodypart = ["Left Arm", "Healthy", False]
bodyparts.append(bodypart)

bodypart = ["Right Arm", "Healthy", False]
bodyparts.append(bodypart)

bodypart = ["Left Leg", "Healthy", False]
bodyparts.append(bodypart)

bodypart = ["Right Leg", "Healthy", False]
bodyparts.append(bodypart)

# # PLAYER SKILLS SYSTEM # #
global playerSkills
playerSkills = []

# Populate playerSkills
'''
skill = ["name","description",level,lvlUpPts]
name - name of skill
description - description of skill
level - skill level (0 to 0.5)
lvlUpPts - points gained for using skill; used to level up
'''
skill = ["Lockpick", "Ability to open locked things", 0.1, 0]
playerSkills.append(skill)

skill = ["Medical", "Used to heal injuries", 0.1, 0]
playerSkills.append(skill)

skill = ["Shooting", "Affects shooting accuracy", 0.1, 0]
playerSkills.append(skill)

skill = ["Evasion", "Ability to dodge enemy attacks", 0.1, 0]
playerSkills.append(skill)

skill = ["Strength", "Affects carry weight", 0.1, 0]
playerSkills.append(skill)

skill = ["Endurance", "Affects action points & chems", 0.1, 0]
playerSkills.append(skill)

# StatusUI active screen
global statUIactive
statUIactive = [True, False, False, False, False, False]

# # PLAYER INVENTORY SYSTEM # # 
# List containing inventory items
global playerInventory
playerInventory = [
    ["Pistol", "A 10mm hand gun", 5, 50, True, True],
    ["10mm mag", "A 10mm magazine", 1, 30, False, True],
    ["Clean Water", "Restores thirst", 1, 25, True, True],
    ["Military MRE", "Restores hunger", 2, 50, True, True],
    ["Bobby Pin", "Required for lockpicking", 0.1, 1, False, True]
]

# List containing all in-game items
global item_list
item_list = []

# Populate item_list
'''
item = ["name", "description", weight, value, useable]
name - name of item
description - brief description of item's purpose (for in game)
weight - weight of the item (how much inventory space it will take up)
value - in game value of item (in scrap metal)
usable - bool value to indicate whether or not item can be used in INV
dropable - bool value to indicate whether the item can be dropped
'''
# Medkit (tier 1 medical) [0]
item = ["Med Kit", "Treats injuries", 3, 50, True, True]
item_list.append(item)

# Antibiotics (tier 1 medical) [1]
item = ["Antibiotics", "Treats infections", 1, 75, True, True]
item_list.append(item)

# Bandage (tier 2 medical) [2]
item = ["Bandage", "Restores health", 1, 25, True, True]
item_list.append(item)

# Painkillers (tier 3 medical) [3] 
item = ["Painkillers", "Removes pain blindness", 0.5, 20, True, True]
item_list.append(item)

# Purified water (tier 1 water) [4] 
item = ["Clean Water", "Restores thirst", 1, 25, True, True]
item_list.append(item)

# Irradiated water (tier 2 water) [5]
item = ["Dirty Water", "Restores thirst ", 1, 10, True, True]
item_list.append(item)

# Can of Spam (tier 1 food) [6]
item = ["Can of Spam", "Restores hunger", 1, 15, True, True]
item_list.append(item)

# Military MRE (tier 1 food) [7]
item = ["Military MRE", "Restores hunger", 2, 50, True, True]
item_list.append(item)

# Cooked Meat (tier 2 food) [8]
item = ["Cooked Meat", "Restores hunger", 2, 15, True, True]
item_list.append(item)

# Candy Bar (tier 2 food) [9]
item = ["Candy Bar", "Restores hunger", 0.5, 5, True, True]
item_list.append(item)

# Raw Meat (tier 3 food) [10]
item = ["Raw Meat", "Restores hunger", 2, 5, True, True]
item_list.append(item)

# Nitro (chem - +AP) [11]
item = ["Nitro", "Increases AP refresh", 1, 50, True, True]
item_list.append(item)

# Grittle (chem - +AP) [12]
item = ["Grittle", "Increases maximum AP", 1, 50, True, True]
item_list.append(item)

# Bulkup (chem - +carryweight) [13]
item = ["Bulkup", "Increases maximum weight", 1, 50, True, True]
item_list.append(item)

# Speed (chem - +max speed) [14]
item = ["Speed", "Increases max speed", 1, 50, True, True]
item_list.append(item)

# Bobby pin (utility) [15]
item = ["Bobby Pin", "Required for lockpicking", 0.1, 1, False, True]
item_list.append(item)

# Crowbar (utility) [16]
item = ["Crowbar", "Used to break locks", 4, 50, False, True]
item_list.append(item)

# 10mm magazine (ammo) [17]
item = ["10mm mag", "A 10mm magazine", 1, 30, False, True]
item_list.append(item)

# 5.56mm magazine (ammo) [18]
item = ["5.56mm mag", "A 5.56mm magazine", 1, 50, False, True]
item_list.append(item)

# .308 cal magazine (ammo) [19]
item = [".308cal mag", "A .308 magazine", 1, 70, False, True]
item_list.append(item)

# 10mm hand gun (weapon) [20]
item = ["Pistol", "A 10mm hand gun", 5, 50, True, True]
item_list.append(item)

# 5.56mm rifle [21]
item = ["Carbine", "A 5.56mm rifle", 7, 75, True, True]
item_list.append(item)

# .308 hunting rifle [22]
item = ["Rifle", "A .308cal rifle", 10, 100, True, True]
item_list.append(item)

# # PLAYER LOCATION SYSTEM # #
# Player location list
global location_list
location_list = [] 

# Populate location_list
'''
segment = ["description", a, b, c, d]
description - text to display upon arriving in a map segment
a - segment north of current 
b - segment east of current
c - segment south of current
d - segment west of current
'''
# Segment 0 (default)
segment = ["Old Shelter", 1, 3, 2, None]
location_list.append(segment)

# Segment 1 (north of default)
segment = ["North Coast", None, 4, 0, None]
location_list.append(segment)

# Segment 2 (south of default)
segment = ["South Coast", 0, 5, None, None]
location_list.append(segment)

# Segment 3 (east of default)
segment = ["Mid Desert", 4, 7, 5, 0]
location_list.append(segment)

# Segment 4 (east of S1)
segment = ["Old Truckstop", None, 6, 3, 1]
location_list.append(segment)

# Segment 5 (east of S2)
segment = ["Old Clinic", 3, 8, None, 2]
location_list.append(segment)

# Segment 6 (east of S4)
segment = ["East Wasteland", None, None, 7, 4]
location_list.append(segment)

# Segment 7 (east of S3)
segment = ["Army Compound", 6, 9, 8, 3]
location_list.append(segment)

# Segment 8 (east of S5)
segment = ["Power Plant", 7, None, None, 5]
location_list.append(segment)

# Segment 9 (east of S7)
segment = ["The Mainframe", None, None, None, 7]
location_list.append(segment)

# # # OTHER # # #

# StageSys options (init)
global stage
stage = 0

# Button font
global buttonFont
buttonFont = pg.font.SysFont("lucidaconsole",20,False,False)

# Allow python to pull files
global addressprefix
addressprefix = os.path.dirname(__file__)

global tree1
tree1 = pg.image.load(addressprefix + "\\misc\\tree1.png")

global tree2
tree2 = pg.image.load(addressprefix + "\\misc\\tree2.png")



