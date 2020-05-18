## Institut für Informatik, 
## Department of Algorithmische Bioinformatik
## Heinrich Heine Univversity Düsseldorf, Germany
## written by: Michael Wulfert
#--------- --------- --------- --------- --------- ---------|--------- --------|
# methods for 'ilp' algorithm: Integer Linear Programming

from pulp import * 
from src.letterObject import getAlphabet
from src.blockObject import sumValues, reportAllLists, reportCharacterList, getLowerLimit
#from blockRecursion # kann nicht rekursiv importiert werden!

def ilpStart(givenBlockList, givenParameter):
    # constant Values as globals:
    global subBlockList, lenBlockList, totalLength, parameter
    # common values as globals:
    global optimalLists, maxValue
    
    #print("used method: ILP = integer linear programming")
    
    # set constants
    subBlockList = givenBlockList    
    lenBlockList = len(subBlockList) 
    totalLength  = sumValues(subBlockList)     
    parameter = givenParameter
    
    if parameter['printMethod']: print("used method: ILP = integer linear programming")
    
    parameter['showAllOptima'] = False  # didn't work with ILP
    
    # set start values    
    optimalLists = []
    maxValue = getLowerLimit(subBlockList, parameter)  # sum of maxima of each letter in blockList
    constraints = 0
    
    if parameter['printSublist']: print(reportSublistData() )
    
    
    # HERE IT HAPPENS...
    
    
    # name of the ILP:
    prob = LpProblem("stringPartition", LpMaximize)
    
    # Variables x[i] and Weights v[i]
    x = []  # variables
    v = []  # weights/values
    n = []  # names
    b = []  # blocks
    for i, block in enumerate(subBlockList):
        x.append(LpVariable("x"+str(i), 0, 1, LpInteger) )
#        x.append(LpVariable(block.getLongBlock(), 0, 1, LpInteger) )
        v.append(block.getBlockValue())
        n.append(block.getLongBlock())
        b.append(block)
    if parameter['printILPsteps']: print("ILP -> x:", x, " - v:", v)
        
    # Maximizing
    prob += sum(x[i]*v[i] for i in range(lenBlockList) )#, "to maximize"
    
#    maxi = ""   # maximize
#    for i, block in enumerate(subBlockList):
#        maxi += x[i]*v[i]       
    #    print("ILP -> x[i]:", x[i], "v[i]:", v[i], "maxi:", maxi)
        
