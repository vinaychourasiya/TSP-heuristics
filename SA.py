import math
import random
import visualize_tsp
import networkx as nx
import matplotlib.pyplot as plt
from copy import copy
from twoOPT1 import TwoOPT


class SimAnneal(object):
    def __init__(self, coords,filename,T=-1, alpha=-1, stopping_T=-1, stopping_iter=-1):
        self.coords = coords
        self.N = len(coords)
        self.T = math.sqrt(self.N) if T == -1 else T
        self.T_save = self.T  # save inital T to reset if batch annealing is used
        #Decrease in temperature
        self.alpha = 0.8 if alpha == -1 else alpha
        #Stopping temperature
        self.stopping_temperature = 1e-8 if stopping_T == -1 else stopping_T
        #Stopping iteration count
        self.stopping_iter = 1000000 if stopping_iter == -1 else stopping_iter
        #Iteration number count
        self.iteration = 1

        #Index of nodes
        self.nodes = [(i+1) for i in range(self.N)]

        self.best_solution = None
        self.best_fitness = float("Inf")
        self.fitness_list = []
        self.filename = filename

    #Nearest neighbour start
    """def initial_solution(self):
        
        #Greedy algorithm to get an initial solution (closest-neighbour).
        
        cur_node = random.choice(self.nodes)  # start from a random node
        solution = [cur_node]

        # get nodes other than current node
        free_nodes = set(self.nodes)
        free_nodes.remove(cur_node)
        
        
        while free_nodes:
            #print(cur_node)
            min_ = 1000000
            for j in free_nodes:
                if (self.coords[cur_node-1,j-1]<min_):
                    min_ = self.coords[cur_node-1,j-1]
                    node = j
            free_nodes.remove(node)
            #print(free_nodes)
            solution.append(node)
            #print(solution)
            cur_node = node
            
            
        cur_fit = self.fitness(solution)
        if cur_fit < self.best_fitness:  # If best found so far, update best fitness
            self.best_fitness = cur_fit
            self.best_solution = solution
        self.fitness_list.append(cur_fit)
        return solution, cur_fit"""
    #Nearest neighbour end
       
    #Random allocation
    """def initial_solution(self):
        solution = copy(self.nodes)
        random.shuffle(solution)
        
        cur_fit = self.fitness(solution)
        if cur_fit < self.best_fitness:  # If best found so far, update best fitness
            self.best_fitness = cur_fit
            self.best_solution = solution
        self.fitness_list.append(cur_fit)
        return (solution, cur_fit)"""
    #Random alloc
    def initial_solution(self):
        L = TwoOPT(self.filename)
        cur_fit, solution = L.run()
        return (solution, cur_fit)
        

    
    
    def fitness(self, solution):
        
        #Total distance of the current solution path.
        
        cur_fit = 0
        for i in range(self.N - 1):
            #print(solution[i],solution[i+1])
            cur_fit += self.coords[solution[i]-1,solution[i+1]-1]
        #print(solution[i+1],solution[0])
        # Add the cost from last node back to initial node
        cur_fit += self.coords[solution[i+1]-1,solution[0]-1]
        return cur_fit

    def p_accept(self, candidate_fitness):
        
        #Probability of accepting if the candidate is worse than current.
        #Depends on the current temperature and difference between candidate and current.
        
        return 1/(1 + math.exp(-abs(candidate_fitness - self.cur_fitness) / self.T))

    def accept(self, candidate):
        
        #Accept with probability 1 if candidate is better than current.
        #Accept with probabilty p_accept(..) if candidate is worse.
        
        candidate_fitness = self.fitness(candidate)
        if candidate_fitness < self.cur_fitness:
            self.cur_fitness, self.cur_solution = candidate_fitness, candidate
            if candidate_fitness < self.best_fitness:
                self.best_fitness, self.best_solution = candidate_fitness, candidate
        else:
            if random.random() > self.p_accept(candidate_fitness):
                self.cur_fitness, self.cur_solution = candidate_fitness, candidate

    def Swap(self, tour, x, y):
        """
            tour : Given TSP tour
            x = swappping First index in tour 
            y = swappping last index in tour
            return : new_tour with perfomming swapping 
            note: x and y should be index only (in tour) not exact city number
        """
        new_tour = tour[:x] + [*reversed(tour[x:y + 1])] + tour[y + 1:]
        return new_tour
    
    def _optimize(self, initial_tour):
        """
            Improve existing tour 
            using 2-opt method
        """
        minchange = -1
        tour = initial_tour
        while minchange < 0:
            minchange = 0
            for i in range(self.N - 3):
                for j in range(i + 2, self.N - 1):
                    t1 = tour[i]
                    t2 = tour[i + 1]
                    t3 = tour[j]
                    t4 = tour[j + 1]

                    change = (self.coords[t1 - 1][t3 - 1] +
                              self.coords[t2 - 1][t4 - 1] -
                              self.coords[t1 - 1][t2 - 1] -
                              self.coords[t3 - 1][t4 - 1])
                    if change < minchange:
                        minchange = change
                        tour = self.Swap(tour, i + 1, j)
        return tour
    
    def anneal(self):
        
        #Execute simulated annealing algorithm.
        
        # Initialize with the greedy solution.
        # Get value for current solution and fittness from greedy algo
        
        self.cur_solution, self.cur_fitness = self.initial_solution()

        print("Starting annealing.")
        while self.T >= self.stopping_temperature and self.iteration < self.stopping_iter:
            candidate = list(self.cur_solution)
            
            #get a random no. from 2 to N-1(index of last node), both included
            # This number of values to be reversed
            l = random.randint(2, self.N - 1)
            #This is the index from where reversing starts i.e. 
            # from 0 N- l as l after values will be reversed
            i = random.randint(0, self.N - l)
            
            # Reverse the value of list from index i to i+l-1
            candidate[i : (i + l)] = reversed(candidate[i : (i + l)])
            #candidate = self._optimize(candidate)
            self.accept(candidate)
            self.T *= self.alpha
            self.iteration += 1

            self.fitness_list.append(self.cur_fitness)
        
        candidate = self._optimize(candidate)
        self.accept(candidate)
        print(self.best_solution)
        print("Best fitness obtained: ", self.best_fitness)
        improvement = 100 * (self.fitness_list[0] - self.best_fitness) / (self.fitness_list[0])
        print(f"Improvement over random allocation: {improvement : .2f}%")
        print(self.iteration)

    def batch_anneal(self, times=5):
        
        #Execute simulated annealing algorithm `times` times, with random initial solutions.
        for i in range(1, times + 1):
            print(f"Iteration {i}/{times} -------------------------------")
            self.T = self.T_save
            self.iteration = 1
            self.cur_solution, self.cur_fitness = self.initial_solution()
            self.anneal()

    def visualize_routes(self):
        
        #Visualize the TSP route with matplotlib.
        G = nx.Graph()
        G.add_edges_from(self.best_solution)
        nx.draw(G,with_labels=True, nodecolor='r', edge_color='b')
        plt.show()

    def plot_learning(self):
        
        #Plot the fitness through iterations.
        
        plt.plot([i for i in range(len(self.fitness_list))], self.fitness_list)
        plt.ylabel("Fitness")
        plt.xlabel("Iteration")
        plt.show()
