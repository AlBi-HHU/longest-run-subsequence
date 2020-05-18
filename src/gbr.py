## Institut für Informatik, 
## Department of Algorithmische Bioinformatik
## Heinrich Heine Univversity Düsseldorf, Germany
## written by: Michael Wulfert
#--------- --------- --------- --------- --------- ---------|--------- --------|
# This is the main program

from sys import argv, stderr
import random
from src.blockObject import independendBlocks, blockInput
     
#from letterObject import sumLetter, getAlphabet
from src.choice import chooseMethod, reportInputBlocks, \
    reportIndependentSublists, reportSubstringResults, \
    reportLongSummary, reportShortSummary, reportResult, \
    helpText, internalBlocks
from src.testParameter import takeParameter 

import time
from src.letterObject import calculatePossibilities, getAlphabet

#--------- --------- --------- --------- --------- ---------|--------- --------|
# main program

def stringProcessor(parameter):
    
    startTime  = time.clock()
    startEpoch = time.time()
    startProcT = time.process_time()
    
    # read input string or filename from command line
    string, stringType = readString(parameter['standardInput'])
    if stringType == 'help':
        print(helpText(parameter))
        return 
    
    if not parameter['onyResultString']:
        print(string, stringType)
        print()
    
    # from input string, create list of Blocks and list of used letters
    # Reduction 1 included
    if stringType == 'String' or stringType == 'RandomString':
        blockList = blockInput(string, parameter)
    else:
        print("input Type not readable", file=stderr)
        return 
    
    
    if not parameter['onyResultString']:
        print("Number of possibilities if every letter must be used:", end = "")
        print(calculatePossibilities(getAlphabet(blockList), True))
        print("Number of possibilities if any letter may be used:", end = "")
        print(calculatePossibilities(getAlphabet(blockList), False))
    
    if parameter['printInputBlocks']:
        print(reportInputBlocks(blockList, parameter))
        
        
    # set output parameters    
    optimum = 0
    optima  = []
    maxima  = []
    recursions = []
    bifurcations = []
    leafes  = []
    compared = []
    constraints = []
    solutions = 1
    
    # Reduction 2a internal sublists
    if parameter['internalSublists']: 
        results = internalBlocks(blockList, parameter)
            
        # results is a tuple of results:
        optima.append(results[0])        # optimal lists
        maxima.append(results[1])        # maximal Value
        optimum += results[1]            # add maximal Value to total Value
        recursions  .append(results[2])  # number of recursions done
        bifurcations.append(results[3])  # number of bifurcations
        leafes      .append(results[4])  # number of maxima tested
        compared    .append(results[5])  # number of compared lists
        constraints .append(results[6])  # number of constraints in ILP
        solutions *= len(results[0])     # total number of solutions
        
        listOfBlockLists = [blockList]  # only one list-in-list
        
    else:    # to be replaced by else
    
        # Reduction 2:
        # consider independent sublists
        if parameter['independentSublists']: 
            listOfBlockLists = independendBlocks(blockList)
            
        else:   
            listOfBlockLists = [blockList]  # only one list-in-list
            
        if parameter['printIndependentSublists']:
            print(reportIndependentSublists(listOfBlockLists) )
        
        if parameter['printSubstringResults']: 
            print("\nOptimization: \n=============")
        
        for actualList in listOfBlockLists:
            
            # HERE IT HAPPENS!
            results = chooseMethod(actualList, parameter)
            
            # results is a tuple of results:
            optima.append(results[0])        # optimal lists
            maxima.append(results[1])        # maximal Value
            optimum += results[1]            # add maximal Value to total Value
            recursions  .append(results[2])  # number of recursions done
            bifurcations.append(results[3])  # number of bifurcations
            leafes      .append(results[4])  # number of maxima tested
            compared    .append(results[5])  # number of compared lists
            constraints .append(results[6])  # number of constraints in ILP
            solutions *= len(results[0])     # total number of solutions
    
            if parameter['printSubstringResults']: 
                print(reportSubstringResults(parameter, results))
        
    if parameter['printLongSummary']:
        print(reportLongSummary(parameter, blockList, optimum, optima, maxima,\
                    recursions, bifurcations, leafes, listOfBlockLists, compared, constraints) )
        
    if parameter['printShortSummary']:
        print(reportShortSummary(parameter, maxima, recursions, bifurcations, leafes,\
                                  compared, constraints) )
       
    print(reportResult(parameter, solutions, optimum, blockList, listOfBlockLists, optima, \
                       maxima, recursions, bifurcations, leafes, compared, constraints))
    
    if parameter['printRuntimes']:
        print("-------- system clock time: ", time.clock()        - startTime,  "seconds")
        print("--------      process time: ", time.process_time() - startProcT, "seconds")
        print("--------         real time: ", time.time()         - startEpoch, "seconds")
        
#    for a in getAlphabet(blockList): print(a, a.orderNumber)    # to control order number
        
    return results

# read string from file if string is a filename (has '.')
def readString(string):
    if string.isnumeric() and len(string) == 1:
        return randomString(int(string)), "RandomString"
    
    if string in ['-h', '-H', 'help']:
        return string, "help"
    
    if string.rfind(".") != -1:     # string is a filename
        inputString = ""
        with open(string, 'r') as readFile:
            lines = readFile.readlines()
        for line in lines:
            inputString = inputString + line.strip()  # removes whitespace
        return inputString, "String"
    else:
        return string, "String"

# generates a random string of length s² with s letters
def randomString(s):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    string = ""
    subalphabet = alphabet[0:s]
    random.seed(3)
    for i in range(s*s):
        string += random.choice(subalphabet)
    return string
    i = i   # avoids warning of unused variable i


#--------- --------- --------- --------- --------- ---------|--------- --------|
# program starts here
#parameter = takeParameter(argv) #sets standard parameters and names
#stringProcessor(parameter)
