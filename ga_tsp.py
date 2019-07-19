import numpy as np, random, operator, pandas as pd, matplotlib.pyplot as plt
from readData import ReadData

class City:
    def __init__(self, label, distance_list):
        self.label = label
        self.distance_list = distance_list
    
    def distance(self, city):
        distance = self.distance_list[(city.label)-1]
        return distance
    
    def __repr__(self):
        return "[" +str(self.label) + "]"

class Fitness:
    def __init__(self, route):
        self.route = route
        self.distance = 0
        self.fitness= 0.0
    
    def routeDistance(self):
        if self.distance ==0:
            pathDistance = 0
            for i in range(0, len(self.route)):
                fromCity = self.route[i]
                toCity = None
                if i + 1 < len(self.route):
                    toCity = self.route[i + 1]
                else:
                    toCity = self.route[0]
                pathDistance += fromCity.distance(toCity)
            self.distance = pathDistance
        return self.distance
    
    def routeFitness(self):
        if self.fitness == 0:
            self.fitness = 1 / float(self.routeDistance())
        return self.fitness

def createRoute(cityList):
    route = random.sample(cityList, len(cityList))
    return route

def initialPopulation(popSize, cityList):
    population = []

    for i in range(0, popSize):
        population.append(createRoute(cityList))
    return population

def rankRoutes(population):
    fitnessResults = {}
    for i in range(0,len(population)):
        fitnessResults[i] = Fitness(population[i]).routeFitness()
    return sorted(fitnessResults.items(), key = operator.itemgetter(1), reverse = True)

def selection(popRanked, eliteSize):
    selectionResults = []
    df = pd.DataFrame(np.array(popRanked), columns=["Index","Fitness"])
    df['cum_sum'] = df.Fitness.cumsum()
    df['cum_perc'] = 100*df.cum_sum/df.Fitness.sum()
    
    for i in range(0, eliteSize):
        selectionResults.append(popRanked[i][0])
    for i in range(0, len(popRanked) - eliteSize):
        pick = 100*random.random()
        for i in range(0, len(popRanked)):
            if pick <= df.iat[i,3]:
                selectionResults.append(popRanked[i][0])
                break
    return selectionResults

def matingPool(population, selectionResults):
    matingpool = []
    for i in range(0, len(selectionResults)):
        index = selectionResults[i]
        matingpool.append(population[index])
    return matingpool

def breed(parent1, parent2):
    child = []
    childP1 = []
    childP2 = []
    
    geneA = int(random.random() * len(parent1))
    geneB = int(random.random() * len(parent1))
    
    startGene = min(geneA, geneB)
    endGene = max(geneA, geneB)

    for i in range(startGene, endGene):
        childP1.append(parent1[i])
        
    childP2 = [item for item in parent2 if item not in childP1]

    #child = childP1 + childP2
    j=0
    for i in range(0, len(parent1)):
        if(i < startGene):
            child.append(childP2[i])
            j = j + 1
        elif(i < endGene):
            child.append(childP1[i-startGene])
        else:
            child.append(childP2[j])
            j = j + 1
    return child

def breedPopulation(matingpool, eliteSize):
    children = []
    length = len(matingpool) - eliteSize
    pool = random.sample(matingpool, len(matingpool))

    for i in range(0,eliteSize):
        children.append(matingpool[i])
    
    for i in range(0, length):
        child = breed(pool[i], pool[len(matingpool)-i-1])
        children.append(child)
    return children

def mutate(individual, mutationRate):
    for swapped in range(len(individual)):
        if(random.random() < mutationRate):
            swapWith = int(random.random() * len(individual))
            
            city1 = individual[swapped]
            city2 = individual[swapWith]
            
            individual[swapped] = city2
            individual[swapWith] = city1
    return individual

def mutatePopulation(population, mutationRate):
    mutatedPop = []
    
    for ind in range(0, len(population)):
        mutatedInd = mutate(population[ind], mutationRate)
        mutatedPop.append(mutatedInd)
    return mutatedPop

def nextGeneration(currentGen, eliteSize, mutationRate):
    popRanked = rankRoutes(currentGen)
    selectionResults = selection(popRanked, eliteSize)
    matingpool = matingPool(currentGen, selectionResults)
    children = breedPopulation(matingpool, eliteSize)
    nextGeneration = mutatePopulation(children, mutationRate)
    return nextGeneration

   # nextGeneration = mutatePopulation(children, mutationRate)

def geneticAlgorithm(population, popSize, eliteSize, mutationRate, generations):
    pop = initialPopulation(popSize, population)
    print("Initial distance: " + str(1 / rankRoutes(pop)[0][1]))
    
    for i in range(0, generations):
        pop = nextGeneration(pop, eliteSize, mutationRate)
    
    print("Final distance: " + str(1 / rankRoutes(pop)[0][1]))
    bestRouteIndex = rankRoutes(pop)[0][0]
    bestRoute = pop[bestRouteIndex]
    return bestRoute

# dist_matrix = [[0 for x in range(size)] for y in range(size)]
# for i in range(size-1):
#     for j in range(i+1,size):
#         dist_matrix[i][j] = int(random.random() * 200)
# for i in range(1,size):
#     for j in range(i):
#         dist_matrix[i][j] = dist_matrix[j][i]
#print(dist_matrix)

 
#geneticAlgorithm(population=cityList, popSize=100, eliteSize=20, mutationRate=0.01, generations=500)

def geneticAlgorithmPlot(population, popSize, eliteSize, mutationRate, generations):
    pop = initialPopulation(popSize, population)
    progress = []
    progress_min = []
    progress.append(1 / rankRoutes(pop)[0][1])
    min_dist = 0
    bestRoute = []
    c = 0
    for i in range(0, generations):
        pop = nextGeneration(pop, eliteSize, mutationRate)
        dist = 1 / rankRoutes(pop)[0][1]
        if(i == 0):
            min_dist = 1 / rankRoutes(pop)[0][1]
            bestRouteIndex = rankRoutes(pop)[0][0]
            bestRoute = pop[bestRouteIndex]
        else:
            if(min_dist > dist):
                min_dist = 1 / rankRoutes(pop)[0][1]
                bestRouteIndex = rankRoutes(pop)[0][0]
                bestRoute = pop[bestRouteIndex]
                c = 0
        c = c+1
        progress.append(dist)
        progress_min.append(min_dist)
        print("Generation : " + str(i)+ " Distance : " + str(dist) + " Minimum Distance : " + str(min_dist))
        if (c > generations/10):
            print("break at generation :",i)
            break
    plt.suptitle('Genetic Algorithm for ch150.tsp')
    plt.subplot(211)
    plt.plot(progress)
    plt.ylabel('Distance')
    plt.xlabel('Generation')
    plt.subplot(212)
    plt.plot(progress_min)
    plt.ylabel('Minimum Distance')
    plt.xlabel('Generation')
    plt.show()
    print("Minimum distance :",min_dist)
    print("Best route :", bestRoute)
   
   

#INPUT

import sys 
if len(sys.argv)<2:
	print("need inpute file")
	sys.exit(1)
r = ReadData(sys.argv[1])
print(r.size)
size = r.size
dist_matrix = r.GetDistanceMat()
cityList = []
for i in range(size):
    cityList.append(City(label = i+1, distance_list = dist_matrix[i]))
geneticAlgorithmPlot(population=cityList, popSize=500, eliteSize=100, mutationRate=0.01, generations=100)

