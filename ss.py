from random import randint, shuffle
from pprint import pprint

BOARDSIZE = 14
NUMANTS = 10
MAXVISION = 4
MAXMETABO = 4

# Create the sugar class. For now, update is isntant generation.
class Sugar(object):
    def __init__(self, x, y, max_val=None, current_val=None):
        self.maxval = max_val
        self.currentval = current_val
    # TODO: use updateSugar
    def updateSugar(self):
        if self.currentval != self.maxval:
           self.currentval = self.maxval

class Ant(object):
    def __init__(self, x, y, scape):
        self.vision = randint(1, MAXVISION)
        self.metabo = randint(1, MAXMETABO)
        self.loc = (x, y)
        self.nextmove = (x, y)
        self.state = 10
        self.parent = scape
        self.local = []
        self.minrow = 0
        self.mincol = 0

    def getVision(self):
        maxcol = onBoard(self.loc[1] + self.vision)
        mincol = onBoard(self.loc[1] - self.vision)
        maxrow = onBoard(self.loc[0] + self.vision)
        minrow = onBoard(self.loc[0] - self.vision)
        # print "col col row row", maxcol, mincol, maxrow, minrow
        #Use slice to get the y's out
        count = 0
        self.local = []
        for i in xrange(minrow, maxrow + 1):
            self.local.append([0] * (maxcol - mincol + 1))
        for row in xrange(minrow, maxrow + 1):
            self.local[count] = self.parent.landscape[row][mincol:maxcol + 1]
            count = count + 1
        self.minrow = minrow
        self.mincol = mincol

    def strategy(self):
        newval = -1
        for row in xrange(len(self.local)):
            for col in xrange(len(self.local[row])):
                try:
                    if self.local[row][col].currentval == newval and randint(0,1) == 1:
                       goal = (row, col)
                    elif self.local[row][col].currentval > newval:
                       newval = self.local[row][col].currentval
                       goal = (row, col)
                except AttributeError:
                    pass

        #Finds how far you need to go to get to max
        #Then a unit vector of sorts
        #And calculates next move
        # We "subtract out" self.loc earlier in the get vision state, so the distance is just the goal
        goal = (goal[0] + self.minrow, goal[1] + self.mincol)
        deltarow = goal[0] - self.loc[0]
        deltacol = goal[1] - self.loc[1]
        drow = getDir(deltarow)
        dcol = getDir(deltacol)
        nextrow = self.loc[0] + drow
        nextcol = self.loc[1] + dcol
        self.nextmove = (nextrow, nextcol)
        try:
            if self.parent.landscape[nextrow][nextcol].currentval >= 0:
               print "moving to some sugar mmm mmm"
        except AttributeError:
           print "I tried to move into an ant!"
           self.nextmove = self.loc

    def updateState(self):
        if self.loc != self.nextmove:
            print "i moved from " , self.loc , " to " , self.nextmove

        if self.loc == self.nextmove:
            print "i didn't move: " , self.loc , " and still " , self.nextmove
        self.loc = self.nextmove
        (i, j) = self.loc
        #Throws an error the first time because there is no sugar at the current location
        try:
            self.state = self.state + self.parent.landscape[i][j].currentval - self.metabo
        except AttributeError:
            self.state = self.state - self.metabo
        # Dead ants go to anty heaven
        if self.state <= 0:
            self.loc = 'Heaven'
            print "I went to anty heaven!"


class Scape(object):
    def __init__(self):
        self.original = self.initscape() 
        self.landscape = self.initscape()
        self.ants = []
        self.addAnts()

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

    def addAnts(self):
        for i in xrange(NUMANTS):
            self.addAnt()

    def addAnt(self):
        x = randint(0, BOARDSIZE - 1)
        y = randint(0, BOARDSIZE - 1)
        ant = Ant(x, y, self)
        self.landscape[x][y] = ant
        self.ants.append(ant)

    def iterate(self):
        #Don't want to give any ants an advantage for being first in the list
        shuffle(self.ants)
        for ant in self.ants:
            if ant.loc == 'Heaven':
                continue
            (i, j) = ant.loc
            ant.getVision()
            ant.strategy()
            ant.updateState()
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
        count = 0
        for i in xrange(BOARDSIZE):
            for j in xrange(BOARDSIZE):
                try:
                    printscape[i][j] = self.landscape[i][j].currentval
                except AttributeError:
                    if self.landscape[i][j].loc != 'Heaven':
                        printscape[i][j] = 'A' + str(self.landscape[i][j].state)
                        count = count + 1

        print "we got this many ants" , count
        pprint(printscape)

# This is a dumb function
# Maybe wrap it in a lambda later
def getDir(dist):
    if dist > 0: unit = 1
    elif dist < 0: unit = -1
    elif dist == 0: unit = 0
    return unit

def onBoard(val):
    if val < 0: val = 0
    elif val >= BOARDSIZE: val = BOARDSIZE - 1
    else: val = val
    return val

if __name__ == "__main__":

    scape = Scape()
    scape.printScape()

    for run in xrange(30):
        scape.iterate()
        scape.printScape()
        raw_input()
