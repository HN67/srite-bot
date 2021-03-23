"""Config file for srite bot"""


class economy:
    """Config for economy functionality"""

    taxAmount = 100
    taxTime = 3600

    growTimeMin = 180
    growTimeMax = 300
    growMatureTime = 60  # Coins start growing after this time
    growRatio = 1 / 24  # Number of coins grown per second (after the mature time)

    collectTime = 10.0

    attributes = ["money", "taxTime"]

    hashLength = 100


class bot:
    """Config for core bot"""

    color = 0x00A229

    prefixes = ("s.", "s:")


class stocks:
    """Config for stocks functionality"""

    items = [
        "SRITE",
        "POG",
        "NWRD",
        "DMND",
        "NOTYET",
        "ANGERY",
        "BRUH",
        "AYA",
        "ANSLY",
        "SPNWRD",
        "NGWRD",
        "CORONA",
        "ALLAH",
    ]

    standard = 100
    change = 5

    tradeChange = 1

    updateFrequency = 300


class time:
    """Time configs"""

    interval = 1
    timeout = 10


class uni:
    """Unicode aliases"""

    leftArrow = "\u2B05"  # "\u21E6"
    upArrow = "\u2B06"
    rightArrow = "\u27A1"  # "\u27A1"
    downArrow = "\u2B07"  # "\u21E9"


class fools:
    """Config for april fools features"""

    channels = [271124181372895242]


class roles:
    """Config for roles"""

    valid_roles = [
        507374117964742670,
        805266626898427915,
        823732123931901972,
    ]
