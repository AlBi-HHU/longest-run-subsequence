## Institut für Informatik, 
## Department of Algorithmische Bioinformatik
## Heinrich Heine Univversity Düsseldorf, Germany
## written by: Michael Wulfert
#--------- --------- --------- --------- --------- ---------|--------- --------|
# choose algorithm, return output strings
## for unit tests: chooseMethod separated from gbr 

from src.blockObject import reportAllLists, reportBlockData, \
     reportBlockListExtended, reportCharacterList, \
     reportAllCharacterLists, sumValues, reportBlockList, blockInput
from src.dagLoop import directedAcyclicGraph
from src.ilp import ilpStart
from src.testParameter import getAlgorithms
from src.letterObject import alphabet, reportAlphabetShort, getAlphabet

# Reduction 2a
def internalBlocks(actualList, parameter):
    parameter['showAllOptima'] = False  # didn't work with all optima
    #print("****** all Blocks ******") 
    listOfLetters = getAlphabet(actualList)
    #print("Alphabet:", reportAlphabetShort(listOfLetters))
    actualBlocks = []
    numberOfBlocks = 0
    
    lastBlockInList = None
    for l in range(len(actualList)):
        ###print("---> bevore:\n" + reportBlockData(actualList[:l+1], parameter))
        block = actualList[l] 
        #print(lastBlockInList, "***", block.getLastSameBlock(), block)
        block.actualize(lastBlockInList, block.getLastSameBlock(), block.getNextSameBlock())
        #print(l, block)
        actualLetter = block.getBlockLetter()
        actualBlocks.append(block)
        ###print("---> after:\n" + reportBlockData(actualBlocks, parameter))
        block.setBlockNumber(numberOfBlocks)
        numberOfBlocks +=1
        
        # verry new try, with LetterList = list of letters in use
        letterList = []
        for firstIndex in range(len(actualBlocks)-1, -1, -1):
            #print("firstIndex", firstIndex, end = " ")
            block = actualBlocks[firstIndex]
            letter = block.getBlockLetter()
            #print("first block", block)
            
            if block.isLastBlock():
                #print("letter", letter, "appended to letterList")
                letterList.append(letter)
            if letter not in letterList:
                #print("letter", letter, "not in letterList")
                break
            # letter is in list
            if block.isfirstBlock():
                #print("letter", letter, "removed from letterList")
                letterList.remove(letter)
            if letterList == []:
                #print("EMPTY LETTER LIST: IT WILL HAPPEN!!!")
                # here it happens!!!
                #print("first index, len actualBlocks", firstIndex, len(actualBlocks)-1)
                currentList = actualBlocks[firstIndex:]
                #print("currentList", reportBlockList(currentList))
                results = chooseMethod(currentList, parameter)  # reduce current string
                resultList = results[0][0]  # take only first result
                #print("resutList", reportBlockList(resultList))
                
                
                lastBlock = None
                resultList[0].actualize(actualBlocks[firstIndex-1], None, None)
                for resultBlock in resultList:
                    if lastBlock != None:
                        if lastBlock.getBlockLetter()!=resultBlock.getBlockLetter():
                            resultBlock.actualize(lastBlock, None, None)
                            #print(lastBlock, "!=", resultBlock)
                        else:   # both blocks are equal
                            resultBlock.actualize(lastBlock, lastBlock, None)
                            #print(lastBlock, "==", resultBlock)
                    lastBlock = resultBlock
                #resultList[-1].makeLastBlock()  # last  block in result is (new) last  block of this letter
                
                actualBlocks[firstIndex:] = resultList   
                break  

        #print("actual Letter:", actualLetter, "actual letter stack", reportAlphabetShort(letterList))
        #print()
        lastBlockInList = actualBlocks[-1]

    return [[actualBlocks], 0, 0, 0, 0, 0, 0]
    




def chooseMethod(actualList, parameter):
    global dag, ilp
#    print("+++parameter: method", parameter['method'])
    dag, ilp = getAlgorithms()
    # tree = 'tree'
    # walk = 'walk' 
    # wide = 'wide'
    # dag  = 'dag'
    # ilp  = 'ilp'
        
    if parameter['method'] == dag:
        results = directedAcyclicGraph(actualList, parameter)
    elif parameter['method'] == ilp:
        results = ilpStart(actualList, parameter)
    
    return results

#--------- --------- --------- --------- --------- ---------|--------- --------|

# help text

def helpText(parameter):
    helptxt  = ""
    helptxt += "This python3 program solves the GROUPING BY REMOVAL problem \n"
    helptxt += "Set parameter in file: " + str(parameter['parameterFile'] + "\n")
    helptxt += "start program with $python3 gbr.py \n"
    helptxt += "first  optional parameter: string or file (without or with .) \n"
    helptxt += "second optional parameter: algorithm \n"
    helptxt += "available algorithms: " + str(getAlgorithms()) + "\n"
    return helptxt
    
# reports for output

def reportInputBlocks(blockList, parameter):
    
    output  = "string in blocks: "
    output += "(blockObject number. l = last blockObject)\n"
    output += reportBlockListExtended(blockList)
    output += reportBlockData(blockList, parameter) + "\n"
    
    return output

