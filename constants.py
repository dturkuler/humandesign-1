"""
Constants for Human Design calculations.

This module contains all the constant values needed for Human Design calculations:
- Offset for I-Ching/Zodiac synchronization
- Planet mapping for Swiss Ephemeris
- I-Ching gates circle list
- Chakra (energy center) definitions and mappings
- Gate-to-chakra mappings
- Channel meaning dictionary
- Incarnation cross types
- Circuit types and groupings
- Awareness streams
"""

# Synchronize I-Ching and zodiac circle: 58°
# Human design systems start at gate 41 in Aries (source: Ra Uru Hu)
ICHING_OFFSET = 58

# Swiss Ephemeris planet codes
# Based on codes from swe: dict([[i, swe.get_planet_name(i)] for i in range(0, 23)])
SWE_PLANET_DICT = {
    "Sun": 0,
    "Earth": 0,  # Sun position -180 longitude
    "Moon": 1,
    "North_Node": 11,  # True Node is used
    "South_Node": 11,  # North_Node position -180 longitude
    "Mercury": 2,
    "Venus": 3,
    "Mars": 4,
    "Jupiter": 5,
    "Saturn": 6,
    "Uranus": 7,
    "Neptune": 8,
    "Pluto": 9,
}

# Order of gates in the Human Design bodygraph
ICHING_CIRCLE_LIST = [
    41, 19, 13, 49, 30, 55, 37, 63, 22, 36, 25, 17, 21, 51, 42, 3,
    27, 24, 2, 23, 8, 20, 16, 35, 45, 12, 15, 52, 39, 53, 62, 56,
    31, 33, 7, 4, 29, 59, 40, 64, 47, 6, 46, 18, 48, 57, 32, 50,
    28, 44, 1, 43, 14, 34, 9, 5, 26, 11, 10, 58, 38, 54, 61, 60
]

# Energy Centers (Chakras) abbreviations:
# HD=Head, AA=Ajna, TT=Throat, GC=G-Centre, SL=Sacral, 
# SN=Spleen, SP=Solar Plexus, HT=Heart/Ego, RT=Root
CHAKRA_LIST = ["HD", "AA", "TT", "GC", "HT", "SP", "SN", "SL", "RT"]

# Gates to Chakra mapping - (gate1, gate2): (chakra1, chakra2)
GATES_CHAKRA_DICT = {
    (64, 47): ("HD", "AA"),
    (61, 24): ("HD", "AA"),
    (63, 4): ("HD", "AA"),
    (17, 62): ("AA", "TT"),
    (43, 23): ("AA", "TT"),
    (11, 56): ("AA", "TT"),
    (16, 48): ("TT", "SN"),
    (20, 57): ("TT", "SN"),
    (20, 34): ("TT", "SL"),
    (20, 10): ("TT", "GC"),
    (31, 7): ("TT", "GC"),
    (8, 1): ("TT", "GC"),
    (33, 13): ("TT", "GC"),
    (45, 21): ("TT", "HT"),
    (35, 36): ("TT", "SP"),
    (12, 22): ("TT", "SP"),
    (32, 54): ("SN", "RT"),
    (28, 38): ("SN", "RT"),
    (57, 34): ("SN", "SL"),
    (50, 27): ("SN", "SL"),
    (18, 58): ("SN", "RT"),
    (10, 34): ("GC", "SL"),
    (15, 5): ("GC", "SL"),
    (2, 14): ("GC", "SL"),
    (46, 29): ("GC", "SL"),
    (10, 57): ("GC", "SN"),
    (25, 51): ("GC", "HT"),
    (59, 6): ("SL", "SP"),
    (42, 53): ("SL", "RT"),
    (3, 60): ("SL", "RT"),
    (9, 52): ("SL", "RT"),
    (26, 44): ("HT", "SN"),
    (40, 37): ("HT", "SP"),
    (49, 19): ("SP", "RT"),
    (55, 39): ("SP", "RT"),
    (30, 41): ("SP", "RT"),
}

# Channel meanings and descriptions
CHANNEL_MEANING_DICT = {
    (64, 47): ["Abstraction", "D. of mental activity and clarity"],
    (61, 24): ["Awereness", "D. of a thinker"],
    (63, 4): ["Logic", "D. of mental muse? mixed with doubt"],
    (17, 62): ["Acceptance", "D. of an organizational being"],
    (43, 23): ["Structuring", "D. of individuality"],
    (11, 56): ["Curiosity", "D. of a searcher"],
    (16, 48): ["The Wave Length", "D. of a talent"],
    (20, 57): ["The Brain Wave", "D. of penetrating awareness"],
    (20, 34): ["Charisma", "D. where thoughts must become deeds"],
    (32, 54): ["Transformation", "D. of being driven"],
    (28, 38): ["Struggle", "D. of stubbornness "],
    (18, 58): ["Judgment", "D. of insatiability"],
    (20, 10): ["Awakening", "D. of commitment to higher principles"],
    (31, 7): ["The Alpha", "For 'good' or 'bad', a d. of leadership"],
    (8, 1): ["Inspiration", "The creative role model"],
    (33, 13): ["The Prodigal", "The d. of witness"],
    (10, 34): ["Exploration", "A d. of following one's convictions"],
    (15, 5): ["Rythm", "A d. of being in the flow"],
    (2, 14): ["The Beat", "A d. of being the keeper of keys"],
    (46, 29): ["Discovery", "A d. of succeding where others fail"],
    (10, 57): ["Perfected Form", "A d. of survival"],
    (57, 34): ["Power", "A d. of an archetype"],
    (50, 27): ["Preservation", "A. d. of custodianship"],
    (45, 21): ["Money", "A d. of a materialist"],
    (59, 6): ["Mating", "A d. focused on reproduction"],
    (42, 53): ["Maturation", "A d. of balanced developement,cyclic"],
    (3, 60): ["Mutation", "Energy which fluctuates and initiates, pulse"],
    (9, 52): ["Concentration", "A d. of determination, focused"],
    (26, 44): ["Surrender", "A d. of a transmitter"],
    (25, 51): ["Initiation", "A d. of needing to be first"],
    (40, 37): ["Community", "A d. of being part, seeking a whole"],
    (35, 36): ["Transitoriness", "A d. of a 'Jack of all Trades'"],
    (12, 22): ["Openness", "A d, of a social being"],
    (49, 19): ["Synthesis", "A d. of being sensitive"],
    (55, 39): ["Emoting", "A d. of moodiness"],
    (30, 41): ["Recognition", "A d. of focused energy"],
}

