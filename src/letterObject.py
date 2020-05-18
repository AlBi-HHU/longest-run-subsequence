## Institut für Informatik, 
## Department of Algorithmische Bioinformatik
## Heinrich Heine Univversity Düsseldorf, Germany
## written by: Michael Wulfert
#--------- --------- --------- --------- --------- ---------|--------- --------|
# This file organizes the alphabet of the string

class alphabet(object):
    letterName   = ""       # name of the character
    letterCount  = 0        # total number of this character in string
    # Reduction 2:
    blockCount   = 0        # total number of blocks of this letter in string
    # Reduction 3:
    maxValue     = 0        # value of largest blockObject
    # ILP:
    lastSame     = None     # last block of same letter
    #DAG
    orderNumber   = 0       # number in sub alphabet, to order string lists
    stringLists   = None    # list of possible stringObjectsLists
    stillToReject = 0       # number of remaining letters of this
    maxValueSum   = 0       # actual maximal value sum in stringLists
    # Reduction 2a: old version?
    nextBlockNr   = -1
    #firstBlock    = None    # first block of this letter in input blockList
    finished      = False   # after last use of this letter in block list
    
    def __init__(self, name, count):
        self.letterName  = name
        self.orderNumber = count
        self.maxValueSum = 0
    #    self.finished    = False 

    def __str__(self):
        return self.letterName
    
    def __hash__(self):
        return self.orderNumber
    
    def __eq__(self, other):
        if other == None: return False
    #    return self == other
    #    return self.letterName == other.letterName
        return self.orderNumber == other.orderNumber
    
    def __ne__(self, other):
        if other == None: return True
    #    return self.letterName != other.letterName
        return self.orderNumber != other.orderNumber
    
    def __lt__(self, other):
        if other == None: return False
#        return self.letterName < other.letterName
        # other possibility:
        return self.orderNumber < other.orderNumber
    
    def setLetterCount(self, n):
        self.letterCount = n
    
    def addLetterCount(self, n):
        self.letterCount += n
        
    def getLetterCount(self):
        return self.letterCount
    
    def setBlockCount(self, n):
        self.blockCount = n
    
    def addBlockCount(self, n):
        self.blockCount += n
        
    def getBlockCount(self):
        return self.blockCount
    
    def newMaxValue(self, value):
        if value > self.maxValue:
            self.maxValue = value
        
    def getMaxValue(self):
        return self.maxValue
    
    def getLastSameBlock(self):
        return self.lastSame
    
    def changeLastSameBlock(self, block):
        oldBlock = self.lastSame
        self.lastSame = block
        return oldBlock
    
#    def findIn(self, alphabet):
#        for letter in alphabet:
#            if self.letterName == letter:
#                return letter    

    # for DAG:
    def newStringLists(self, newStringObject):
        self.stringLists = [[newStringObject]]
        
    def getStringLists(self):
        return self.stringLists
        
    def setStringLists(self, newStringLists):
        self.stringLists = newStringLists
        
#    def appendToStringList(self, newStringObject):
#        self.stringList.append(newStringObject)
        
    def insertIntoStringLists(self, pos, newStringList):
#        pos = len(self.stringList)-1
#        while pos > 0 and self.stringList[pos] > newStringObject:
#            pos -= 1
        self.stringLists.insert(pos, newStringList)

    '''        
    def copyStringListAndElongate(self, letterList, actualBlock):
        newLetterList = letterList.copy()
        newLetterList.addBlock(actualBlock)
        self.stringList.append(newLetterList)
    '''
        
    
    def setOrderNumber(self, n):
        self.orderNumber = n
        
    def getStillToReject(self):
        return self.stillToReject
    
    def setStillToReject(self, newValue):
        self.stillToReject = newValue
    
    #not necessary, use addMaxValueSum:    
    #def setMaxValueSum(self, value):
    #    self.maxValueSum = value
    
    def clearMaxValueSum(self):
        self. maxValueSum = 0
    
    def setMaxValueSum(self, value):
        self. maxValueSum = value
        
    def addMaxValueSum(self, value):
        self.maxValueSum += value
        
    def adaptMaxValueSum(self, value):
        if value > self.maxValueSum:
            self.maxValueSum = value
        
    def getMaxValueSum(self):
        return self.maxValueSum
    
    '''
    def setFirstBlock(self, firstBlock):
        self.firstBlock = firstBlock
    
    def getFirstBlock(self):
        return self.firstBlock
    '''
        
    def finishLetter(self):
        self.finished = True
    
    def isFinished(self):
        return self.finished
    
    def setNextBlockNr(self, n):
        self.nextBlockNr = n
        
    def getNextBlockNr(self):
        return self.nextBlockNr
        
    
        
def findCharacter(characterToFind, letterList):
    # if characterToFind already exists in stringList: return letter
    for letter in letterList:
        if characterToFind == str(letter):
            return letter
    
    # if letterToFind not jet exists: create new letter 
    newLetter = alphabet(characterToFind, len(letterList))
    letterList.append(newLetter)
    return newLetter

def getAlphabet(blockList):
    letterList = []
    for block in blockList:
        actualLetter = block.getBlockLetter()
        if actualLetter not in letterList:
            letterList.append(actualLetter)
    return letterList
   


def sumMaxValues(letterList):
    sumValues = 0
    for letter in letterList:
        sumValues += letter.getMaxValue()
    return sumValues

def sumLetter(letterList):
    sumLetter = 0
    for letter in letterList:
        sumLetter += letter.getLetterCount()
    return sumLetter

# calculate possibilities
def calculatePossibilities(letterList, everyLetterExists):
    possibilities = 1
    addEveryLetter = 1
    if everyLetterExists: addEveryLetter = 0
    for letter in letterList:
        possibilities *= letter.getBlockCount() + addEveryLetter
    return possibilities


def reportAlphabetShort(letterList):
    letterStr = ""
    for letter in letterList:
        letterStr += str(letter)
    return letterStr

def reportAlphabet(letterList, withPossibilities):
    letterStr = ""
    for letter in letterList:
        letterStr += str(letter)
        letterStr += " (" + str(letter.orderNumber + 1) + "-th letter): "
        letterStr += str(letter.getLetterCount()) + " letter"
        if letter.getLetterCount() != 1: letterStr += "s"
        if letter.getBlockCount() > 0:
            letterStr += " in " + str(letter.getBlockCount()) + " blockObject"
            if letter.getBlockCount() != 1: letterStr += "s"
            letterStr += ", largest blockObject has "
            letterStr += str(letter.getMaxValue()) + " letter"
            if letter.getMaxValue() != 1: letterStr += "s"
        letterStr += "\n"
    
    if withPossibilities:    
        letterStr += "Number of possibilities if every letter must be used:"
        letterStr += str(calculatePossibilities(letterList, True ) ) + "\n"
        letterStr += "Number of possibilities if any letter may be used:"
        letterStr += str(calculatePossibilities(letterList, False) ) + "\n"
    
    return letterStr
    
    