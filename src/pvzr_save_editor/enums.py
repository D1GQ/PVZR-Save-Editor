"""Enum tables for PvZ Replanted save data (integer id -> name).

The editor auto-discovers every UPPER_CASE dict in this module whose keys are
all ints, so adding a new table here is enough to make it available by name
(e.g. in meta.POTTED_PLANT_ENUM_FIELDS).
"""

# Plant ids 0..53, in game order. Id 53 is the game's NumSeedTypes sentinel.
_SEED_NAMES = [
    "Peashooter",    "Sunflower",     "Cherrybomb",    "Wallnut",       "Potatomine",   "Snowpea",         # 0-5
    "Chomper",       "Repeater",      "Puffshroom",    "Sunshroom",     "Fumeshroom",   "Gravebuster",     # 6-11
    "Hypnoshroom",   "Scaredyshroom", "Iceshroom",     "Doomshroom",    "Lilypad",      "Squash",          # 12-17
    "Threepeater",   "Tanglekelp",    "Jalapeno",      "Spikeweed",     "Torchwood",    "Tallnut",         # 18-23
    "Seashroom",     "Plantern",      "Cactus",        "Blover",        "Splitpea",     "Starfruit",       # 24-29
    "Pumpkinshell",  "Magnetshroom",  "Cabbagepult",   "Flowerpot",     "Kernelpult",   "InstantCoffee",   # 30-35
    "Garlic",        "Umbrella",      "Marigold",      "Melonpult",     "Gatlingpea",   "Twinsunflower",   # 36-41
    "Gloomshroom",   "Cattail",       "Wintermelon",   "GoldMagnet",    "Spikerock",    "Cobcannon",       # 42-47
    "Imitater",      "ExplodeONut",   "GiantWallnut",  "Sprout",        "Leftpeater",   "NumSeedTypes",    # 48-53
]

# General seed type: -1 means "no seed".
SEED_TYPE = {-1: "None", **dict(enumerate(_SEED_NAMES))}

# Zen Garden seed type: same ids, but 0 is "None" and Peashooter is excluded.
ZEN_SEED_TYPE = {0: "None", **dict(enumerate(_SEED_NAMES[1:], start=1))}

ACHIEVEMENT_TYPE = dict(enumerate([
    "HomeSecurity",     "GoldSunflower",    "BetterOffDead",    "ChinaShop",        # 0-3
    "Spudow",           "Explodonator",     "Morticulturalist", "DontPeaInPool",    # 4-7
    "RollSomeHeads",    "Grounded",         "Zombologist",      "PennyPincher",     # 8-11
    "SunnyDays",        "PopcornParty",     "GoodMorning",      "NoFungusAmongUs",  # 12-15
    "BeatAllMiniGames", "Immortal",         "ToweringWisdom",   "MustacheMode",     # 16-19
    "HypnotizeDancer",  "FinalRest",        "LifeWellLived",    "CloudCover",       # 20-23
    "Pyromaniac",       "AliveAndPlanting", "WallNotAttack",    "ShootingStar",     # 24-27
    "SolInvictus",      "SproingSproing",   "IWin",             "Smashing",         # 28-31
    "LastMownStanding", "Enlightened",      "SecondLife",       "LifeHalfEmpty",    # 32-35
    "LifeHalfFull",     "MaxAchievements",                                          # 36-37
]))

STORE_ITEM = {-1: "None", **dict(enumerate([
    "PlantGatlingpea",  "PlantTwinsunflower", "PlantGloomshroom", "PlantCattail",       # 0-3
    "PlantWintermelon", "PlantGoldMagnet",    "PlantSpikerock",   "PlantCobcannon",     # 4-7
    "PlantImitater",    "BonusLawnMower",     "PottedMarigold1",  "PottedMarigold2",    # 8-11
    "PottedMarigold3",  "GoldWateringcan",    "Fertilizer",       "BugSpray",           # 12-15
    "Phonograph",       "GardeningGlove",     "MushroomGarden",   "WheelBarrow",        # 16-19
    "StinkyTheSnail",   "PacketUpgrade",      "PoolCleaner",      "RoofCleaner",        # 20-23
    "Rake",             "AquariumGarden",     "Chocolate",        "TreeOfWisdom",       # 24-27
    "TreeFood",         "Firstaid",           "Pvz",                                    # 28-30
]))}

GARDEN_TYPE = dict(enumerate(["Main", "Mushroom", "WheelBarrow", "Aquarium"]))

DRAW_VARIATION = dict(enumerate([
    "Normal", "Imitater",                                                   # 0-1
    "MarigoldWhite", "MarigoldMagenta", "MarigoldOrange", "MarigoldPink",   # 2-5
    "MarigoldLightBlue", "MarigoldRed", "MarigoldBlue", "MarigoldViolet",   # 6-9
    "MarigoldLavender", "MarigoldYellow", "MarigoldLightGreen",             # 10-12
    "ZenGarden", "ZenGardenWater", "SproutNoFlower",                        # 13-15
    "ImitaterLess", "Aquarium", "BigIdle",                                  # 16-18
]))

POTTED_PLANT_AGE = dict(enumerate(["Sprout", "Small", "Medium", "Full"]))

POTTED_PLANT_NEED = dict(enumerate(["None", "Water", "Fertilizer", "BugSpray", "Phonograph"]))
