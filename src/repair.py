"""Repair known corruption patterns in a loaded UserProfile.

Fixes the damage older versions of this editor could do:
  * achievement arrays padded past their real length (the enum's
    "MaxAchievements" entry is a count sentinel, not an achievement)
  * the potted-plant array grown past its fixed slot count
  * mNumPottedPlants set to the slot count instead of the used-plant count
"""

from .binary import PottedPlant
from .enums import ACHIEVEMENT_TYPE

MAX_POTTED_PLANTS = 200
ACHIEVEMENT_COUNT = next(
    (k for k, v in ACHIEVEMENT_TYPE.items() if v == "MaxAchievements"),
    len(ACHIEVEMENT_TYPE))


def repair_profile(p):
    """Fix `p` in place. Returns (fixed, warnings) lists of messages."""
    fixed, warnings = [], []

    for name in ("mBEarnedAchievements", "mBShownAchievements"):
        arr = list(getattr(p, name))
        if len(arr) > ACHIEVEMENT_COUNT:
            extra = arr[ACHIEVEMENT_COUNT:]
            setattr(p, name, arr[:ACHIEVEMENT_COUNT])
            msg = f"{name}: trimmed {len(arr)} -> {ACHIEVEMENT_COUNT} entries"
            if any(extra):
                msg += " (dropped entries were set; they were invalid)"
            fixed.append(msg)
        elif len(arr) < ACHIEVEMENT_COUNT:
            warnings.append(
                f"{name} has {len(arr)} entries, expected {ACHIEVEMENT_COUNT}; "
                f"left unchanged")

    plants = p.mPottedPlant
    slots = getattr(p, "_plant_slots", len(plants))
    if len(plants) > MAX_POTTED_PLANTS:
        used = [pl for pl in plants if not pl.is_blank()]
        if len(used) > MAX_POTTED_PLANTS:
            warnings.append(
                f"{len(used)} plants are in use, more than {MAX_POTTED_PLANTS} "
                f"slots; plant list left unchanged")
        else:
            p.mPottedPlant = used + [
                PottedPlant() for _ in range(MAX_POTTED_PLANTS - len(used))]
            p._plant_slots = MAX_POTTED_PLANTS
            fixed.append(f"plant slots: trimmed {len(plants)} -> "
                         f"{MAX_POTTED_PLANTS}")
    elif len(plants) < MAX_POTTED_PLANTS:
        warnings.append(f"only {len(plants)} plant slots, expected "
                        f"{MAX_POTTED_PLANTS}; left unchanged")

    used_count = sum(1 for pl in p.mPottedPlant if not pl.is_blank())
    if p.mNumPottedPlants != used_count:
        fixed.append(f"mNumPottedPlants: {p.mNumPottedPlants} -> {used_count}")
        p.mNumPottedPlants = used_count

    return fixed, warnings
