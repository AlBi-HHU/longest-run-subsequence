## Institut für Informatik, 
## Department of Algorithmische Bioinformatik
## Heinrich Heine Univversity Düsseldorf, Germany
## written by: Michael Wulfert
#--------- --------- --------- --------- --------- ---------|--------- --------|
# methods for 'dag' algorithm: Directed Acyclic Graph

from src.blockObject import sumValues, reportAllLists, reportCharacterList, getLowerLimit
from src.letterObject import getAlphabet, reportAlphabet, reportAlphabetShort
from src.dagObject import GrowingString, \
    dublicateAndExtendStringLists, reportStringList, reportAlphabetOfStringLists
    
from sys import exit    # for debugging

#from blockRecursion import reportSublistData, reportOptimalSublists

def directedAcyclicGraph(givenBlockList, givenParameter):
    # constant Values as globals:
    global subBlockList, lenBlockList, totalLength, parameter, actualSubAlphabet
    # common values as globals:
    global optimalLists, maxValue, lastLetterBlockList, testedLetterLists, comparedLists
    
    #print("used method: dag = directed acyclic graph")
    
    # set constants
    subBlockList = givenBlockList    
    lenBlockList = len(subBlockList) 
    totalLength = sumValues(subBlockList)   
    parameter = givenParameter
    
    if parameter['printMethod']: print("used method: dag = directed acyclic graph")
    
    maxValue = getLowerLimit(subBlockList, parameter)  
    maxValue = 0

    testedLetterLists = 0
    
    optimalLists = []
    lastLetterBlockList = []
    comparedLists = 0
    
    if parameter['printSublist']: print(reportSublistData() )
    
    
    actualSubAlphabet = getAlphabet(subBlockList)
    actualSubAlphabet.sort()
    if parameter['printDAG']:
        print("DAG -> actual alphabet: \n" + reportAlphabet(actualSubAlphabet, parameter['reportPossibilities']))
    

    
    # HERE IT HAPPENS...
    blockLoop(parameter)
    
    
    
    
    if parameter['printSublist']: print(reportOptimalSublists() )
    
    return optimalLists, maxValue, 0, 0, testedLetterLists, comparedLists, 0
    # no values for recursions, bifurcations and constraints

