## Institut für Informatik, 
## Department of Algorithmische Bioinformatik
## Heinrich Heine Univversity Düsseldorf, Germany
## written by: Michael Wulfert
#--------- --------- --------- --------- --------- ---------|--------- --------|
# parameter for the string processor 'gbr' to control:

# input,
# different reductions
# outputs

def getParameter():
    
    # create dictionary with standard parameter
    parameter = setParameter()
    
    # read parameter file
    parameter = readParameterFile(parameter)
    
    if parameter['onyResultString']:
        noOutputs(parameter)
    
    return parameter

def setParameter():    
    # short names of algorithms
    global algorithms
    
    parameter = {}     #empty dictionary
    
    # file name of parameter file
    parameter.update(parameterFile = './src/parameter.prm')
    
# Input
    
    # standard input if no argument is given
#    inputString = "TestSeqShort.seq"
    inputString = "TestSeq.seq"    # may be commented out
    parameter.update(standardInput = inputString)
    
    # result has all optimal strings or only one
    parameter.update(showAllOptima = True)
    
    # result must have every letter
    parameter.update(everyLetterExists = False)
    
    
    # methods:
    tree = 'tree'   # binary decision tree
    walk = 'walk'   # random walk through tree
    wide = 'wide'   # wide decision tree
    dag  = 'dag'    # directed acyclic graph, ideal for small alphabets
    ilp  = 'ilp'    # Integer Linear Programming, uses pulp
    parameter.update(method = 'tree')
    
    algorithms = (dag, ilp)
    
# Reductions

    # Reduction 1
    # group blocks of identical letters
    parameter.update(blockIdenticalLetters = True)
    
    # Reduction 2:
    # consider independent sublists
    parameter.update(independentSublists = True)

    # Reduction 2a: stronger than reduction 2
    # consider internal sublists
    parameter.update(internalSublists = True)
    
    # Reduction 3:
    # break iteration branch if maximum is not longer reachable
    parameter.update(breakIfTooSmall = True)
    
    # Reduction 4:
    # break iteration branch if maximum is not longer reachable
    parameter.update(tooManyToReject = True)
    
    # Reduction 5:
    # take only 'new' letters - avoids leading blocks of same letter missing
    parameter.update(takeOnlyNewLetters = True)
    
    # Reduction 6:
    # take contiguous unique blocks together
    parameter.update(uniquesTogether = True)
    
    # Reduction 7:
    # no more letters left
    parameter.update(noMoreLetters = True)
    
    
    # Reduction 8:
    # take last possible letter
    parameter.update(takeLastLetter = True)
    
    
    # Reduction 9:
    # minimum of letters to reject in the remaining string
    parameter.update(minToReject = True)
    
    
    
    
    # Heuristic 1:
    # remove some small blocks
    # (not yet implemented)
    
    
    # Heuristics 2 (only for tree):
    # If bifurcation possible: choose one randomly
    parameter.update(randomTreeWalk = False)
    parameter.update(randomTreeRepeats = 10000)
    parameter.update(randomTreeProbability = 0.5)
    
    
# Outputs:

    parameter.update(onyResultString     = False)

    # print sublists
    parameter.update(printSublist        = False)
    parameter.update(reportPossibilities = True)
    parameter.update(printMethod         = True)

    # tree: recursion steps: no False after True!
    parameter.update(printRecursionSteps = False)
    parameter.update(printRecursionBreak = True)
    parameter.update(printRecursionStop  = False)
    # for walk histograms:
    parameter.update(countStringLengths  = False)
    
    # ILP:
    parameter.update(printILPsteps     = False)
    parameter.update(printILPequations = False)
    parameter.update(printILPresults   = False)
    
    #DAG
    parameter.update(printNewListLetter     = True)
    parameter.update(printLetterLists       = False)
    parameter.update(printLetterComparisons = False)
    parameter.update(printNewMaxima         = False)
    parameter.update(printDAG               = True)
    #dag - debug
    #parameter.update(pointerPosResetExit    = False)
    
    
    # results
    parameter.update(printInputBlocks          = True)
    parameter.update(printIndependentSublists  = False)
    parameter.update(printSubstringResults     = False)
    parameter.update(printLongSummary          = True)
    parameter.update(printShortSummary         = True)
    parameter.update(printResultList           = True)
    parameter.update(printRuntimes             = False)
    
# Return
    
    return parameter

def noOutputs(parameter):   # Avoids all outputs

    # print sublists
    parameter['printSublist']           = False
    parameter['reportPossibilities']    = False
    parameter['printMethod']            = False

    # tree: recursion steps: no False after True!
    parameter['printRecursionSteps']    = False
    parameter['printRecursionBreak']    = False
    parameter['printRecursionStop']     = False
    # for walk histograms:
    parameter['countStringLengths']     = False
    # ILP:
    parameter['printILPsteps']          = False
    parameter['printILPequations']      = False
    parameter['printILPresults']        = False
    
    #DAG
    parameter['printNewListLetter']     = False
    parameter['printLetterLists']       = False
    parameter['printLetterComparisons'] = False
    parameter['printNewMaxima']         = False
    parameter['printDAG']               = False
    #dag - debug
    #parameter['pointerPosResetExit    = False)
    
    
    # results
    parameter['printInputBlocks']       = False
    parameter['printIndependentSublists']= False
    parameter['printSubstringResults']  = False
    parameter['printLongSummary']       = False
    parameter['printShortSummary']      = False
    parameter['printResultList']        = True  # result output
    parameter['printRuntimes']          = False
    
    return parameter

    
def getAlgorithms():
    # short names of algorithms
    global algorithms 
    return  algorithms


def takeParameter(args):
    # short names of algorithms
    global algorithms 
    
    parameter = getParameter()
    if len(args) > 1:
        parameter['standardInput'] = args[1]
    if len(args) > 2:
        if args[2] in algorithms:
            parameter['method'] = args[2]
        else:
            print('method', args[2], 'is unknown, ' + parameter['method'] + ' used instead')
    return parameter

def readParameterFile(parameter):
    # read file 'parameterFile'
    with open(parameter['parameterFile'], 'r') as readFile:
        lines = readFile.readlines()
    for line in lines:
        line.strip()    # removes whitespaces
        if len(line) > 0 and line[0] in "#%/ ": # comment lines
            continue
        try:
            name, value = line.split('=')
        #    print("parameter:", name, "value:", value)
            name  = name.strip()
            value = value.strip()
            if not name in ('standardInput', 'method'): # don't convert strings
                value = eval(value)
            parameter[name]=value
        except:
            pass
        #    print(line + " is not a valid parameter assignment")
    return parameter
