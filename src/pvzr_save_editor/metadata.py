"""Enum tables and UI metadata (labels, groups, enum bindings).

Wraps the data modules `enums` and `meta` so the rest of the app can ask for
labels / enum tables by name.
"""

from . import enums as _enums
from . import meta as _meta


def _meta_attr(name, default):
    return getattr(_meta, name, default)


FIELD_LABELS = _meta_attr("FIELD_LABELS", {})
FIELD_GROUPS = _meta_attr("FIELD_GROUPS", [])
PROFILE_ENUM_FIELDS = _meta_attr("PROFILE_ENUM_FIELDS", {})
POTTED_PLANT_ENUM_FIELDS = _meta_attr("POTTED_PLANT_ENUM_FIELDS", {})
ARRAY_FIELD_ENUMS = _meta_attr("ARRAY_FIELD_ENUMS", {})
STORE_TOGGLE_ITEMS = set(_meta_attr("STORE_TOGGLE_ITEMS", set()))
FIELDS_OWNED_BY_OTHER_TABS = set(_meta_attr(
    "FIELDS_OWNED_BY_OTHER_TABS",
    {"mPurchases", "mBShownAchievements", "mBEarnedAchievements",
     "mNumPottedPlants"}))

# Every UPPER_CASE {int: name} dict in enums...
ENUM_TABLES = {}
for _attr in dir(_enums):
    _value = getattr(_enums, _attr)
    if (_attr.isupper() and isinstance(_value, dict)
            and all(isinstance(k, int) for k in _value)):
        ENUM_TABLES[_attr] = _value

# ...plus the level/minigame tables from meta.
for _name in ("ADVENTURE_LEVELS", "MINIGAMES", "SURVIVAL_LEVELS",
              "PUZZLE_LEVELS", "COOP_LEVELS", "CLOUDY_DAY_LEVELS",
              "CHALLENGE_RECORDS"):
    _table = _meta_attr(_name, None)
    if isinstance(_table, dict):
        ENUM_TABLES.setdefault(_name, _table)


def enum_for(table_name):
    return ENUM_TABLES.get(table_name, {})


def label_for(field_name):
    return FIELD_LABELS.get(field_name, field_name)