def blockLoop(parameter):
    global subBlockList, lastLetterBlockList, actualSubAlphabet, pointerPos, totalLength, comparedLists
    global maxValue
    
    firstPos = subBlockList[0].getTotalLength()    # for Reduction 3
    lastBlockWasUnique = False   # for Reduction 6
    remainingLetters = totalLength
    
    # loop over all blocks in substring
    for actualBlock in subBlockList:
        actualLetter = actualBlock.getBlockLetter()
        actualValue  = actualBlock.getBlockValue()             
        # add value of actual block to maximal length in string list            
        actualLetter.addMaxValueSum(actualValue)
            
        
        if parameter['printDAG']:
            print("\nDAG -> actual letter:", actualLetter, end = " ")
            print("is in", str(actualBlock.getBlockNumber()+1) + "-th block")
        
        # for reduction 3+4
        remainingLetters -= actualValue
        actualLetter.setStillToReject(actualLetter.getLetterCount()- actualBlock.getBlockSum() )
        
        shortBlockList = lastLetterBlockList    # if it is not changed
        
        if actualBlock.isfirstBlock():  # first block with this letter
                
            # make new list in letter
            newStringObject = GrowingString()
            rejected = actualBlock.getTotalLength()-firstPos    # first pos of substring
            newStringObject.addBlockOfOtherLetters(actualBlock, rejected)
            actualLetter.newStringLists(newStringObject)
            
            #print("DAG -> new letter List:", actualLetter.getStringList() )
            #print("DAG -> new letter List:", reportStringBlockList(actualLetter.getStringLists()) )
        
        else: # actualLetter in lastLetterBlockList:
            
            if parameter['printDAG']:
                print("DAG -> actual Block in lastLetterBlockList", actualLetter)

            # corresponds to Reduction 0 and Reduction 5:
            if parameter['takeOnlyNewLetters']:
                shortBlockList = lastLetterBlockList[lastLetterBlockList.index(actualLetter)+1:]
            
            if parameter['printDAG']:
                print("DAG -> short letter Lists:", reportAlphabetShort(shortBlockList))
                #print("DAG ->  last letter Lists:", reportAlphabetShort(lastLetterBlockList) )  
            
            
            # corresponds to Reduction 0:
            lastLetterBlockList.remove(actualLetter)
            
            # add letterLists of last same actual letter
            rejected =  actualBlock.getTotalLength() - \
                        actualBlock.getLastSameBlock().getTotalLength() - \
                        actualBlock.getLastSameBlock().getBlockValue()
                        
            for actualStringList in actualLetter.getStringLists().copy():   # some elements may be removed
                #print("##### length actual string list:", len(actualLetter.getStringLists()))
   
                # Reduction 3: Works well only near the end of the string
                if parameter['breakIfTooSmall'] and remainingLetters < maxValue:    # else may not enough to add 
                    #print("##*## actual stringList:", actualStringList[0], " rejected:", rejected)
                    #print("      total length:", totalLength, " get rejected:", actualStringList[0].getRejected())
                    if (totalLength - actualStringList[0].getRejected() - rejected ) < maxValue:
                        actualLetter.getStringLists().remove(actualStringList)
                    #    print("      --- removed --- ")
                        continue
                    
                # Reduction 4: reject appending if result is too short
                if parameter['tooManyToReject']:  # as long as it didn't work
                    if parameter['breakIfTooSmall'] and remainingLetters < maxValue:                         
                        # calculate newToReject 
                        newToReject = 0
                        for letter in actualStringList[0].getUsedLetterList():
                            if letter != actualLetter:
                                newToReject += letter.getStillToReject()
                        # test if strings will be too short without already rejected and new to reject
                        if (totalLength - actualStringList[0].getRejected() - rejected - newToReject ) < maxValue:
                            actualLetter.getStringLists().remove(actualStringList)
                            #print("      --- removed --- ")
                            #print('      total length:', totalLength)
                            #print('      - actualStringList[0].getRejected():', actualStringList[0].getRejected())
                            #print('      - rejected:', rejected)
                            #print('      - newToReject:', newToReject)
                            #print('      < maxValue:', maxValue)
                            continue
                        
                        
                    else:   # only reduction 4, not reduction 3
                        if (totalLength - actualStringList[0].getToReject() ) < maxValue:
                            actualLetter.getStringLists().remove(actualStringList)
                            continue
                    
                for actualStringObject in actualStringList: 
                    actualStringObject.addBlockOfSameLetters(actualBlock, rejected)
                
            if parameter['printNewListLetter']: 
                print("  actual letter elongated:", actualLetter)
                    
            #print("DAG -> growing letter List:", actualLetter.getStringList() )
            #print("DAG -> growing letter List:", reportStringBlockList(actualLetter.getStringList()) )
        #    print("DAG -> number of growing letter Lists:", len(actualLetter.getStringLists()) )
            
            
        # Recursion 6: consecutive unique blocks handled together like one block
        if parameter['uniquesTogether'] and lastBlockWasUnique and actualBlock.isUnique():              
            lastBlockLetter = lastLetterBlockList[-1]
            shortBlockList = [lastBlockLetter]          # add only from last unique block
            lastLetterBlockList.remove(lastBlockLetter) # don't use last block letter any more
            
        # copy blocks of last letters without actual letter and elongate them
        # use reversed order to begin with latest = longest lists
        #for lastLetter in shortBlockList:    
        for lastLetter in shortBlockList[::-1]:    # it's sufficient to start after the last same letter,
                                                    # this corresponds to Reduction 0
            debug  = "    -> last letter in List:" + str( lastLetter) + "\twith "
            debug += str( sum((len(llist)) for llist in lastLetter.getStringLists())) + " Strings in " 
            debug += str(len(lastLetter.getStringLists())) + " letter combinations" 
        
            pointerPos = 0 # search starts at begin of stringList
            
            debug += str("\nxxxxxxxxxx pointerPos=0, Alphabets of stringLists:")
            debug += str( reportAlphabetOfStringLists(lastLetter.getStringLists()) )
            
            if parameter['printLetterComparisons']: print(debug)
            
            # list of found strings of last letter
            for stringLists in lastLetter.getStringLists():
                
                actualStringLists = actualLetter.getStringLists()   
                
                if False:   #  for debugging
                #    print("   DAG -> string Lists in last letter in List:", stringLists[0], "(begins with)")
                    print("   DAG -> string Lists in last letter in List:", reportStringList(stringLists, "; ") )
                #    print("   DAG -> already used letters in this stringLists:", (stringLists.getUsedLetterList()) )
                    print("   DAG -> already used letters in this stringLists:", end = " ")
                    print( reportAlphabetShort(stringLists[0].getUsedLetterList()) )
                
                
                if stringLists[0].isWithout(actualLetter):  # string lists with actual letter can't be used
                    comparedLists += 1
                #    print("      DAG -> bevStringObject:",    stringLists[0])  

                    lastTakenBlock = stringLists[0].getLastBlock()
                    rejected = actualBlock.getTotalLength() - lastTakenBlock.getTotalLength() \
                                - lastTakenBlock.getBlockValue()
                #    print("*** actualBlock", actualBlock.getLongBlock(), "has total Length:", actualBlock.getTotalLength())
                #    print("*** last Block", lastTakenBlock.getLongBlock(), "has total Length:", lastTakenBlock.getTotalLength())
                #    print("*** last Block", lastTakenBlock.getLongBlock(), "has Length:", lastTakenBlock.getBlockValue(), end = "")
                #    print(" add to rejected:", rejected)
                    newStringList = dublicateAndExtendStringLists(stringLists, actualBlock, lastLetter, rejected)
                    
                    # Reduction 3:
                    if parameter['breakIfTooSmall']:                        
                        if (totalLength - newStringList[0].getRejected() ) < maxValue:
                            continue                        
                    
                    # Reduction 4: reject appending if result is too short
                    if parameter['tooManyToReject']:  # as long as it didn't work
                        if (totalLength - newStringList[0].getToReject() ) < maxValue:
                            continue
    
                    
                    ''' not necessary debugging test
                    # sometimes the sorting didn't work correct: search new
                    if pointerPos < len(actualStringLists) and pointerPos > 0 \
                      and  newStringList[0] < actualStringLists[pointerPos][0]:
                        print("\n_____ pointerPos", pointerPos, "reset ___________________")
                        print("new string list [0]:", newStringList[0], "<", end = " ")
                        print("actual string list [pointerPos] [0]:", actualStringLists[pointerPos][0])
                        printAllLists([actualLetter]) 
                        if parameter['pointerPosResetExit']: exit() # for debugging
                        pointerPos = 0
                    '''        
                    # correct maxValueSum...
                    actualLetter.adaptMaxValueSum(newStringList[0].getStringValue())
                        
                    # find corresponding position in actual letter list
                    while pointerPos < len(actualStringLists) \
                            and  newStringList[0] > actualStringLists[pointerPos][0]:
                        pointerPos += 1 
                    
                    # new string list is last in actual string list:
                    # stringLists[0] > actualStringLists[pointerPos][0]
                    if pointerPos >= len(actualStringLists):
                        actualStringLists.append(newStringList) 
                    #    continue
                    
                    # combine new string list with actual string list (both have same letters)
                    elif newStringList[0] == actualStringLists[pointerPos][0]:
                        appendIfLongest(actualLetter, newStringList)
                    #    pointerPos += 1    # not with 'exit()' after reset pointerPos
                    #    continue
                    
                    # insert new string list in actual string list at pointerPos
                    else:   # newStringList[0] < actualStringLists[pointerPos][0]:                      
                        actualStringLists.insert(pointerPos, newStringList)    
                    #    continue
                    
                    # continue not necessary at the end of the loop...
                    
            
            if parameter['printNewListLetter']: 
                print("  last letter merged:", lastLetter, end = " - with ")
                print(str( sum((len(llist)) for llist in lastLetter.getStringLists())), end = "" )
                print(" Strings in " + str(len(lastLetter.getStringLists())) + " letter combinations" ) 
        
        # last block of a letter: test found strings for maximal length
        if actualBlock.isLastBlock():
            if parameter['printDAG']:
                print("DAG -> this was the last", actualLetter, "in this string ---------------------------")   
            if actualLetter.getMaxValueSum() >= maxValue:
                addLongestToResults(actualLetter)   # adds longest resutl strings to result list
            
        # maximal sum of values in string list   
        if parameter['printDAG']:
            print("DAG -> Actual Letter:", actualLetter, "- maxValueSum", actualLetter.getMaxValueSum(), end = ' - ')
            print("actual max value", maxValue)    
        
        if actualLetter.getMaxValueSum() > maxValue:
            maxValue = actualLetter.getMaxValueSum()
            pass
            
        lastLetterBlockList.append(actualLetter)  
        if parameter['printDAG']:
            print("DAG -> lastLetterBlockList, with this letter:", reportAlphabetShort(lastLetterBlockList))
        
        lastSameBlock = actualBlock.getLastSameBlock()
        if parameter['printDAG']:
            print("DAG -> actual block:", actualBlock, end = ",")
            if lastSameBlock != None:
                print(" last same block number:", lastSameBlock.getBlockNumber()+1 )
            else:
                print(" is first block with this letter")
        
        # Recursion 6:
        if parameter['uniquesTogether'] and lastBlockWasUnique and actualBlock.isUnique(): 
            actualLetter.getStringLists().remove([newStringObject]) 
        lastBlockWasUnique = actualBlock.isUnique()
        
    #    if parameter['printLetterLists']: printAllLists(actualSubAlphabet)  # print all letters
        if parameter['printLetterLists']: printAllLists([actualLetter])     # print only changed letters

