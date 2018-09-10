import numpy as np
import data as data

'''
Authors: Jerome Pasvantis and Kymry Burwell

Instructions for use - Simply update the 'import data' to the correct file\dataset and run
Dataset format is as follows:
nNurses = 100
hours =  24
demand = [ 18,19,17,18,20,21,23,24,24,28,32,32,33,30,29,28,27,26,25,20,18,18,18,19 ]
minHours = 4
maxHours = 10
maxConsec = 5
maxPresence = 13
'''

# Generate chromosome length
def getChromosomeLength(data):
    return data.nNurses

# Iterates through each individual in the population
def decode(population, data):
    for ind in population:
        solution, fitness=decoder_assignment(data,ind['chr'])
        ind['solution']=solution
        ind['fitness']=fitness
    return(population)

# Decoder - Adds hours to nurses and generates solution (adheres to all problem constraints)
def decoder_assignment(data, chromosome):
    nurses = list([]) # Create empty list for working nurses
    demand = list(data.demand)
    # Iterate through each gene in Chromosome until demand is met
    for index, i in enumerate(chromosome):
        if demandMet(demand):
            solution,fitness = generateSolution(nurses)
            return solution, fitness
        startHour = int(i)
        currentHour = startHour
        nurse = Nurse(index)
        if startHour % 2 == 0: # Sets working direction
            backwards = False
        else:
            backwards = True
        nurses.append(nurse) # Adds nurse to current solution
        maxPresence = data.maxPresence
        maxConsec = data.maxConsec
        consec = 0
        #Adds hours to current nurse - max hours, min hours, max consecutive, and max presence constraints ensured
        while maxPresence > 0 and sum(nurse.hours) < data.maxHours:
            maxPresence -=  1
            if consec < maxConsec:
                nurse.hours[currentHour] = 1
                consec += 1
                demand[currentHour] -= 1
            else: consec = 0
            if currentHour == data.hours - 1:
                currentHour = startHour - 1
                backwards = True
                consec = min(maxConsec,data.hours-startHour)
            elif currentHour == 0:
                currentHour = startHour + 1
                backwards = False
                consec = min(maxConsec,startHour)
            else:
                if backwards: currentHour -= 1
                else: currentHour += 1
    return None, 99999

# Check if demand is met
def demandMet(demand):
    met = True
    for i in demand:
        if i > 0:
            met = False
    return met

# Generate solution
def generateSolution(nurses):
    fitness = len(nurses)
    solution = list([])
    for n in nurses:
        solution.append((n.name,n.hours))
    return solution, fitness

# Nurse data structure
class Nurse:
    def __init__(self,number):
        self.name = number
        self.hours = [0 for i in range(data.hours)]
