"""UI metadata for the PvZ Replanted save editor: labels, groups, enum bindings
and level/minigame name tables. Everything here is optional; the editor falls
back to raw field names when an entry is missing.
"""

# --------------------------------------------------------------------------
# Field labels (UserProfile + PottedPlant)
# --------------------------------------------------------------------------

FIELD_LABELS = {
    # ---- UserProfile ----
    "mName":                          "Name",
    "mGuid":                          "GUID",
    "mUseSeq":                        "Use sequence",
    "mId":                            "Profile ID",
    "mLevel":                         "Level",
    "mRipLevel":                      "RIP level",
    "mCoins":                         "Coins",
    "mFinishedAdventure":             "Finished adventure",
    "mFinishedRipAdventure":          "Finished RIP adventure",
    "mPlayTimeActivePlayer":          "Play time (active)",
    "mPlayTimeInactivePlayer":        "Play time (inactive)",
    "mHasUsedCheatKeys":              "Has used cheat keys",
    "mHasWokenStinky":                "Has woken Stinky",
    "mDidntPurchasePacketUpgrade":    "Didn't purchase packet upgrade",
    "mLastStinkyChocolateTime":       "Last Stinky chocolate time",
    "mStinkyPosX":                    "Stinky X",
    "mStinkyPosY":                    "Stinky Y",
    "mHasUnlockedMinigames":          "Unlocked minigames",
    "mHasUnlockedPuzzleMode":         "Unlocked puzzle mode",
    "mHasNewMiniGame":                "Has new minigame",
    "mHasNewVasebreaker":             "Has new vasebreaker",
    "mHasNewIZombie":                 "Has new I, Zombie",
    "mHasNewSurvival":                "Has new survival",
    "mHasUnlockedSurvivalMode":       "Unlocked survival mode",
    "mNeedsMessageOnGameSelector":    "Needs game-selector message",
    "mNeedsMagicTacoReward":          "Needs magic taco reward",
    "mHasSeenStinky":                 "Has seen Stinky",
    "mHasSeenUpsell":                 "Has seen upsell",
    "mNumPottedPlants":               "Potted plant count",
    "mShownZombatarDesktopMessage":   "Shown Zombatar desktop message",
    "mAcceptedZombatarULA":           "Accepted Zombatar EULA",
    "mRipModeActive":                 "RIP mode active",
    "mRipUsedLawnMower":              "RIP used lawnmower",
    "mRipHasSeenHelp":                "RIP has seen help",
    "mPreOrderContentActive":         "Pre-order content active",
    "mPlatformContentActive":         "Platform content active",
    "mRetroContentActive":            "Retro content active",
    "mDanceModeActive":               "Dance mode active",
    "mMustacheModeActive":            "Mustache mode active",
    "mFutureModeActive":              "Future mode active",
    "mTrickedOutModeActive":          "Tricked-out mode active",
    "mDaisesModeActive":              "Daises mode active",
    "mPinataModeActive":              "Piñata mode active",
    "mSukhbirModeActive":             "Sukhbir mode active",
    "mHasSeenMultiplayerUnlocked":    "Seen multiplayer unlock",
    "mHasSeenCloudyDayUnlocked":      "Seen Cloudy-Day unlock",
    "mHasSeenLimboUnlocked":          "Seen Limbo unlock",
    "mHasSeenRIPUnlocked":            "Seen RIP unlock",
    "mHarderEnabled":                 "Harder enabled",
    "mZenGardenTutorialCompleted":    "Zen Garden tutorial done",
    "mBShownAchievements":            "Achievements (shown)",
    "mBEarnedAchievements":           "Achievements (earned)",
    "mChallengeRecords":              "Challenge records",
    "mPurchases":                     "Purchases",
    "mPlaceHolderPlayerStats":        "Placeholder stats",
    "mMiniGamesCompleted":            "Minigames completed",
    "mCloudyDayLevelsCompleted":      "Cloudy-Day levels completed",
    "mCoopLevelsCompleted":           "Co-op levels completed",
    "mCollectedZenGardenPlants":      "Collected Zen-Garden plants",
    "mCoopChallengeRecords":          "Co-op challenge records",
    "mCloudyDayRecords":              "Cloudy-Day records",
    "StinkyWakeUpTime":               "Stinky wake-up time",
    # ---- PottedPlant ----
    "mSeedType":                      "Plant type",
    "mWhichZenGarden":                "Garden",
    "mX":                             "X",
    "mY":                             "Y",
    "mFacing":                        "Facing",
    "mLastWateredTime":               "Last watered",
    "mDrawVariation":                 "Draw variation",
    "mPlantAge":                      "Age",
    "mTimesFed":                      "Times fed",
    "mFeedingsPerGrow":               "Feedings per grow",
    "mPlantNeed":                     "Need",
    "mLastNeedFulfilledTime":         "Last need fulfilled",
    "mLastFertilizedTime":            "Last fertilized",
    "mLastChocolateTime":             "Last chocolate",
    "mFutureAttribute":               "Future attribute",
}

