"""Binary (de)serialisation of UserProfile / PottedPlant."""

import struct
from datetime import datetime

from .constants import DEFAULT_PROFILE_VERSION, HEADER_SIZE


class Reader:
    __slots__ = ("d", "p")

    def __init__(self, data: bytes):
        self.d = data
        self.p = 0

    def _take(self, n):
        if self.p + n > len(self.d):
            raise EOFError(f"EOF at {self.p}, need {n}, have {len(self.d) - self.p}")
        b = self.d[self.p:self.p + n]
        self.p += n
        return b

    def _unpack(self, fmt):
        return struct.unpack(fmt, self._take(struct.calcsize(fmt)))[0]

    def _length(self, what):
        n = self.i32()
        if n < 0:
            raise ValueError(f"negative {what} length {n} at {self.p - 4}")
        return n

    def i32(self): return self._unpack("<i")
    def i64(self): return self._unpack("<q")
    def u64(self): return self._unpack("<Q")
    def f32(self): return self._unpack("<f")
    def b(self):   return self._take(1)[0] != 0

    def string(self):
        n = self._length("string")
        return self._take(n).decode("utf-8", errors="strict") if n else None

    def i32arr(self):
        n = self._length("int[]")
        return list(struct.unpack(f"<{n}i", self._take(4 * n)))

    def boolarr(self):
        n = self._length("bool[]")
        return [b != 0 for b in self._take(n)]

    def remaining(self):
        return len(self.d) - self.p


class Writer:
    __slots__ = ("buf",)

    def __init__(self):
        self.buf = bytearray()

    def _pack(self, fmt, v):
        self.buf += struct.pack(fmt, v)

    def i32(self, v): self._pack("<i", int(v))
    def i64(self, v): self._pack("<q", int(v))
    def u64(self, v): self._pack("<Q", int(v))
    def f32(self, v): self._pack("<f", float(v))
    def b(self, v):   self.buf.append(1 if v else 0)

    def string(self, s):
        if s is None:
            self.i32(0)
            return
        data = s.encode("utf-8")
        self.i32(len(data))
        self.buf += data

    def i32arr(self, arr):
        self.i32(len(arr))
        self.buf += struct.pack(f"<{len(arr)}i", *[int(x) for x in arr])

    def boolarr(self, arr):
        self.i32(len(arr))
        self.buf += bytes(1 if x else 0 for x in arr)

    def getvalue(self):
        return bytes(self.buf)


# Field kind -> (read(reader), write(writer, value)).
# "i64time" is an i64 shown as a date/time in the UI.
# "booltoi32" is a bool stored as a 4-byte int (normalised to 0/1 on read).
CODECS = {
    "i32":       (Reader.i32,    Writer.i32),
    "i64":       (Reader.i64,    Writer.i64),
    "i64time":   (Reader.i64,    Writer.i64),
    "u64":       (Reader.u64,    Writer.u64),
    "f32":       (Reader.f32,    Writer.f32),
    "bool":      (Reader.b,      Writer.b),
    "str":       (Reader.string, Writer.string),
    "i32arr":    (Reader.i32arr, Writer.i32arr),
    "boolarr":   (Reader.boolarr, Writer.boolarr),
    "booltoi32": (lambda r: 1 if r.i32() else 0,
                  lambda w, v: w.i32(1 if v else 0)),
}


def default_for_kind(kind):
    if kind == "str":
        return None
    if kind in ("i32arr", "boolarr"):
        return []
    if kind == "bool":
        return False
    return 0


def _read_fields(obj, reader, fields):
    for name, kind in fields:
        setattr(obj, name, CODECS[kind][0](reader))


def _write_fields(obj, writer, fields):
    for name, kind in fields:
        CODECS[kind][1](writer, getattr(obj, name))


POTTED_PLANT_FIELDS = [
    ("mSeedType",               "i32"),
    ("mWhichZenGarden",         "i32"),
    ("mX",                      "i32"),
    ("mY",                      "i32"),
    ("mFacing",                 "i32"),
    ("mLastWateredTime",        "i64time"),
    ("mDrawVariation",          "i32"),
    ("mPlantAge",               "i32"),
    ("mTimesFed",               "i32"),
    ("mFeedingsPerGrow",        "i32"),
    ("mPlantNeed",              "i32"),
    ("mLastNeedFulfilledTime",  "i64time"),
    ("mLastFertilizedTime",     "i64time"),
    ("mLastChocolateTime",      "i64time"),
    ("mFutureAttribute",        "i32arr"),
]


class PottedPlant:
    def __init__(self):
        for name, kind in POTTED_PLANT_FIELDS:
            setattr(self, name, default_for_kind(kind))
        self.mFutureAttribute = [0]  # empty slots in real saves carry [0]

    @classmethod
    def fresh(cls):
        """A newly added plant. Needs non-zero fields so it isn't read back
        as an empty slot."""
        p = cls()
        p.mPlantAge = 1
        p.mFeedingsPerGrow = 3
        return p

    def is_blank(self):
        for name, kind in POTTED_PLANT_FIELDS:
            v = getattr(self, name)
            if name == "mFutureAttribute":
                if any(v):
                    return False
            elif v:
                return False
        return True

    @classmethod
    def deserialize(cls, r: Reader):
        p = cls()
        _read_fields(p, r, POTTED_PLANT_FIELDS)
        return p

    def serialize(self, w: Writer):
        _write_fields(self, w, POTTED_PLANT_FIELDS)


