from AlternatingOptimization import *

from HelperFunctions import *



'''
This file contains a testrun over all the functions that are defined within this project. 
'''


# start by defining global variables, properties of the circuit. 
# Where FSIZES has to match NQ and GATES
NQ = 20
GATES = 40
MMAX = 2
QMAX = 4
FSIZES = [4,4,4]

# showPlots indicates if plots should be displayed or not 
showPlots = True  
showAnimations = False

# create a random circuit with given properties 
# circuitOfQubits = random_circuit(NQ, GATES)

gatesList, commutationMatrix = CreateRandomCircuit(NQ, GATES, 2, display= False)
possibleArrangements = BFS([gatesList], commutationMatrix)


# if showPlots: 
#     show_circuit(NQ,circuitOfQubits)



# given this circuit, we aggregate the qubits in processing blocks. 
# Each processing block holds active qubits in processing zones and idle qubits in both processing and storage zones 
bestCircuit = DetermineBestArrangement(possibleArrangements, NQ, QMAX, MMAX)
processingBlockArrangement = blockProcessCircuit(bestCircuit, NQ, FSIZES, QMAX, MMAX)


if showPlots: 
    temporaryCost = computeTotalCost(computeArrangements(processingBlockArrangement, FSIZES, MMAX), NQ)
    visualize_blocks(processingBlockArrangement, 'Qubits arranged in processing blocks, cost: ' + str(temporaryCost))


'''
this arrangement can now be optimized using 
  1. deterministic optimiation 
  2. tabu sarch 
  3. alternating optimization
'''

# start with deterministic optimization 
processingBlockArrangementAfterDeterministicOptimization, processingBlockArrangementDisplaying = improvePlacement(processingBlockArrangement, NQ, FSIZES, QMAX, MMAX, True)

if showPlots: 
    temporaryCost = computeTotalCost(computeArrangements(processingBlockArrangementAfterDeterministicOptimization, FSIZES, MMAX), NQ)
    visualize_blocks(processingBlockArrangementAfterDeterministicOptimization, 'Processing block arrangement after deterministic optimization, cost: ' + str(temporaryCost))


if showAnimations: 
    animate_solving(processingBlockArrangementDisplaying, 'Animation of deterministic optimization')


# now, tabu search
processingBlockArrangementAfterTabuSearch, costProgressList, bestcostProgressList, globalCostNotImprovementCounter, numberOfImprovingSteps, numberOfTabuSteps, numberOfStepsWithoutUpdate, processingBlockArrangementDisplaying = improvePlacementTabuSearch(processingBlockArrangement, FSIZES, QMAX, MMAX, NQ, TSiterations=600, tabuListLength=30, swapNumMax=3, processingZoneSwapFraction=0, greedySpread=False, storeAllBestprocessingBlockArrangement=True, echo=True)

if showPlots: 
    temporaryCost = computeTotalCost(computeArrangements(processingBlockArrangementAfterTabuSearch, FSIZES, MMAX), NQ)
    visualize_blocks(processingBlockArrangementAfterTabuSearch, 'Processing block arrangement after tabu search, cost: ' + str(temporaryCost))

if showAnimations: 
    animate_solving(processingBlockArrangementDisplaying, 'Animation of optimization with tabu search')



# now, for the last step. The alternating optimization
processingBlockArrangementDisplaying ,b,c,numberOfTabuStepsList,costEvolution, processingBlockArrangementAfterAlternatingSearch = optimizeArrangements(processingBlockArrangement, NQ, FSIZES, QMAX, MMAX, numOptimizationSteps= 15, TSiterations= 10000, tabuListLength= 100, echo = True, visualOutput = False)

if showPlots: 
    temporaryCost = computeTotalCost(computeArrangements(processingBlockArrangementAfterAlternatingSearch, FSIZES, MMAX), NQ)
    visualize_blocks(processingBlockArrangementAfterAlternatingSearch, 'Processing block arrangement after tabu search, cost: ' + str(temporaryCost))


if showAnimations: 
    animate_solving(processingBlockArrangementDisplaying, 'Animation of optimization with tabu search')



plt.figure()
plt.plot(costEvolution, label = 'cost')
plt.title('Evolution of total cost with alternating iterations \n')
plt.xlabel('Iterations')
plt.ylabel('Cost')
plt.legend()
plt.show()