def reportIndependentSublists(listOfBlockLists):
    output = "independent sublists: \n"
    output += reportAllLists(listOfBlockLists)
    return output

def reportSubstringResults(parameter, results):
    global tree, walk, wide, dag, ilp
    output  = "\n"
    if parameter['method'] == tree or parameter['method'] == walk:
        output += "optimum of sublist: " + str(results[1])
        output += " found in " + str(results[2]) + " recursion steps, "
        output += str(results[3]) + " of them are bifurcations \n"
    elif parameter['method'] == ilp:
        output += " using " + str(results[5]) + " constraints \n"
    output += "optimal reduced sublists:\n"
    # lists of optimal substrings:
    output += reportAllCharacterLists(results[0], "\n") + "\n"   
    return output
    
        
def reportLongSummary(parameter, blockList, optimum, optima, maxima, \
          recursions, bifurcations, leafes, listOfBlockLists, compared, constraints):
    
    output  = "\n" + "Summary\n" + "--------\n"
    output += reportCharacterList(blockList) + "\n"
    output += "Maximal value: " + str(optimum)
    output += " of " + str(sumValues(blockList) ) + "\n"
    for i, lists in enumerate(optima):#    output += "|\n"
        output += "\nSubstring " + str(i+1) + " has " + str(len(lists)) 
        output += " optimal sublist"        
        if len(lists) != 1: output += "s" 
        output += " with value " + str(maxima[i]) 
        output += reportOneSummary(parameter, maxima[i], recursions[i],\
                 bifurcations[i], leafes[i], listOfBlockLists[i],\
                 listOfBlockLists, compared[i], constraints[i])
        output += "\n" + reportAllCharacterLists(lists, "\n") + "\n"
        
    return output
        
        
def reportOneSummary(parameter, maxima, recursions, bifurs, leafes,\
                     blockList, listOfBlockLists, compared, constraint):
    global tree, walk, wide, dag, ilp
    output  = "\n"
    if parameter['method'] == tree or parameter['method'] == walk:
        output += "found in " + str(recursions) + " recursion"
        if recursions != 1: output += "s" 
        output += ", " + str(bifurs) + " of them are bifurcation"
        if bifurs != 1: output += "s" 
    if parameter['method'] == tree:
        output += " and "
    if parameter['method'] == dag:
        output += str(compared) + " lists compared and "
    if parameter['method'] == tree or parameter['method'] == dag:
        output += str(leafes) + " string"
        if leafes != 1: output += "s" 
        output += " tested for maximal length."
    elif parameter['method'] == ilp:
        output += " found using in total " + str(constraint) + " constraints"
    output += "\n"
    output += reportAllCharacterLists(listOfBlockLists, " ") + "\n"
    output += "reduced by " + str(sumValues(blockList)-maxima)
        
    return output

def reportResult(parameter, solutions, optimum, blockList,listOfBlockLists, optima, maxima, \
                 recursions, bifurcations, leafes, compared, constraints):
    global tree, walk, wide, dag, ilp
    output = ""
    if not parameter['onyResultString']:
        output += "Total result: \n" 
        output += "============= \n"
        output += "The whole string has " + str(solutions)
        if parameter['method'] == walk:
            output += " solutions, maximum length found was " + str(optimum)
        else:    
            output += " solutions, each with a total value of " + str(optimum)
        output += " from " + str(sumValues(blockList)) + " letters, "
        output += reportOneSummary(parameter, sum(maxima), sum(recursions),\
                     sum(bifurcations), sum(leafes), blockList,\
                     listOfBlockLists, sum(compared), sum(constraints))

        if parameter['printResultList']:
            output += " to: (choose in every line one block) \n"
            for sublist in optima:
                output += reportAllCharacterLists(sublist, "; ")
                output += "\n"
        else: output += "\n"
    else: 
        for sublist in optima:
            output += reportAllCharacterLists(sublist, "")
        
    return output

def reportShortSummary(parameter, maxima, recursions, bifurcations, leafes, compared, constraints):
    global tree, walk, wide, dag, ilp
    output      =                                          "\n"
    output     += "Maxima:         " + str(maxima)       + "\tsum: " + str(sum(maxima))       + "\n"
    if  parameter['method'] == tree\
     or parameter['method'] == walk\
     or parameter['method'] == wide:
        output += "Recursions:     " + str(recursions)   + "\tsum: " + str(sum(recursions))   + "\n"
    if  parameter['method'] == tree\
     or parameter['method'] == walk:
        output += "Bifurcations:   " + str(bifurcations) + "\tsum: " + str(sum(bifurcations)) + "\n"
    if  parameter['method'] == dag:
        output += "compared lists: " + str(compared)     + "\tsum: " + str(sum(compared))     + "\n"
    if  parameter['method'] == tree\
     or parameter['method'] == walk\
     or parameter['method'] == dag:
        output += "strings tested: " + str(leafes)       + "\tsum: " + str(sum(leafes))       + "\n"
    elif parameter['method'] == ilp:
        output += "Constraints:    " + str(constraints)  + "\tsum: " + str(sum(constraints))  + "\n"
    
    return output