def appendIfLongest(actualLetter, newStringList):
    global parameter, totalLength, pointerPos
    
    actualStringLists = actualLetter.getStringLists()
    
    #print("--------------- append if longest")
        
    if len(actualStringLists) > 0:
        if pointerPos < len(actualLetter.getStringLists()): 
            actualStringList = actualStringLists[pointerPos]
        else:
            actualStringList = actualStringLists[pointerPos-1]    # take last list elements
            
    if   len(newStringList[0]) < len(actualStringList[0]): 
        if parameter['printLetterComparisons']: 
            print("         DAG -> new string is shorter than actual string: forget new string")
        del newStringList
        return  # without appending new string object because it is too short
    
    # Reduction 3:
    if parameter['breakIfTooSmall']:  
        if False:   # for debugging
            print("breakIfTooSmall: totalLength:", totalLength, end = ", ")
            print("rejected:", actualStringList[0].getRejected(), end = ", ")
            print("maxValue:", maxValue)
            print("actualStringList[0]:", actualStringList[0], end = " - ")
            print("length actualStringList[0]:", len(actualStringList[0]), end = ", ")
            print("newStringList[0]:", newStringList[0])
        
        if (totalLength - newStringList[0].getRejected() ) < maxValue:
            actualStringLists.remove(actualStringList)
            # del actualStringList # delete unused list ?
            return        
    
    # Reduction 4: reject appending if result is too short
    if parameter['tooManyToReject']:  # as long as it didn't work
        if (totalLength - newStringList[0].getToReject() ) < maxValue:
            actualStringLists.remove(actualStringList)
            # del actualStringList # delete unused list ?
            return
    
    #actual string is shorter than new string: replace actual strings by new strings
    if len(newStringList[0]) > len(actualStringList[0]):
        if parameter['printLetterComparisons']: 
            print("         DAG -> actual string is shorter than new string: replace it")
        #actualStringLists[pointerPos] = newStringList
        # or with swap:
        actualStringLists[pointerPos], newStringList = newStringList, actualLetter.getStringLists()[pointerPos]
        del newStringList   # is now the old stringList
        
    # same letters and same length:
    else:   # len(newStringList[0]) == len(actualStringList[0]): 
    
        if parameter['printLetterComparisons']: 
            print("         DAG -> actual string is has equal length with new string: add new string")
        
        if parameter['showAllOptima']:
            actualStringLists[pointerPos].extend(newStringList)

    return

    
