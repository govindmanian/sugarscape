from random import randint, shuffle
from pprint import pprint

BOARDSIZE = 14
NUMANTS = 10 
MAXVISION = 4
MAXMETABO = 4

class Sugar(object):
    def __init__(self, x, y, max_val=None, current_val=None):
        self.maxval = max_val
        self.currentval = current_val
    def updateSugar(self):
        if self.currentval != self.maxval:
           self.currentval = self.maxval

class Ant(object):
    def __init__(self, x, y):
        # self.vision = randint(1, MAXVISION)
        self.metabo = randint(1, MAXMETABO)
        self.vision = BOARDSIZE 
        self.metabo = randint(1, MAXMETABO)
        self.loc = (x, y)
        self.nextmove = (x, y)
        self.state = 10

    def getNextMove(self, scape):
        goal = self.loc
        newval = -1
        # Find the local max
        for row in xrange(self.loc[0] - self.vision, self.loc[0] + self.vision):
            for col in xrange(self.loc[1] - self.vision, self.loc[1] + self.vision):
                if 0 <= row <= (BOARDSIZE - 1) and 0 <= col <= (BOARDSIZE - 1):
                    try:
                        if scape.landscape[row][col].currentval == newval and randint(1,2) == 1:
                            goal = (row, col)
                        elif scape.landscape[row][col].currentval > newval:
                            newval = scape.landscape[row][col].currentval
                            goal = (row, col)
                    except AttributeError:
                        pass

        deltax = goal[0] - self.loc[0]
        deltay = goal[1] - self.loc[1]
        dx = getDir(deltax)
        dy = getDir(deltay)
        nextx = self.loc[0] + dx
        nexty = self.loc[1] + dy
        self.nextmove = (nextx, nexty)

        if scape.landscape[nextx][nexty] is Ant:
           print "i tried to move into another ant"
           self.nextmove = self.loc

    def updateState(self, scape):
        if self.loc != self.nextmove:
            print "i moved from " , self.loc , " to " , self.nextmove

        self.loc = self.nextmove
        (i, j) = self.loc
        try:
            self.state = self.state + scape.landscape[i][j].currentval - self.metabo
        except AttributeError:
            self.state = self.state - self.metabo
        # Dead ants go to anty heaven
        if self.state <= 0:
            self.loc = 'Heaven'
            print "I went to anty heaven"


class Scape(object):
    def __init__(self):
        self.original = self.initscape() 
        self.landscape = self.initscape()

    def initscape(self):
        original = []
        # Initialize the board
        for i in xrange(BOARDSIZE):
            original.append([0]*BOARDSIZE)

        # Make some sugar - have to do this kind of stupidly for now
        for i in xrange(BOARDSIZE):
            for j in xrange(BOARDSIZE):
                original[i][j] = Sugar(i, j, max_val=0, current_val=0)

        for i in xrange(7):
            for j in xrange(7):
                original[i][j] = Sugar(i, j, max_val=5, current_val=5)
        for i in xrange(BOARDSIZE - 7, BOARDSIZE):
            for j in xrange(BOARDSIZE - 7, BOARDSIZE):
                original[i][j] = Sugar(i, j, max_val=5, current_val=5)

        for i in xrange(1, 7 - 1):
            for j in xrange(1, 7 - 1):
                original[i][j] = Sugar(i, j, max_val=6, current_val=6)
        for i in xrange(BOARDSIZE - 6, BOARDSIZE - 1):
            for j in xrange(BOARDSIZE - 6, BOARDSIZE - 1):
                original[i][j] = Sugar(i, j, max_val=6, current_val=6)

        for i in xrange(2, 7 - 2):
            for j in xrange(2, 7 - 2):
                original[i][j] = Sugar(i, j, max_val=7, current_val=7)
        for i in xrange(BOARDSIZE - 5, BOARDSIZE - 2):
            for j in xrange(BOARDSIZE - 5, BOARDSIZE - 2):
                original[i][j] = Sugar(i, j, max_val=7, current_val=7)

        original[3][3] = Sugar(3, 3, max_val=8, current_val=8)
        original[10][10] = Sugar(BOARDSIZE - 4, BOARDSIZE - 3 , max_val=8, current_val=8)
        return original

    def iterate(self, ants):
        antlist = range(NUMANTS)
        #Don't want to give any ants an advantage for being first in the list
        shuffle(antlist)
        for idx in antlist:
            ant = ants[idx]
            if ant.loc == 'Heaven':
                continue
            (i, j) = ant.loc
            ant.getNextMove(scape)
            ant.updateState(scape)
            if ant.loc == 'Heaven':
                self.landscape[i][j] = self.original[i][j]
                continue
            (newi, newj) = ant.loc
            # If it wants to move, move it and replace with some sugar
            if (newi, newj) != (i, j):
                self.landscape[newi][newj] = ant
                self.landscape[i][j] = self.original[i][j]

    def printScape(self):
        printscape = []
        for i in xrange(BOARDSIZE):
            printscape.append([0]*BOARDSIZE)

        for i in xrange(BOARDSIZE):
            for j in xrange(BOARDSIZE):
                try:
                    printscape[i][j] = self.landscape[i][j].currentval
                except AttributeError:
                    if self.landscape[i][j].loc != 'Heaven':
                        printscape[i][j] = 'A' + str(self.landscape[i][j].state)

        pprint(printscape)
"""
        for i in xrange(BOARDSIZE):
            for j in xrange(BOARDSIZE):
                try:
                    printscape[i][j] = self.initscape[i][j].currentval
                except AttributeError:
                    if self.initscape[i][j].loc != 'Heaven':
                        printscape[i][j] = 'A' + str(self.initscape[i][j].state)
        pprint(printscape)
"""

# This is a dumb function
# Maybe wrap it in a lambda later
def getDir(dist):
    if dist > 0: unit = 1
    elif dist < 0: unit = -1
    elif dist == 0: unit = 0
    return unit

if __name__ == "__main__":

    ants = []
    for i in xrange(NUMANTS):
        row = randint(0, BOARDSIZE - 1)
        col = randint(0, BOARDSIZE - 1)
        newant = Ant(row, col)
        ants.append(newant)

    scape = Scape()

    for ant in ants:
        scape.landscape[ant.loc[0]][ant.loc[1]] = ant


    for run in xrange(30):
        scape.iterate(ants)
        scape.printScape()
        raw_input()
