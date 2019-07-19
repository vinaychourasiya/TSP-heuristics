# coding: utf-8
# Author: Vinay Chourasiya

import time
start_time = time.time()
from readData import ReadData
import numpy as np
import sys 

class TwoOPT:
    """
    2-opt:
          Generate intial tour
          and improve it by deleting 1 one edges
          and change with other
    -- It gives nearly optimal tour    
    """

    def __init__(self, file):
        """
            Intialize: Instaces file,
                       Distance Matrix,
                       and size
        """
        self.file = file
        self.instance = ReadData(self.file)
        self.size = self.instance.size
        self.dis_mat = self.instance.GetDistanceMat()
        self.time_read = self.instance.time_to_read
        self.time_algo = 0

    def get_initial_tour(self):
        """
        Return: intial tour
        """
        return [*range(1, self.size + 1)]

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

    def get_distance(self, tour):
        """
        Given any tour it return total distance of
        given tour
        dis_mat : distance matrix 
        """
        total_dis = 0
        for ind, r in enumerate(tour):
            _from = r
            if ind + 1 == len(tour):
                _to = tour[0]
                total_dis += self.dis_mat[_from - 1][_to - 1]
            else:
                _to = tour[ind + 1]
                total_dis += self.dis_mat[_from - 1][_to - 1]
        return total_dis

    def _optimize(self, initial_tour, Debuglevel=0):
        """
            Improve existing tour 
            using 2-opt method
        """
        minchange = -1
        tour = initial_tour
        while minchange < 0:
            minchange = 0
            for i in range(self.size - 3):
                for j in range(i + 2, self.size - 1):
                    t1 = tour[i]
                    t2 = tour[i + 1]
                    t3 = tour[j]
                    t4 = tour[j + 1]

                    change = (self.dis_mat[t1 - 1][t3 - 1] +
                              self.dis_mat[t2 - 1][t4 - 1] -
                              self.dis_mat[t1 - 1][t2 - 1] -
                              self.dis_mat[t3 - 1][t4 - 1])
                    if change < minchange:
                        minchange = change
                        tour = self.Swap(tour, i + 1, j)
            if Debuglevel:
                print("Tour After Change : ", minchange, "Distances: ",
                      self.get_distance(tour))
        self.best_tour = tour
        return tour

    def _initial_random_tour(self,seed):
        """"
        Return randomly generated tour
        """
        np.random.seed(seed)
        T = np.arange(1,self.size+1)
        np.random.shuffle(T)
        return list(T)

    def run(self):
        tours = []
        tours_dist = []
        #self._write_info()
        for r in range(1):
            T = self._initial_random_tour(r)
            tour = self._optimize(T)
            tour_distance = self.get_distance(tour)
            tours.append(tour)
            tours_dist.append(tour_distance)

        min_dist_index = np.argmin(tours_dist)
        return (tours_dist[min_dist_index], tours[min_dist_index])
        

    """def _write_info(self):
        print("Instance name:", self.instance.name)
        print("Dimention:", self.size)
        print("Distance Type:", self.instance.EdgeWeightType)
        print("\n \t \t Running 2-opt over 50 random tour ")

    def _writestat(self,D,T):
        print("\n Tour Distance: ",D)
        print(" Best Tour by 2-opt is: \n", T)
        print("\n Time to read instance (sec): ", round(self.time_read))
        self.time_algo = time.time() - start_time
        print(" Time to run instances(sec): ", round(self.time_algo))
        print(" Total Time (sec): ", round(self.time_read+self.time_algo))


if len(sys.argv)<2:
	print("need inpute file")
	sys.exit(1)
t = TwoOPT(sys.argv[1])
t.run()	 """
