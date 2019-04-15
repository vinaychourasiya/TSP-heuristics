# coding: utf-8
# Author: Vinay Chourasiya
import time
start_time = time.time()
import sys
from readData import ReadData
import numpy as np

class NN():
    name = "Nearest Neighbor"

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

    def get_dist_mat(self):
        """
        changing the distances between tha
        i to i with infinity for simility in code
        """
        D = self.dis_mat.copy()
        for i in range(self.size):
            D[i][i]=np.inf
        return D


    def nn_algo(self,startPoint):
        """
        Nearest Neighbour algorithm
        """    
        dist_mat = self.get_dist_mat()
        Tour = [startPoint]
        for _ in  range(self.size-1):
            min_index = np.argmin(dist_mat[Tour[-1]])
            for t in Tour:
                dist_mat[min_index][t] = np.inf
                dist_mat[t][min_index] = np.inf
            Tour.append(min_index)
        return np.array(Tour)
    
    def run(self):
        """
        randomly chooces starting point
        10% of intances size
        and max = 1000
        min = 10
        and call nn_algo for tour
        """
        tours_dist = []
        tours = []
        self._write_info()
        startPoints = self._start_pt_list()
        for s in startPoints:
            t = self.nn_algo(s)
            d = self.get_tour_distance(t)
            tours.append(t+1)
            tours_dist.append(d)
        
        self._best_tour(tours,tours_dist) 

    def _best_tour(self,Ts,Tsd):
        min_dist_index = np.argmin(Tsd)
        self._writestat(Tsd[min_dist_index], Ts[min_dist_index])

    def get_tour_distance(self,T):
        s = 0
        for i,t in enumerate(T):
            try:
                s+=self.dis_mat[t][T[i+1]]
            except IndexError:
                s+=self.dis_mat[t][T[0]]
        return s

    def _write_info(self):
        """
        write info about instance
        """
        print("Instance name:", self.instance.name)
        print("Dimention:", self.size)
        print("Distance Type:", self.instance.EdgeWeightType)
        print("\n \t \t Running 2-opt over 50 random tour ")

    def _writestat(self,D,T):
        """
        Write stats
        """
        print("\n Tour Distance: ",D)
        print(" Best Tour by 2-opt is: \n", T)
        print("\n Time to read instance (sec): ", round(self.time_read))
        self.time_algo = time.time() - start_time
        print(" Time to run instances(sec): ", round(self.time_algo))
        print(" Total Time (sec): ", round(self.time_read+self.time_algo))
   
    def _start_pt_list(self):
        """
        return starting points list
        """
        np.random.seed(1)
        a = round(self.size*0.1)
        mi = 10
        mx = 1000
        if a>mx:
            l = np.random.choice(self.size, mx, replace=False)
            return(l)
        elif a<=10:
            l = np.random.choice(self.size, mi, replace=False)
            return(l)
        else:
            l = np.random.choice(self.size, a, replace=False)
            return(l)


if len(sys.argv)<2:
    print("need inpute file")
    sys.exit(1)
t = NN(sys.argv[1])
t.run()	          