def addLongestToResults(actualLetter):
    global parameter, actualSubAlphabet 
    global optimalLists, maxValue, lastLetterBlockList, testedLetterLists
    
    lenAlphabet = len(actualSubAlphabet)
    ctrlString = "\nnumber of different letters in subalphabet: " + str(lenAlphabet)
    
    for actualLists in actualLetter.getStringLists()[::-1]:     # in reverse order: largest first
        if parameter['everyLetterExists'] and lenAlphabet > len(actualLists[0].getUsedLetterList() ):
            continue    # or break?
        for actualStringList in actualLists:
            testedLetterLists += 1
            listLength = len(actualStringList)
            ctrlString += "\nlen actual string list: " + str(listLength)
            ctrlString += ", actual maxValue: " + str(maxValue)
            ctrlString += " find longest substring " # + str(actualStringList)
            ctrlString += "with last letter: " + str(actualLetter)
            #print("DAG->> results, actual list", actualStringList, " has length", listLength)
            if listLength > maxValue:
                maxValue = listLength
                optimalLists = [actualStringList.getStringBlockList()]
                ctrlString += ": new maximum"
            
            elif parameter['showAllOptima'] and listLength == maxValue:
                optimalLists.append(actualStringList.getStringBlockList() )
                ctrlString += ": " + str(len(optimalLists)) + "th maximum added"                
        
    if parameter['printNewMaxima']: print(ctrlString, "\n")
            

