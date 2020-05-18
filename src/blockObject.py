## Institut für Informatik, 
## Department of Algorithmische Bioinformatik
## Heinrich Heine Univversity Düsseldorf, Germany
## written by: Michael Wulfert
#--------- --------- --------- --------- --------- ---------|--------- --------|
# block objects for strings

from src.letterObject import findCharacter, getAlphabet, reportAlphabet, sumMaxValues
import string
#from choice import chooseMethod    # didn't work here

# This file organizes the blocks of the (presorted) string

class block(object):
    blockLetter = None
    # Reduction 1, Reduction 3:
    blockValue = 0      # block length
    # Reduction 2:
    blockCount  = 0     # actual number of block of same letter
    # Reduction 4:
    blockSum    = 0     # actual sum of block values of this letter
    # Reduction 7:
    nextSame    = None  # next block of same letter
    # ILP:
    blockNumber = -1
    lastSame    = None  # last block of same letter
    # DAG:    
    totalLength = 0     # sum of values until (but without) this block

    # Output:
    longString  = ""
    
    def __init__(self, letter, letterCount, number, totalLetterCount):
#        print("new block:", letter, letterCount)
        self.blockLetter = letter                           # Reduction 1
        self.blockValue = letterCount                       # Reduction 1, 3
        letter.addBlockCount(1)                             # Reduction 2
        self.blockCount = letter.blockCount                 # Reduction 2
        letter.newMaxValue(letterCount)                     # Reduction 3
        self.blockSum = letter.letterCount                  # Reduction 4
        self.longString = str(letter) * int(letterCount)    # Output
        self.blockNumber = number                           # ILP
        self.lastSame = letter.changeLastSameBlock(self)    # ILP
        self.nextSame = None                                # Reduction 7
        if self.lastSame != None:
            self.lastSame.nextSame = self
        self.totalLength = totalLetterCount                 # DAG
        
    def actualize(self, lastBlock, lastSameBlock, nextSameBlock):
        # lastBlock: last Block in Block List
        # lastSameBlock: last Block of same Letter
        letter = self.blockLetter   # letter of this block
        #self.blockLetter     #remains                      # Reduction 1
        #self.blockValue      #remains                      # Reduction 1, 3
        if lastSameBlock == None:       # first block of this letter
            letter.setBlockCount(1)     # set first block
            letter.setLetterCount(self.blockValue)
            letter.maxValue = self.blockValue
            letter.lastSame = self
            self.lastSame = None                            # ILP
        else: 
            letter.addBlockCount(1)     # is next block     # Reduction 2
            letter.addLetterCount(self.blockValue)
            letter.newMaxValue(self.blockValue)             # Reduction 3
            #letter.lastSame = self    
            #self.lastSame = letter.changeLastSameBlock(self)    # ILP
            #print(self, self.lastSame, lastSameBlock)
            #self.lastSame = lastSameBlock    # ILP
            self.lastSame.nextSame = self
              
        letter.setMaxValueSum(0)
        self.blockCount = letter.blockCount                 # Reduction 2
        self.blockSum = letter.letterCount                  # Reduction 4
        self.nextSame = nextSameBlock                       # Reduction 7  
        #self.nextSame = None    # will be changed           # Reduction 7  
        self.longString = str(letter) * int(self.blockValue)    # Output
        if lastBlock == None:           # first block in string
            self.blockNumber = 0                            # iLP
            self.totalLength = 0                            # DAG
        else:
            self.blockNumber = lastBlock.blockNumber +1         # iLP
            self.totalLength = lastBlock.getNewTotalLength()    # DAG
        
    def __str__(self):
        return str(self.blockLetter) + str(self.blockValue)
    
    # for Reduction 2a: Comparison of block letters
    def _eq_(self, other):
        return self.blockLetter == other.blockLetter
    
    # for Reduction9: Needs to sort blocks according to block value
    def __lt__(self, other):
        return self.blockValue < other.blockValue
    
    def isfirstBlock(self):
        return self.lastSame == None
        # first solution was:
        return self.blockCount == 1
    
    def isLastBlock(self):
        return self.nextSame == None
        # first solution was:
        return self.blockCount == self.blockLetter.blockCount
    
    def isUnique(self):
        return self.lastSame == None and self.nextSame == None
        # first solution was:
        return self.blockLetter.blockCount == 1
    
    # for Reduction 2a:
    #def makeUnique(self):
    #    self.lastSame = None
    #    self.nextSame = None
        
    def makeFirstBlock(self, blockNumber, totalLengt):
        self.lastSame = None
        self.blockCount = 1
        self.blockLetter.letterCount = self.blockValue
        self.blockLetter.setBlockCount(1)
        self.blockLetter.maxValue = self.blockValue
        self.blockLetter.lastSame = None
        self.blockLetter.stringLists = None
        self.blockLetter.clearMaxValueSum()
        self.blockSum = self.blockValue
        self.blockNumber = blockNumber
        self.nextSame = None    # might be also the last block
        self.totalLength = totalLengt + self.blockValue
        
    def makeNextBlock(self, lastBlock, blockNumber):
        self.lastSame = lastBlock
        self.blockCount = self.lastSame.blockCount +1
        self.blockLetter.letterCount += self.blockValue
        self.blockLetter.addBlockCount(1)
        self.blockLetter.newMaxValue(self.blockValue)
        self.blockLetter.lastSame = lastBlock
        self.blockSum = self.lastSame.blockSum + self.blockValue
        self.nextSame = None
        self.blockNumber = blockNumber
        self.totalLength = self.lastSame.totalLength + self.blockValue
        self.lastSame.nextSame = self
        
    def makeLastBlock(self):
        self.nextSame = None
        
    
    def getBlockValue(self):
        return self.blockValue
    
    def getBlockLetter(self):
        return self.blockLetter
    
    def getBlockSum(self):
        return self.blockSum
    
    def getLongBlock(self):
        return self.longString
    
    def printLongBlock(self):
        print(self.longString, end = "")
        
    def getLastSameBlock(self):
        return self.lastSame
        
    def getNextSameBlock(self):
        return self.nextSame
        
    def setBlockNumber(self, blockNumber):
        self.blockNumber = blockNumber
        
    def getBlockNumber(self):
        return self.blockNumber
        
    def getTotalLength(self):
        return self.totalLength
        
    def getNewTotalLength(self):
        return self.totalLength + self.blockValue
    
    # only for test purposes:
    def addBlockCount(self, n):
        self.blockCount += n
    
