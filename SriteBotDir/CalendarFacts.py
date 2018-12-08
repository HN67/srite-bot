# HN67 Calendar Facts XKCD Generator

import random

class Node:
    def __init__(self, data, parents = [], children = []):
        self.data = data
        self.parents = parents
        self.children = children

class Chain:

    def __init__(self, root):
        self.nodes = {root:Node(root)}
        self.root = root

    # Add a node to the chain
    def add(self, parents, children, data = []):

        # If a string is given, encapsulate in list
        if type(parents) is str:
            parents = [parents]
        if type(children) is str:
            children = [children]
        if type(data) is str:
            data = [data]

        # Pad data list with children tags
        data = [data[i] if i < len(data) else child for i, child in enumerate(children)]
        
        # For each child, create with data and parents
        for index, child in enumerate(children):
            if child in self.nodes:
                raise ValueError("Child '{}' is already a node".format(child))
            self.nodes[child] = Node(data[index], parents)

        # Update parent's children
        for parent in parents:
            self.nodes[parent].children = self.nodes[parent].children + children

    def connect(self, parent, child):
        self.nodes[parent].children.append(child)
        self.nodes[child].parents.append(parent)

xkcd = Chain("Did you know that")

xkcd.add("Did you know that",["the1","the2","the3","daylight","leap","easter","the4",
                               "toyota truck month","shark week"],
         ["the","the","the","daylight","leap","easter","the",
          "toyota truck month","shark week"])

xkcd.add("the1",["fall","spring"])
xkcd.add(["fall","spring"],"equinox")
xkcd.add("the2",["winter","summer"])
xkcd.add(["winter","summer"],["solstice","olympics"])
xkcd.add("the3",["earliest","latest"])
xkcd.add(["earliest","latest"],["sunrise","sunset"])
xkcd.add("daylight",["saving","savings"])
xkcd.add(["saving","savings"],"time")
xkcd.add("leap",["day","year"])
xkcd.add("the4",["harvest","super","blood"])
xkcd.add(["harvest","super","blood"],"moon")
xkcd.add(["equinox","solstice","olympics","sunrise","sunset","time","day","year",
          "easter","moon","toyota truck month","shark week"],
         ["happens","drifts out of sync with the","might"])
xkcd.add("happens",["earlier","later","at the wrong time"])
xkcd.add(["earlier","later","at the wrong time"],"every year")
xkcd.add("drifts out of sync with the",["sun","moon2","zodiac","gregorian",
                                        "mayan","lunar","iPhone","atomic clock in colorado"],
         ["sun","moon"])
xkcd.add(["gregorian","mayan","lunar","iPhone"],"calendar")
xkcd.add("might",["not happen","happen twice"])
xkcd.add(["not happen","happen twice"],"this year")
xkcd.add(["every year","sun","moon2","zodiac","calendar","atomic clock in colorado","this year"],
         "because of")
xkcd.add("because of",["time zone legislation in","a decree by the Pope"
                       " in the 1500s","precession","libration","nutation",
                       "libation","eccentricity","obliquity","magnetic"
                       " field reversal","an arbitrary decision by"])
xkcd.add(["precession","libration","nutation",
          "libation","eccentricity","obliquity"],"of the")
xkcd.add("of the",["moon3","sun2","Earth's axis","equator","prime meridian",
                   "international date","mason-dixon"],["moon","sun"])
xkcd.add(["international date","mason-dixon"],"line")
xkcd.add("time zone legislation in",["indiana","arizona","russia"])
xkcd.add("an arbitrary decision by",["Benjamin Franklin","Isaac Newton","FDR"])
xkcd.add(["indiana","russia","arizona","a decree by the Pope in the 1500s",
          "moon3","sun2","Earth's axis","equator","prime meridian","line",
          "magnetic field reversal","Benjamin Franklin","Isaac Newton","FDR"],"?")


def random_chain_path(chain):

    string = []
    spot = chain.root
    while chain.nodes[spot].children:
        string.append(chain.nodes[spot].data)
        spot = random.choice(chain.nodes[spot].children)
    string.append(chain.nodes[spot].data)
    string = " ".join(string)
    return string


