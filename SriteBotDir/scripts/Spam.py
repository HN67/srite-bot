# Ryan Allard Random Words Generator
import random

vowels = "aoueiy"
consonants = "bcdfghjklmnpqrstvwxyz"
punctuation = "!.?"

def consonantBlock():
    string = []
    for i in range(random.randrange(2) + 1):
        string.append(consonants[random.randrange(len(consonants))])
    return "".join(string)

def vowelBlock():
    string = []
    for i in range(random.randrange(2) + 1):
        string.append(vowels[random.randrange(len(vowels))])
    return "".join(string)

def puncSymbol():
    return punctuation[random.randrange(len(punctuation))]

def syllable():
    string = []
    if random.randrange(10) < 8:
        string.append(consonantBlock())
    string.append(vowelBlock())
    if random.randrange(3) < 1:
        string.append(consonantBlock())
    return "".join(string)

def word():
    string = []
    for i in range(random.randrange(3) + 1):
        string.append(syllable())
    return "".join(string)

def sentence():
    string = []
    for i in range(random.randrange(15) + 1 + 5):
        string.append(word())
    return " ".join(string).capitalize() + puncSymbol()

def paragraph(sentences):
    string = []
    for i in range(sentences):
        string.append(sentence())
    return " ".join(string)
