from GeneticAlgorithmFunctions import *
from AlternatingOptimization import * 

'''
This file is responsible for running a Genetic algorithm to unclutter a graph. 

populationsize seems to have a huge impact!!!


COMBINE GA WITH TABUSEARCH OR SO 

Add tournamentselection for more individuals!!

'''

# global variables for GA
NUMBEROFGENERATIONS = 1000
POPULATIONSIZE = 300

# these should be fine
CROSSOVERPROB = 0.8
MUTATIONPROB = 0.025

TOURNAMENTPROB = 0.75
TOURNAMENTSIZE = 2

# global variables for Block aggregation
NQ = 20
GATES = 40
MMAX = 2
QMAX = 4
FSIZES = [4,4,4]

# initiate circuit
circuitOfQubits = random_circuit(NQ, GATES)


# alpha is the variable that somehow controls explorations vs. exploitation 
alpha = 1


# 
# INITIALIZE POPULATION - a list of aggregated processing blocks 
# 
population = InitializePopulation(POPULATIONSIZE, NQ, GATES, FSIZES, QMAX, MMAX, False)

costList = []

print('Populationsize:')
print(np.shape(population))

maximumGlobalFitness = 0



for iGeneration in range(NUMBEROFGENERATIONS): 

    # evaluate individuals and keep a list 
    fitnessList = np.zeros(POPULATIONSIZE)

    maximumFitness = 0 

    # evaluate individuals 
    for jIndividual in range(POPULATIONSIZE):

        tempBrocessingBlockArrangement = population[jIndividual]

        costForThisIndividual = computeTotalCost(computeArrangements(tempBrocessingBlockArrangement, FSIZES, MMAX), NQ)

        fitnessList[jIndividual] = 1/costForThisIndividual
        if fitnessList[jIndividual] > maximumFitness: 
            maximumFitness = fitnessList[jIndividual]
            bestIndividual = jIndividual 
            if iGeneration == 0: 
                bestIndividual1stGen = []
                bestIndividual1stGen.append(bestIndividual)

        if fitnessList[jIndividual] > maximumGlobalFitness: 
            maximumGlobalFitness = fitnessList[jIndividual]
            bestGlobalIndividual = jIndividual


    # proceed with evolution
    tempPopulation = population

    # print(fitnessList)

    # iterate over population, only taking into account every second individual 
    for jIndividual in range(0, POPULATIONSIZE, 2):

        # 
        # TOURNAMENTSELECTION
        # 

        individualOneIndex = TournamentSelection(fitnessList, TOURNAMENTPROB, TOURNAMENTSIZE)
        individualTwoIndex = TournamentSelection(fitnessList, TOURNAMENTPROB, TOURNAMENTSIZE)
        
        randomNumber = random.random()

        # 
        # CROSSOVER
        # 

        individualOne = population[individualOneIndex]
        individualTwo = population[individualTwoIndex]

        if randomNumber < CROSSOVERPROB and alpha > 0.5: 
            
            newIndividualOne, newIndividualTwo = CrossOver(individualOne, individualTwo)

            tempPopulation[jIndividual] = newIndividualOne
            tempPopulation[jIndividual+1] = newIndividualTwo

        else: 
            tempPopulation[jIndividual] = individualOne
            tempPopulation[jIndividual+1] = individualTwo


    # elitism 
    tempPopulation[0] = population[bestIndividual]

    # 
    # MUTATION
    # 
    for jIndividual in range(POPULATIONSIZE):
        tempIndividual = Mutation(tempPopulation[jIndividual], MUTATIONPROB, alpha)
        tempPopulation[jIndividual] = tempIndividual
    

    # update alpha
    alpha *= 0.99

    # update population
    population = tempPopulation

    # exit()
    if iGeneration %100 == 0: 
        print('Best individual: ')
        print(computeTotalCost(computeArrangements(population[bestIndividual], FSIZES, MMAX), NQ))
    costList.append(computeTotalCost(computeArrangements(population[bestIndividual], FSIZES, MMAX), NQ))


plt.title('Developement of the cost with generations. populationsize: ' + str(POPULATIONSIZE))
plt.xlabel('Generations')
plt.ylabel('Cost')
plt.plot(costList)
plt.show()

# visualize_blocks(population[bestIndividual1stGen[0]], 'Before genetic algorithm, cost: ' + str(computeTotalCost(computeArrangements(population[bestIndividual1stGen[0]], FSIZES, MMAX), NQ)))
visualize_blocks(population[bestGlobalIndividual], 'After genetic algorithm, cost: ' + str(computeTotalCost(computeArrangements(population[bestGlobalIndividual], FSIZES, MMAX), NQ)))