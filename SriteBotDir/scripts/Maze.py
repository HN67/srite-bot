#Ryan Allard Maze Generator December 17th 2017
'''Module that provides functionality for generating mazes'''
import random

#Data Container of a cell (borders and whether neighbors are visited)
class Cell:
    '''Data Container of borders and whether neighbors are visited'''
    def __init__(self, y, x):
        self.y = y
        self.x = x
        self.borders = {"top":True,"right":True,"bottom":True,"left":True}
        self.unvisited = {"top","right","bottom","left"}

#Takes a 2-D Array of cells and draws an ASCII map
def drawMap(mazeMap):
    '''Takes a 2-D Array of cells and returns an ASCII map string'''
    #Create top map border and initalize display
    display = " _"*len(mazeMap[0])+"\n"
    #For each row
    for row in mazeMap:
        #Create empty line
        line = ""
        #For each cell
        for cell in row:
            #If cell has left border, add vertical line
            if cell.borders["left"]:
                line += "|";
            else:
                line += " ";
            #If cell has bottom border, add horizontal line
            if cell.borders["bottom"]:
                line += "_";
            else:
                line += " ";
            #Shouldnt need to check right and top, it should be
            #reflected in the other cells left/bottom
        #Add right map border
        line += "|"
        #Add line to display
        display += (line + "\n")
    return display

#Directions (y, x)
direction = {"top":(-1,0),"right":(0,1),"bottom":(1,0),"left":(0,-1)}

#Returns opposite of a direction
def oppositeDirection(direction):
    '''Returns opposite of a direction'''
    return {"top":"bottom","bottom":"top","left":"right","right":"left"}[direction]


class MazeGenerator:
    '''Object used to generate mazes'''

    def __init__(self, size):
        self.mapSize = size
        self.mazeMap = []
    
    #Notifies all neighboring cell that (y, x) is visited
    def _updateVisits(self, y, x):
        '''Notifies all neighboring cell that (y, x) is visited'''
        #For each direction
        for way in list(direction.keys()):
            #Get reference to neighbor cell
            newY = y + direction[way][0]
            newX = x + direction[way][1]
            #Make sure cell is in map
            if newX >= 0 and newX < self.mapSize and newY >= 0 and newY < self.mapSize:
                #Create reference and remove unvisited tag
                neighbor = self.mazeMap[newY][newX]
                neighbor.unvisited.remove(oppositeDirection(way))

    #Generates map into mazeMap
    def generateMap(self, mapSize = "default"):
        '''Creates an array of cells in a maze pattern'''

        #Set default mapSize
        if mapSize == "default":
            mapSize = self.mapSize
        else:
            self.mapSize = mapSize

        #Create clean 2-d list of cells
        self.mazeMap = [[Cell(y,x) for x in range(mapSize)] for y in range(mapSize)]

        #Add border to map
        for i in range(mapSize):
            self.mazeMap[0][i].unvisited.remove("top")
            self.mazeMap[mapSize - 1][i].unvisited.remove("bottom")
            self.mazeMap[i][0].unvisited.remove("left")
            self.mazeMap[i][mapSize - 1].unvisited.remove("right")

        #Init the history list
        history = [(0,0)]

        #Set starting cell
        x = 0
        y = 0
        #Update visited status on neighboring cells
        self._updateVisits(y, x)

        while len(history) > 0:
            #Create reference to current cell
            cell = self.mazeMap[y][x]
            #Pick a random unvisited direction
            try:
                move = random.choice(tuple(cell.unvisited))
            except IndexError:
                #Cell has no unvisited neighbors, backtrack
                history.pop()
                try:
                    y = history[-1][0]
                    x = history[-1][1]
                except IndexError:
                    #Maze is complete
                    pass
            else:
                #Break border on old cell
                cell.borders[move] = False
                #Move x and y
                y += direction[move][0]
                x += direction[move][1]
                #Create reference to new cell
                cell = self.mazeMap[y][x]
                #Add new position to history
                history.append((y,x))
                #Break border on new cell
                cell.borders[oppositeDirection(move)] = False
                #Update visited status on neighboring cells
                self._updateVisits(y, x)

        #Return finished map
        return self.mazeMap