#--------- --------- --------- --------- --------- ---------|--------- --------|

# copied control outputs   
        
def reportSublistData():
    global subBlockList, totalLength, parameter
    global maxValue 
    
    ctrlString  = "\n" + "substring: "
    ctrlString += reportCharacterList(subBlockList) + "\n"
    ctrlString += "length of this substring: " + str(totalLength) + "\n"
    ctrlString += "lower limit for optimum:  " +str(maxValue) + "\n"
    return ctrlString

def reportOptimalSublists():
    global optimalLists
    return "\noptimal subLists: \n" + reportAllLists(optimalLists)

        
def printAllLists(subAlphabet):
    
    print("\n*******************************************")
    
    for letter in subAlphabet:
        print("letter:", letter, "\tactual maxValue", maxValue)#, "\n")
        actualLetterList = letter.getStringLists()
        #print("    stringList:", actualLetterList)
        if actualLetterList:
            for stringList in actualLetterList:
                print(letter, "-> letters used:", end = "")
            #    print(" string list: ", reportAlphabetShort(stringList), end = "\t" )
                print(reportAlphabetShort(stringList[0].getUsedLetterList()), end = "\t" )
                print(" rejected+toReject: ", stringList[0].getRejected(), end = "+" )
                print(stringList[0].getToReject(), end = "\t" )
                print("string object(s): ", end = "")
                for strObject in stringList:
                    #if strObject == None:
                    if strObject:
                        print(strObject, end = ", ")
                    else:
                        print("is empty/None", end = "")
                print()
    
    print("*******************************************\n")
    
    
    
