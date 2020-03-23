"""Config file for srite bot"""

class economy:
    """Config for economy functionality"""

    taxAmount = 50
    taxTime = 3600

    collectTime = 10.0

    attributes = ["money", "taxTime"]

    hashLength = 100

class bot:
    """Config for core bot"""

    color = 0x00A229

    prefixes = ("s.", "s:")

class stocks:
    """Config for stocks functionality"""

    items = ["SRITE",
             "POG",
             "NWRD",
             "DMND",
             "NOTYET",
             "ANGERY",
             "BRUH",
             "AYA",
             "ANSLY",
             "SPNWRD",
             "NGWRD"
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

    leftArrow = "\u2B05"#"\u21E6"
    upArrow = "\u2B06"
    rightArrow = "\u27A1"#"\u27A1"
    downArrow = "\u2B07"#"\u21E9"