# --------------------------------------------------------------------------
# Main-tab layout
# --------------------------------------------------------------------------

# Profile fields edited in a dedicated tab (Store / Achievements / Zen Garden)
# and therefore hidden from the main field editor.
FIELDS_OWNED_BY_OTHER_TABS = {
    "mPurchases",
    "mBShownAchievements",
    "mBEarnedAchievements",
    "mNumPottedPlants",
}

# (group title, [field names]) in display order. Profile fields that appear in
# no group (and aren't owned by another tab) are shown under "Other".
FIELD_GROUPS = [
    ("Identity", ["mName", "mGuid", "mId", "mUseSeq"]),
    ("Progress", [
        "mLevel", "mRipLevel",
        "mFinishedAdventure", "mFinishedRipAdventure",
        "mRipModeActive", "mRipUsedLawnMower",
        "mHarderEnabled",
        "mMiniGamesCompleted", "mCloudyDayLevelsCompleted",
        "mCoopLevelsCompleted", "mCollectedZenGardenPlants",
        "mChallengeRecords", "mCoopChallengeRecords",
        "mCloudyDayRecords", "mPlaceHolderPlayerStats",
        "mPlayTimeActivePlayer", "mPlayTimeInactivePlayer",
    ]),
    ("Economy", ["mCoins"]),
    ("Unlocks & Notifications", [
        "mHasUnlockedMinigames", "mHasUnlockedPuzzleMode",
        "mHasUnlockedSurvivalMode",
        "mHasNewMiniGame", "mHasNewVasebreaker",
        "mHasNewIZombie", "mHasNewSurvival",
        "mNeedsMessageOnGameSelector", "mNeedsMagicTacoReward",
        "mHasSeenStinky", "mHasSeenUpsell",
        "mHasSeenMultiplayerUnlocked",
        "mHasSeenCloudyDayUnlocked", "mHasSeenLimboUnlocked",
        "mHasSeenRIPUnlocked", "mRipHasSeenHelp",
    ]),
    ("Content", [
        "mPreOrderContentActive", "mPlatformContentActive",
        "mRetroContentActive", "mDanceModeActive",
        "mMustacheModeActive", "mFutureModeActive",
        "mTrickedOutModeActive", "mDaisesModeActive",
        "mPinataModeActive", "mSukhbirModeActive",
    ]),
    ("Zen Garden", [
        "mZenGardenTutorialCompleted",
        "mHasWokenStinky", "mLastStinkyChocolateTime",
        "mStinkyPosX", "mStinkyPosY", "StinkyWakeUpTime",
    ]),
    ("Miscellaneous", [
        "mHasUsedCheatKeys", "mDidntPurchasePacketUpgrade",
        "mShownZombatarDesktopMessage", "mAcceptedZombatarULA",
    ]),
]

# --------------------------------------------------------------------------
# Enum bindings (field name -> enum table name in enums / this module)
# --------------------------------------------------------------------------

PROFILE_ENUM_FIELDS = {}

POTTED_PLANT_ENUM_FIELDS = {
    "mSeedType":       "ZEN_SEED_TYPE",
    "mWhichZenGarden": "GARDEN_TYPE",
    "mDrawVariation":  "DRAW_VARIATION",
    "mPlantAge":       "POTTED_PLANT_AGE",
    "mPlantNeed":      "POTTED_PLANT_NEED",
}

# Array fields: each index is labelled using the named table.
ARRAY_FIELD_ENUMS = {
    "mMiniGamesCompleted":       "MINIGAMES",
    "mCloudyDayLevelsCompleted": "CLOUDY_DAY_LEVELS",
    "mCoopLevelsCompleted":      "COOP_LEVELS",
    "mChallengeRecords":         "CHALLENGE_RECORDS",
    "mCoopChallengeRecords":     "COOP_LEVELS",
    "mCloudyDayRecords":         "CLOUDY_DAY_LEVELS",
    "mCollectedZenGardenPlants": "ZEN_SEED_TYPE",
}

