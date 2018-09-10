# imports
import math
import matplotlib.pyplot as plt

import BRKGA as brkga # BRKGA framework (problem independent)
import decoder as decoder # Decoder algorithm (problem-dependent)
import data as data # Input data (problem-dependent and instance-dependent)
from configuration import config  # Configuration parameters (problem-dependent and execution-dependent)

# initializations
numIndividuals=int(config['numIndividuals'])
numElite=int(math.ceil(numIndividuals*config['eliteProp']))
numMutants=int(math.ceil(numIndividuals*config['mutantProp']))
numCrossover=max(numIndividuals-numElite-numMutants,0)
maxNumGen=int(config['maxNumGen'])
ro=float(config['inheritanceProb'])
evol=[]

# Main body
chrLength=decoder.getChromosomeLength(data)
population=brkga.initializePopulation(numIndividuals,chrLength)

i=0
while (i<maxNumGen):
    population = decoder.decode(population,data)
    evol.append(brkga.getBestFitness(population)['fitness'])
    print brkga.getBestFitness(population)['fitness']
    if numElite>0:
        elite, nonelite = brkga.classifyIndividuals(population,numElite)
    else:
        elite = []
        nonelite = population
    if numMutants>0: mutants = brkga.generateMutantIndividuals(numMutants,chrLength)
    else: mutants = []
    if numCrossover>0: crossover = brkga.doCrossover(elite,nonelite,ro,numCrossover)
    else: crossover=[]
    population=elite + crossover + mutants
    i+=1

population = decoder.decode(population, data)
bestIndividual = brkga.getBestFitness(population)

print bestIndividual['fitness']
print population