# Serialized in file order. The potted-plant list sits in the middle of the
# profile, right after mCollectedZenGardenPlants (see UserProfile below).
PROFILE_FIELDS = [
    ("mName",                          "str"),
    ("mGuid",                          "str"),
    ("mUseSeq",                        "u64"),
    ("mId",                            "i32"),
    ("mLevel",                         "i32"),
    ("mRipLevel",                      "i32"),
    ("mCoins",                         "i32"),
    ("mFinishedAdventure",             "booltoi32"),
    ("mFinishedRipAdventure",          "booltoi32"),
    ("mPlayTimeActivePlayer",          "i32"),
    ("mPlayTimeInactivePlayer",        "i32"),
    ("mHasUsedCheatKeys",              "booltoi32"),
    ("mHasWokenStinky",                "booltoi32"),
    ("mDidntPurchasePacketUpgrade",    "booltoi32"),
    ("mLastStinkyChocolateTime",       "i64time"),
    ("mStinkyPosX",                    "i32"),
    ("mStinkyPosY",                    "i32"),
    ("mHasUnlockedMinigames",          "booltoi32"),
    ("mHasUnlockedPuzzleMode",         "booltoi32"),
    ("mHasNewMiniGame",                "booltoi32"),
    ("mHasNewVasebreaker",             "booltoi32"),
    ("mHasNewIZombie",                 "booltoi32"),
    ("mHasNewSurvival",                "booltoi32"),
    ("mHasUnlockedSurvivalMode",       "booltoi32"),
    ("mNeedsMessageOnGameSelector",    "booltoi32"),
    ("mNeedsMagicTacoReward",          "booltoi32"),
    ("mHasSeenStinky",                 "booltoi32"),
    ("mHasSeenUpsell",                 "booltoi32"),
    ("mNumPottedPlants",               "i32"),
    ("mShownZombatarDesktopMessage",   "bool"),
    ("mAcceptedZombatarULA",           "bool"),
    ("mRipModeActive",                 "bool"),
    ("mRipUsedLawnMower",              "bool"),
    ("mRipHasSeenHelp",                "bool"),
    ("mPreOrderContentActive",         "bool"),
    ("mPlatformContentActive",         "bool"),
    ("mRetroContentActive",            "bool"),
    ("mDanceModeActive",               "bool"),
    ("mMustacheModeActive",            "bool"),
    ("mFutureModeActive",              "bool"),
    ("mTrickedOutModeActive",          "bool"),
    ("mDaisesModeActive",              "bool"),
    ("mPinataModeActive",              "bool"),
    ("mSukhbirModeActive",             "bool"),
    ("mHasSeenMultiplayerUnlocked",    "bool"),
    ("mHasSeenCloudyDayUnlocked",      "bool"),
    ("mHasSeenLimboUnlocked",          "bool"),
    ("mHasSeenRIPUnlocked",            "bool"),
    ("mHarderEnabled",                 "bool"),
    ("mZenGardenTutorialCompleted",    "bool"),
    ("mBShownAchievements",            "boolarr"),
    ("mBEarnedAchievements",           "boolarr"),
    ("mChallengeRecords",              "i32arr"),
    ("mPurchases",                     "i32arr"),
    ("mPlaceHolderPlayerStats",        "i32arr"),
    ("mMiniGamesCompleted",            "boolarr"),
    ("mCloudyDayLevelsCompleted",      "boolarr"),
    ("mCoopLevelsCompleted",           "boolarr"),
    ("mCollectedZenGardenPlants",      "boolarr"),
    ("mCoopChallengeRecords",          "i32arr"),
    ("mCloudyDayRecords",              "i32arr"),
]

PROFILE_KIND = dict(PROFILE_FIELDS)

_PLANTS_SPLIT = [n for n, _ in PROFILE_FIELDS].index("mCollectedZenGardenPlants") + 1
_FIELDS_BEFORE_PLANTS = PROFILE_FIELDS[:_PLANTS_SPLIT]
_FIELDS_AFTER_PLANTS = PROFILE_FIELDS[_PLANTS_SPLIT:]


class UserProfile:
    def __init__(self):
        for name, kind in PROFILE_FIELDS:
            setattr(self, name, default_for_kind(kind))
        self.mPottedPlant = []

    @classmethod
    def deserialize(cls, data: bytes, version: int = DEFAULT_PROFILE_VERSION):
        r = Reader(data)
        p = cls()
        _read_fields(p, r, _FIELDS_BEFORE_PLANTS)
        plant_count = r.i32()
        if plant_count < 0:
            raise ValueError(f"negative plant count {plant_count}")
        p.mPottedPlant = [PottedPlant.deserialize(r) for _ in range(plant_count)]
        _read_fields(p, r, _FIELDS_AFTER_PLANTS)
        if r.remaining() != 0:
            raise ValueError(
                f"Deserialization consumed {r.p} of {len(data)} bytes "
                f"({r.remaining()} leftover)")
        p._version = version
        p._plant_slots = plant_count   # the game stores a fixed-size array
        return p

    def serialize(self) -> bytes:
        w = Writer()
        # Fixed number of slots; used plants first, blanks after. The separate
        # mNumPottedPlants field counts used plants, not slots.
        slots = getattr(self, "_plant_slots", len(self.mPottedPlant))
        used = [pl for pl in self.mPottedPlant if not pl.is_blank()]
        if len(used) > slots:
            raise ValueError(f"{len(used)} potted plants but the save has "
                             f"only {slots} slots")
        plants = used + [PottedPlant() for _ in range(slots - len(used))]
        self.mNumPottedPlants = len(used)
        _write_fields(self, w, _FIELDS_BEFORE_PLANTS)
        w.i32(len(plants))
        for plant in plants:
            plant.serialize(w)
        _write_fields(self, w, _FIELDS_AFTER_PLANTS)
        return w.getvalue()
