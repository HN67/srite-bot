# Ryan Allard Alt-Paths Chain

import random

class Option:
    '''Class that holds a list of options'''

    def __init__(self, *options):
        self.options = options

    def value(self):
        """Returns value of random item from list"""
        return value(random.choice(self.options))

class Chain:
    '''Class that holds chain of values'''

    def __init__(self, *values):
        self.values = values

    def value(self):
        """Returns joined values of all items from list"""
        return "".join([value(i) for i in self.values])

def value(item):
    '''Trys to get the value of the item, otherwise returns the item'''

    try:
        return item.value()
    except AttributeError:
        return item


# XKCD Chain
xkcd = Chain("Did you know that ",Option(Chain("the ",Option("fall ","spring "),"equinox "),
                                         Chain("the ",Option("winter ","summer "),Option("solstice ","olympics ")),
                                         Chain("the ",Option("earliest ","latest "),Option("sunrise ","sunset ")),
                                         Chain("Daylight ",Option("Saving ","Savings "),"Time "),
                                         Chain("leap ",Option("day ","year ")),
                                         "Easter ",
                                         Chain("the ",Option("Harvest ","Super ","Blood "),"Moon "),
                                         "Toyota Truck Month ",
                                         "Shark Week "),
             Option(Chain("happens ",Option("earlier ","later ","at the wrong time "),"every year "),
                    Chain("drifts out of sync with the ",Option("sun ","moon ","zodiac ",
                                                                Chain(Option("Gregorian ","Mayan ","Lunar ","iPhone "),"calendar "),
                                                                "atomic clock in Colorado ")),
                    Chain("might ",Option("not happen ","happen twice "),"this year ")),
             "because of ",
             Option(Chain("time zone legislation in ",Option("Indiana","Arizona","Russia")),
                    "a decree by the Pope in the 1500's",
                    Chain(Option("precession ","libration ","nutation ","libation ","eccentricity ","obliquity "),
                          "of the ",
                          Option("moon","sun","Earth's axis","equator","prime meridian",Chain(Option("International Date ","Mason-Dixon "),"Line"))),
                    "magnetic field reversal",
                    Chain("an arbitrary decision by ",Option("Benjamin Franklin","Isaac Newton","FDR"))),
             "? Apparently ",
             Option("it causes a predictable increase in car accidents",
                    "thats why we have leap seconds",
                    "scientists are really worried",
                    Chain("it was even more extreme during the ",Option("Bronze Age","Ice Age","Cretaceous","1990s")),
                    Chain("there's a proposal to fix it, but it ",Option("will never happen",
                                                                         "actually makes things worse",
                                                                         "is stalled in Congress",
                                                                         "might be unconstitutional")),
                    "it's getting worse and no one knows why"),
             ". (While it may seem like trivia, it ",
             Option("causes huge headaches for software developers","is taken advantage of by high-speed traders",
                    "triggered the 2003 Northeast Blackout","has to be corrected for by GPS satellites",
                    "is now recognized as a major cause of World War 1"),
             ").")
                    
                    
             
                          
                    
                          
             