# creates a list of blocks of same letters from a string
def blockInput(string, parameter):
    if len(string) < 1: return None     # no input string
    
    blockList        = []   # empty list of blocks of letters
    blockAlphabet    = []   # empty list of letters
    lastCharacter    = None
    characterCount   = 1
    totalLetterCount = 0
    blockNumber      = 0
    
    for character in (string + "\n"):  # "\n" as endmark
        if character == lastCharacter and parameter['blockIdenticalLetters']:
            characterCount += 1
            
        elif lastCharacter != None:
            # ad last block of same characters to letterList
            letterObject = findCharacter(lastCharacter, blockAlphabet)
            letterObject.addLetterCount(characterCount)
            blockList.append(block(letterObject, characterCount, blockNumber, totalLetterCount))
            totalLetterCount += characterCount      # count letters for next block
            characterCount = 1 #set counter for next block
            blockNumber += 1
            
        lastCharacter = character     # to compare with next letter

    return blockList

def appendBlock(blockList, newletter):
    return
    
    
'''
# creates a list of blocks of same letters from a string
def blockString(string, letterList, inputType):
    if inputType == 'String':
        blockList = []  # empty List of blocks of letters
        if len(string) > 0: lastLetter = string[0]
        letterCount = 0
        
        for letter in (string + "\n"):  # "\n" as endmark
            if letter == lastLetter:
                letterCount += 1
                
            else:
                letterObject = findCharacter(lastLetter, letterList)
                blockList.append(block(letterObject, letterCount))
                letterCount = 1 #set counter for next block
                
            lastLetter = letter     # to compare with next letter
            
        return blockList
    
    # other input types may be added here
    return None
'''

def sumValues(blocklist):
    valueSum = 0
    for block in blocklist:
        valueSum += block.getBlockValue()
    return valueSum
    
def independendBlocks(blockList):    
    listOfBlocks = []
    actualBlocks = []
    overlap = 0
    
    for block in blockList:
        actualBlocks.append(block)
        if block.isfirstBlock(): overlap += 1
        if block.isLastBlock():  
            overlap -= 1
            if overlap == 0:        # next independent list
                listOfBlocks.append(actualBlocks)
                actualBlocks = []   # new empty list
    
    return listOfBlocks
def getLowerLimit(subBlockList, parameter):
    
    subAlphabet = getAlphabet(subBlockList)
    maxValue = sumMaxValues(subAlphabet)  #all maxima will be added  
    
    # test for single-letter-solution in long strings with small alphabets 
    if not parameter['everyLetterExists']: 
        for letter in subAlphabet:
            if letter.getLetterCount() > maxValue:
                maxValue = letter.getLetterCount() 
    
    # finds only a single optimal string if length > maxValue, therefore:
    if not parameter['showAllOptima']: 
        maxValue -= 1    # -1 to find max 
               
    return maxValue

#--------- --------- --------- --------- --------- ---------|--------- --------|

def reportBlockList(blockList):   
    blockStr = ""
    for block in blockList:
        blockStr += str(block) + "(" + str(block.blockCount) + "."
        if block.isLastBlock(): blockStr += "l"
        blockStr += ") "
    return blockStr
    
def reportBlockListExtended(blockList):
    blockStr  = reportBlockList(blockList) + "\n" 
    blockStr += reportCharacterList(blockList) + "\n\n"
    blockStr +=     reportAlphabet(getAlphabet(blockList), False) + "\n\n"
    return blockStr
    
def reportCharacterList(blockList):
    outString = ""
    for block in blockList:
        outString += block.getLongBlock()
    return outString

def reportAllCharacterLists(blockList, separator):
    outString = ""
    for block in blockList:
        outString += reportCharacterList(block)
        if block != blockList[-1]: outString += separator
    return outString

def reportAllLists(listlist):
    listStr = ""   
    for singleList in listlist:
        listStr += reportBlockList(singleList) + "\n"
    return listStr 
        
def reportBlockData(blockList, parameter):
    outString  = "different characters:     " + str(len(getAlphabet(blockList))) + "\n"
    outString += "lower limit of maxValues: " + str(getLowerLimit(blockList, parameter)) + "\n"
#    outString += "upper limit of maxValues: "  + "\n"  # vorläufig
    outString += "total length of string:   " + str(sumValues(blockList)) + "\n"
    outString += "block.totalLength " + str(blockList[-1].totalLength) + " + "
    outString += "value of this block " + str(blockList[-1].blockValue) 
    return outString