# Incarnation Cross Types (RAC=Right Angle Cross, LAC=Left Angle Cross, JXP=Juxtaposition)
IC_CROSS_TYP = {
    (1, 3): "RAC",
    (1, 4): "RAC",
    (2, 4): "RAC",
    (2, 5): "RAC",
    (3, 5): "RAC",
    (3, 6): "RAC",
    (4, 6): "RAC",
    (4, 1): "JXP",
    (5, 1): "LAC",
    (5, 2): "LAC",
    (6, 2): "LAC",
    (6, 3): "LAC",
}

# Penta gates
PENTA_DICT = {
    31: [], 8: [], 33: [], 7: [], 1: [], 13: [],
    15: [], 2: [], 46: [], 5: [], 14: [], 29: []
}

# Circuit types for channels
CIRCUIT_TYPE_DICT = {
    (24, 61): "Knowledge",
    (23, 43): "Knowledge",
    (1, 8): "Knowledge",
    (2, 14): "Knowledge",
    (3, 60): "Knowledge",
    (39, 55): "Knowledge",
    (12, 22): "Knowledge",
    (28, 38): "Knowledge",
    (20, 57): "Knowledge",
    (10, 34): "Centre",
    (25, 51): "Centre",
    (4, 63): "Realize",
    (17, 62): "Realize",
    (7, 31): "Realize",
    (5, 15): "Realize",
    (9, 52): "Realize",
    (18, 58): "Realize",
    (16, 48): "Realize",
    (47, 64): "Sense",
    (11, 56): "Sense",
    (13, 33): "Sense",
    (29, 46): "Sense",
    (42, 53): "Sense",
    (30, 41): "Sense",
    (35, 36): "Sense",
    (32, 54): "Ego",
    (26, 44): "Ego",
    (19, 49): "Ego",
    (37, 40): "Ego",
    (21, 45): "Ego",
    (6, 59): "Protect",
    (27, 50): "Protect",
    (10, 20): "Integration",
    (20, 34): "Integration",
    (34, 57): "Integration",
    (10, 57): "Integration",
}

# Circuit group types
CIRCUIT_GROUP_TYPE_DICT = {
    "Knowledge": "Individual",
    "Centre": "Individual",
    "Realize": "Collective",
    "Sense": "Collective",
    "Ego": "Tribal",
    "Protect": "Tribal",
    "Integration": "Integration",
}

# Awareness streams
AWARENESS_STREAM_DICT = {
    (58, 18, 48, 16): "Taste",
    (38, 28, 67, 20): "Intuition",
    (54, 32, 44, 26): "Instinct",
    (41, 30, 36, 35): "Feel",
    (39, 55, 22, 12): "Emotion",
    (19, 49, 37, 40): "Sensitivity",
    (64, 47, 11, 56): "Realize/Meaning",
    (61, 24, 43, 23): "Knowledge",
    (63, 4, 17, 62): "Understand"
}

# Awareness stream groups
AWARENESS_STREAM_GROUP_DICT = {
    "Taste": "Spleen",
    "Intuition": "Spleen",
    "Instinct": "Spleen",
    "Feel": "SolarPlexus",
    "Emotion": "SolarPlexus",
    "Sensitivity": "SolarPlexus",
    "Realize/Meaning": "Ajna",
    "Knowledge": "Ajna",
    "Understand": "Ajna"
}

# Strategy by energy type
STRATEGY_BY_TYPE = {
    "GENERATOR": "Wait to respond",
    "MANIFESTING GENERATOR": "Wait to respond, then inform",
    "PROJECTOR": "Wait for invitation",
    "MANIFESTOR": "Inform before action",
    "REFLECTOR": "Wait 28 days for clarity"
}

# Authority descriptions
AUTHORITY_DESCRIPTIONS = {
    "SP": "Emotional Authority",
    "SL": "Sacral Authority",
    "SN": "Splenic Authority",
    "HT": "Ego-Manifested Authority",
    "GC": "Self-Projected Authority",
    "HT_GC": "Ego-Projected Authority",
    "outher_auth": "No Inner Authority",
    "lunar": "Lunar Authority"
}
