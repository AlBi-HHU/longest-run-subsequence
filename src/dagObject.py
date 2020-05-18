## Institut für Informatik, 
## Department of Algorithmische Bioinformatik
## Heinrich Heine Univversity Düsseldorf, Germany
## written by: Michael Wulfert
#--------- --------- --------- --------- --------- ---------|--------- --------|
# objects for 'dag' algorithm: Directed Acyclic Graph

from src.letterObject import reportAlphabetShort
from src.blockObject import sumValues
#    reportCharacterList, reportBlockList, reportBlockListExtended

# keine rekursiven Importe! blockObject, letterObject

# This file organizes the blocks of the (presorted) totalString

class GrowingString(object):
    blocksAdded = []
    stringValue = 0     # sumValue(self.blocksAdded)
    usedLetters = []
    totalString = ""
    # Reduction 3:
    rejected       = 0
    # Reduction 4:
    toReject       = 0
    endLetterValue = 0
    
    
    def __init__(self):
        self.blocksAdded    = []
        self.stringValue    = 0
        self.usedLetters    = []
        self.totalString    = ""
        self.rejected       = 0
        self.toReject       = 0
        self.endLetterValue = 0
        
    def __str__(self):
        output  = self.totalString
#        output  = "growingStringObject, totalString: '" + self.totalString 
#        output += "' blocksAdded: " + reportBlockList(self.blocksAdded)
#        output += "' blocksAdded: " + reportBlockListExtended(self.blocksAdded)
#        output += " has " + reportAlphabetShort(self.usedLetters) + " as letters"
        return output
        
    def __len__(self):
        return self.stringValue
        # may be faster than:
        return sumValues(self.blocksAdded)
    
    # comparison of letter lists
    def __lt__(self, other):
        # compare from the end of the lists
        return self.usedLetters[-1::-1] < other.usedLetters[-1::-1] 
    
    # no longer used...
        if len(self.usedLetters) < len(other.usedLetters): return True
        if len(self.usedLetters) > len(other.usedLetters): return False
        return self.usedLetters < other.usedLetters
    
    def __eq__(self, other):
    #    if other == None: return False
        #if len(self.usedLetters) != len(other.usedLetters): return False
        return self.usedLetters == other.usedLetters
    
    def __gt__(self, other):
        # compare from the end of the lists
        return other.usedLetters[::-1] < self.usedLetters[::-1] 
    
    # no longer used...
        if len(other.usedLetters) < len(self.usedLetters): return True
        if len(other.usedLetters) > len(self.usedLetters): return False
        return other.usedLetters < self.usedLetters
     
    def delete(self):
        pass        # del has to be implemented
        del self    # but it's not used...
    
    def getStringBlockList(self):
        return self.blocksAdded
    
    def getUsedLetterList(self):
        return self.usedLetters
    
    def getRejected(self):
        return self.rejected
    
    def getToReject(self):
        return self.toReject
    
    def getLastBlock(self):
        return self.blocksAdded[-1]
    
    def addToReject(self, toAdd):
        self.toReject += toAdd
    
    def getEndLetterValue(self):
        return self.endLetterValue
    
    def isWithout(self, letter):
    #    print("      DAG-Object -> self.blocksAdded:", reportCharacterList(self.blocksAdded) )
        if letter in self.usedLetters: 
    #       print("False:", letter, block.getBlockLetter() )
            return False
    #    print("True")
        return True
    
    def dublicateStringObject(self):
        newStringObject = GrowingString()
        
        newStringObject.blocksAdded = self.blocksAdded.copy()
        newStringObject.stringValue = self.stringValue
        newStringObject.usedLetters = self.usedLetters.copy()
        newStringObject.totalString = self.totalString
        newStringObject.rejected    = self.rejected
        newStringObject.toReject    = self.toReject
        newStringObject.endLetterValue = self.endLetterValue
        
        return newStringObject
    
    def addBlockOfOtherLetters(self, newBlock, rejected):
        (self.blocksAdded).append(newBlock)
        self.stringValue += newBlock.getBlockValue()
        blockLetter = newBlock.getBlockLetter()
    #    print("*** -> dagObject: new letter added:", blockLetter )
        self.usedLetters.append(blockLetter)
        self.usedLetters.sort()
        self.totalString += newBlock.getLongBlock()
#        self.totalString += str(newBlock)
        self.rejected += rejected
        self.endLetterValue = newBlock.getBlockValue()
    
    def addBlockOfSameLetters(self, newBlock, rejected):
        self.blocksAdded.append(newBlock)
        self.stringValue += newBlock.getBlockValue()
    #    blockLetter = newBlock.getBlockLetter() # used in next (outcommented?) line
    #    print("*** -> dagObject: same letter (not) added:", blockLetter )
#        self.usedLetters.append(blockLetter)    # already done
#        self.usedLetters.sort()                 # not necessary
        self.totalString += newBlock.getLongBlock()
#        self.totalString += str(newBlock)
        self.rejected += rejected
        self.endLetterValue += newBlock.getBlockValue()
    
    def getStringValue(self):
        return self.stringValue

    def hasEqualLetters(self, other):
        if other == None:
            return False
        
        # new version with sorted used letter lists:
        if len(self.usedLetters) != len(other.usedLetters):
            return False
        
        for i in range(len(self.usedLetters)):
            if self.usedLetters[i] != other.usedLetters[i]:
                return False
            
        return True
    
'''    
    # old, simple version, may be removed   
    def hasEqualLetters(self, other): 
        if other == None:
            return False
                
        for letter in self.usedLetters:
            if letter not in other.usedLetters:
        #        print("s-o      letter", letter, "not in", reportAlphabetShort(other.usedLetters))
                return False
            
        for letter in other.usedLetters:
            if letter not in self.usedLetters:
        #        print("o-s      letter", letter, "not in", reportAlphabetShort(self.usedLetters))
                return False
            
        return True
'''

def dublicateAndExtendStringLists(stringList, newBlock, lastLetter, rejected):
    newStringList = stringList.copy()
    # deep copy:
    for i in range(len(stringList)):
        newStringList[i] = stringList[i].dublicateStringObject()
        newStringList[i].addToReject(lastLetter.getLetterCount() - stringList[i].getEndLetterValue())
        newStringList[i].addBlockOfOtherLetters(newBlock, rejected) 
    
    return newStringList


def reportStringList(stringList, separator):
    output = ""
    for strings in stringList[:-1]:
        output += strings.totalString + separator
    output += stringList[-1].totalString    
    return output

def reportStringBlockList(stringList):
    output = ""
    for blockStrings in stringList:
        output += " "
        for blockString in blockStrings:
            output += str(blockString.totalString) + " "
    return output

def reportAlphabetOfStringLists(stringLists):
    output = ""
    for i in range(len(stringLists)):
        output += str(i) + ":" + reportAlphabetShort(stringLists[i][0].usedLetters) + " - "
    return output    
        
        
        
        
        
        
        
        
    