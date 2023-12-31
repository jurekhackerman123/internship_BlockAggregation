from BlockAggregation import *

'''
In this file, the gatecoverage and thus, the cost of the inital arrangements is compared for the different commutations of the inital random circuit
that are allowed as calculated in the file RandomCircuitQiskit.py

Two things will be displayed: 
    The gatecoverage for the different arrangements 
    The cost of the resulting qubit arregations
'''


def CompareDifferentArrangements(possibleArrangements, show):

    if show: 
        ShowCommutationMatrix(commutationMatrix)

    if len(possibleArrangements) == 1: 
        # print('Only one variation found. No other arrangements due to commutation.')
        return [0, 1]

    # else: 
    #     print('Number of variations found: ', len(possibleArrangements))
    # 
    costList = []
    gateCoverageList = []
    for i in range(len(possibleArrangements)):
        tempCircuit = possibleArrangements[i]
        tempArrangement = blockProcessCircuit(tempCircuit, NQ, FSIZES, QMAX, MMAX)

        if show == True: 
            visualize_blocks(tempArrangement, 'Arrangement after Block Aggregation number ' + str(i))
        costList.append(computeTotalCost(computeArrangements(tempArrangement, FSIZES, MMAX), NQ))

        a, b, c, tempGateCoverage = AggregateBlocksStep(tempCircuit, NQ, QMAX, MMAX)
        gateCoverageList.append(tempGateCoverage)

        


    if show == True:
        plt.plot(costList)
        plt.xlabel('Commutation variation No.')
        plt.ylabel('Cost')
        plt.title('Cost over the different possible arrangements, max diff: ' + str(max(costList) - min(costList)))
        plt.show()

        plt.plot(gateCoverageList)
        plt.xlabel('Commutation variation No.')
        plt.ylabel('Gate Coverage')
        plt.title('Gate Coverage over different possible Arrangements')
        plt.show()

    # costlist[0] corresponds to the initial element that would have been chosen if no commutation had been considered
    return [max(costList) - costList[0], len(possibleArrangements)]




def CompareTest(possibleArrangements, desiredRange, show):
    '''
    Assume that we just have the one arrangement without commutation -
    What kind of variation do we have in the final cost after doing the blockaggregation a couple of times 
    Remember: There is randomness invlved in the Block Aggregation - the placement of the idle qubits. Thus, let's see      
    '''



    # else: 
    #     print('Number of variations found: ', len(possibleArrangements))
    # 
    costList = []

    tempCircuit = possibleArrangements[0]
    for i in range(desiredRange):
        tempArrangement = blockProcessCircuit(tempCircuit, NQ, FSIZES, QMAX, MMAX)

        costList.append(computeTotalCost(computeArrangements(tempArrangement, FSIZES, MMAX), NQ))

        


    if show == True:
        plt.plot(costList)
        plt.xlabel('Commutation variation No.')
        plt.ylabel('Cost')
        plt.title('Cost over the different possible arrangements, max diff: ' + str(max(costList) - min(costList)))
        plt.show()

    # costlist[0] corresponds to the initial element that would have been chosen if no commutation had been considered
    return [max(costList) - costList[0], len(possibleArrangements)]



def CalculatePossibleImprovement(numberOfIterations, all): 

    storingList = []
    gaugeStoringList = []

    for iteration in range(numberOfIterations): 
        if iteration % 10 == 0:
            print(iteration)

        gatesList, commutationMatrix = CreateRandomCircuit(NQ, GATES, 2, display= False)
        possibleArrangements = BFS([gatesList], commutationMatrix)

        tempResult = CompareDifferentArrangements(possibleArrangements, False)

        storingList.append( tempResult )
        gaugeStoringList.append(CompareTest(possibleArrangements, tempResult[1], False))

    if all == True: 
    # average improvement over iterations, considering all cases: 
        count = 0 
        for i in range(len(storingList)): 

            count += storingList[i][0]

        print('Average improvement for all:')
        print(count/len(storingList))

    else: 
        tabuList = []

        avgList = []
        avgGaugeList = []
        indexList = []

        indexCount = np.zeros(50)

        for i in range(len(storingList)): 
            
            # tempIndex is the length of the arrangement
            tempIndex = storingList[i][1]

            # we want to know the frequencies of the occurences of different ArrangementLenghts (only smaller 50 are of interest)
            if tempIndex < 50: 
                indexCount[tempIndex-1] += 1

            # if we saw this index before or the lenght of the arrangement is one (no commutation induced rearrangement possibilities)
            if tempIndex in tabuList or tempIndex == 1:
                if tempIndex == 1: 
                    indexCount[0] += 1
                continue

            tabuList.append(tempIndex)

            tempCount = 0
            tempSum = 0
            tempGaugeSum = 0


            for j in range(len(storingList)): 
                if storingList[j][1] == tempIndex: 
                    tempSum += storingList[j][0]

                    tempGaugeSum += gaugeStoringList[j][0]
                    tempCount += 1

            avgList.append(tempSum / tempCount)
            avgGaugeList.append(tempGaugeSum / tempCount)
            indexList.append(tempIndex)


            print('Average for possiblearrangements Length ', tempIndex, ' is ', tempSum / tempCount, '. \n Where the number of averages was ', tempCount)


        # bar plot for the frequencies
        xValues = np.arange(50)
        plt.bar(xValues, indexCount)
        plt.xlim(-1, 10.5)
        plt.title('Histogram')
        plt.ylabel('Frequency')
        plt.xlabel('Number of possible arrangements')
        plt.show()

        # print average possible cost improvement for the different iterations
        plt.title('Maximum possible cost improvement for variations')
        plt.scatter(indexList, avgList, label = 'With commutation')
        plt.scatter(indexList, avgGaugeList, label = 'Without commutation')
        plt.xlim(0,50)
        plt.xlabel('Numbers of possible arrangements')
        plt.ylabel('Maximum possible cost improvement')
        plt.legend()
        plt.show()



CalculatePossibleImprovement(1000, all = False)