ACHIEVEMENT_BOOL_FIELDS = ["mBShownAchievements", "mBEarnedAchievements"]

STORE_ARRAY_FIELDS = ["mPurchases"]

# Store items shown as an on/off checkbox instead of a quantity spinbox.
STORE_TOGGLE_ITEMS = {
    0, 1, 2, 3, 4, 5, 6, 7, 8,      # plant unlocks
    9,                               # BonusLawnMower
    13,                              # GoldWateringcan
    16,                              # Phonograph
    17,                              # GardeningGlove
    18,                              # MushroomGarden
    19,                              # WheelBarrow
    20,                              # StinkyTheSnail
    22,                              # PoolCleaner
    23,                              # RoofCleaner
    25,                              # AquariumGarden
    27,                              # TreeOfWisdom
}

# --------------------------------------------------------------------------
# Level / minigame name tables (index -> display name)
# --------------------------------------------------------------------------

# 5 worlds x 10 levels: "Level 1-1" .. "Level 5-10".
ADVENTURE_LEVELS = {i: f"Level {i // 10 + 1}-{i % 10 + 1}" for i in range(50)}

MINIGAMES = dict(enumerate([
    "ZomBotany", "Wall-nut Bowling", "Slot Machine", "It's Raining Seeds",          # 0-3
    "Beghouled", "Invisi-ghoul", "Seeing Stars", "Zombiquarium",                    # 4-7
    "Beghouled Twist", "Big Trouble Little Zombie", "Portal Combat",                # 8-10
    "Column Like You See 'Em", "Bobsled Bonanza", "Zombie Nimble Zombie Quick",     # 11-13
    "Whack a Zombie", "Last Stand", "ZomBotany 2", "Wall-nut Bowling 2",            # 14-17
    "Pogo Party", "Dr. Zomboss's Revenge", "Art Challenge Wall-nut", "Sunny Day",   # 18-21
    "Unsodded", "Big Time", "Art Challenge Sunflower", "Air Raid",                  # 22-25
    "Ice Level", "Zen Garden", "High Gravity", "Grave Danger",                      # 26-29
    "Can You Dig It?", "Dark Stormy Night", "Bungee Blitz", "Squirrel",             # 30-33
]))

# Ordered as three tiers of five areas: normal, hard, endless.
_SURVIVAL_AREAS = ["Day", "Night", "Pool", "Fog", "Roof"]
_SURVIVAL_TIERS = ["", " (Hard)", " (Endless)"]
SURVIVAL_LEVELS = {
    tier * len(_SURVIVAL_AREAS) + area_idx: f"Survival: {area}{suffix}"
    for tier, suffix in enumerate(_SURVIVAL_TIERS)
    for area_idx, area in enumerate(_SURVIVAL_AREAS)
}

PUZZLE_LEVELS = dict(enumerate([
    "Vasebreaker", "To the Left", "Third Vase", "Chain Reaction",                   # 0-3
    "M is for Metal", "Scary Potter", "Hokey Pokey", "Another Chain Reaction",      # 4-7
    "Ace of Vase", "Vasebreaker Endless",                                           # 8-9
    "I, Zombie", "I, Zombie Too", "Can You Dig It?", "Totally Nuts",                # 10-13
    "Dead Zeppelin", "Me Smash!", "ZomBoogie", "Three Hit Wonder",                  # 14-17
    "All your brainz r belong to us", "I, Zombie Endless",                          # 18-19
]))

# 0-7: four areas, each as a normal/hard pair; 8-9: specials; 10-14: the
# endless survival levels (shared with SURVIVAL_LEVELS).
_COOP_AREAS = ["Day", "Night", "Pool", "Roof"]
COOP_LEVELS = {
    **{
        area_idx * 2 + hard: f"Co-Op {area}" + (" (Hard)" if hard else "")
        for area_idx, area in enumerate(_COOP_AREAS)
        for hard in (0, 1)
    },
    8: "Wall-nut Bowling",
    9: "Dr. Zomboss's Revenge",
    **{i: SURVIVAL_LEVELS[i] for i in range(10, 15)},
}

CLOUDY_DAY_LEVELS = {
    **{i: f"Cloudy Day Level {i + 1}" for i in range(12)},
    12: "Cloudy Day (Endless)",
}

CHALLENGE_RECORDS = {}