#    prob += maxi, "to maximize" 
#    print("ILP -> to maximize:", maxi, "\n")
#    print("ILP -> prob without constraints:", prob)

        
    # constraints
    offset = subBlockList[0].getBlockNumber()    
    for i, block in enumerate(subBlockList):
        z = [1 for j in range(lenBlockList)]    # array: [1, 1, ...1]
        lastSameBlock = block.getLastSameBlock()
        # take all previous blocks of same letters in reverse order:
        while lastSameBlock != None:
            if parameter['printILPsteps']: 
                print("ILP -> last same block:", lastSameBlock, "block number", lastSameBlock.getBlockNumber() )
            firstBlocksNumber = lastSameBlock.getBlockNumber() - offset
            lastBlocksNumber = block.getBlockNumber() - offset
            blocksBetween = lastBlocksNumber - firstBlocksNumber -1
            if parameter['printILPsteps']: 
                print("ILP -> firstBlocksNumber:", firstBlocksNumber, "lastBlocksNumber:", lastBlocksNumber, "width:", blocksBetween)
            
            if blocksBetween > 0:
            #    print(          (x, z, firstBlocksNumber, lastBlocksNumber, lenBlockList))
            #    print(constraint(x, z, firstBlocksNumber, lastBlocksNumber, lenBlockList))
                prob += constraint(x, z, firstBlocksNumber, lastBlocksNumber, lenBlockList)
                constraints += 1
                
                # Reduction 5:
                if parameter['takeOnlyNewLetters']:
                    #print(constraint2(x, z, firstBlocksNumber, lastBlocksNumber, lenBlockList))
                    if constraint2(x, z, firstBlocksNumber, lastBlocksNumber, lenBlockList) != None:
                        prob += constraint2(x, z, firstBlocksNumber, lastBlocksNumber, lenBlockList)
                    constraints += 1
                    
            
            z[lastSameBlock.getBlockNumber() - offset] = 0  # don't calculate inner letters
            lastSameBlock = lastSameBlock.getLastSameBlock()
        
        # Reduction 6: uniques together    
        if parameter['uniquesTogether']:
            if i > 0 and subBlockList[i-1].isUnique() and block.isUnique():
                prob += x[i-1] - x[i] == 0, "unique blocks " + str(i-1) + " and " + str(i) + " together"
                constraints += 1
            

    if parameter['everyLetterExists']:
        alphabet = getAlphabet(subBlockList)

        for letter in alphabet:
            y = [0 for j in range(lenBlockList)]
            actualBlock = letter.getLastSameBlock()
            while actualBlock != None:
                y[actualBlock.getBlockNumber() - offset] = 1
                actualBlock = actualBlock.getLastSameBlock()
            if parameter['printILPsteps']: print("ILP -> letter:", letter, "y:", y)
            cString = "Constraint use letter " + str(letter) 
            prob += sum(x[j] * y[j] for j in range(lenBlockList)) >= 1, cString
            constraints += 1
            
            
        
    #print("ILP -> full prob:", prob)
    if parameter['printILPequations']: 
        print("ILP -> prob is:")
        print(prob)
    
    if not parameter['onyResultString']:    
        print(constraints, "constraints")
    
    # save
    prob.writeLP("stringPartition.LP")
    
    # solve
    prob.solve()
    
    # result status:
   
    if parameter['printILPresults']: print("Status:", LpStatus[prob.status], prob.status)
    
    # optimized variables:
    if parameter['printILPresults']: 
        #print(prob.variables() )
        for variables in prob.variables():
            print(variables.name, "=", variables.varValue)
        
    # result:
    if parameter['printILPresults']: print("maximum:", value(prob.objective))
    maxValue = int(value(prob.objective))   # here only int
    
    resultString = ""
    optimalList = []
    if parameter['printILPresults']: print(x)
    for i in range(len(x)):
        if value(x[i]) == 1:
            resultString += n[i]
            optimalList.append(b[i])
    if parameter['printILPresults']: print(resultString)
#    print(optimalList)
    optimalLists = [optimalList]
    
    if parameter['printSublist']: print(reportOptimalSublists() )
    
    return optimalLists, maxValue, 0, 0, 0, 0, constraints

def constraint(x, z, oldBlock, newBlock, lenBlockList):
    y = [0 for j in range(lenBlockList)]
    blocksBetween = newBlock - oldBlock - 1
#    print("blocks between (old):", blocksBetween)
    blocksBetween -= lenBlockList - sum(z)  # corrects for same letters between
#    print("blocks between (z..):", blocksBetween)
    if blocksBetween > 0 or True:   #is called only if blocksBetween > 0
        y[oldBlock] = blocksBetween
        y[newBlock] = blocksBetween
        for j in range(oldBlock+1, newBlock):
            y[j] = 1
            if parameter['printILPsteps']: print(j, end = "; ")
        if parameter['printILPsteps']: 
            print("-> from", oldBlock+1, "to", newBlock-1, "with", blocksBetween, "blocks between")
            print(y)
        cString = "Constraint blocks " + str(oldBlock) + " to " + str(newBlock)
        #print(cString)
        return sum(x[j] * y[j] * z[j] for j in range(lenBlockList)) <= 2*blocksBetween, cString
    
# take all letters of the same type between 
def constraint2(x, z, firstBlock, lastBlock, lenBlockList):
    y = [0 for j in range(lenBlockList)]
#    blocksBetween = lastBlock - firstBlock - 1
    blocksBetween = lenBlockList - sum(z)  # corrects for same letters between
    if blocksBetween > 0 or True:
        y[firstBlock] = blocksBetween
        y[lastBlock]  = blocksBetween
        for j in range(firstBlock+1, lastBlock):
            y[j] = z[j]-1
            if parameter['printILPsteps']: print(j, end = "; ")
        if parameter['printILPsteps']: 
            print("-> from", firstBlock+1, "to", lastBlock-1, "with", blocksBetween, "same blocks between")
            print(y)
        cString = "Constraint same blocks " + str(firstBlock) + " to " + str(lastBlock)
        #print(cString)
        return sum(x[j] * (y[j])  for j in range(lenBlockList)) <= 1*blocksBetween, cString



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


