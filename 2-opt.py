
# coding: utf-8
# Author: Vinay Chourasiya

from readData import ReadData

class TwoOPT:
    """
    2-opt:
          Generate intial tour
          and improve it by deleting 1 one edges
          and change with other
    -- It gives nearly optimal tour    
    """
    def __init__(self,file):
        """
            Intialize: Instaces file,
                       Distance Matrix,
                       and size
        """
        self.file = file
        self.instance = ReadData(self.file)
        self.size =  self.instance.size
        self.dis_mat = self.instance.GetDistanceMat()
        self.initial_tour = self.get_initial_tour()
        self.best_tour = self.initial_tour
        
    def get_initial_tour(self):
        """
        Return: intial tour
        """
        return  [*range(1,self.size +1)]
        
     
    def Swap(self, tour,x, y):
        """
            tour : Given TSP tour
            x = swappping First index in tour 
            y = swappping last index in tour
            return : new_tour with perfomming swapping 
            note: x and y should be index only (in tour) not exact city number
        """
        new_tour = tour[:x]+[*reversed(tour[x:y+1])]+tour[y+1:]
        return new_tour
    
    def get_distance(self, tour ):
        """
        Given any tour it return total distance of
        given tour
        dis_mat : distance matrix 
        """
        total_dis = 0
        for ind,r in enumerate(tour):
            _from = r   
            if ind+1==len(tour):
                _to = tour[0]
                total_dis+=self.dis_mat[_from-1][_to-1]
            else:
                _to = tour[ind+1]
                total_dis+=self.dis_mat[_from-1][_to-1]
        return total_dis

    def _optimize(self,Debuglevel=0):
        """
            Improve existing tour 
            using 2-opt method
        """
        minchange = -1
        tour = self.initial_tour
        #print(tour)
        while minchange<0:
            minchange = 0
            for i in range(self.size-3):
                for j in range(i+2,self.size-1):
                    t1 = tour[i]; t2 = tour[i+1]
                    t3 = tour[j]; t4 = tour[j+1]  

                    change = (self.dis_mat[t1-1][t3-1]+ self.dis_mat[t2-1][t4-1]- 
                              self.dis_mat[t1-1][t2-1]- self.dis_mat[t3-1][t4-1])
                    if change < minchange:
                        minchange = change
                        tour = self.Swap(tour,i+1,j)
            if Debuglevel:
                print("Tour After Change : ", minchange, "Distances: ", self.get_distance(tour))
        self.best_tour = tour
        return tour
                      
    def get_best_tour(self):
        best_tour = self._optimize()
        tour_distance = self.get_distance(best_tour)
        print("Best tour is: \n", best_tour, "\n Distance of tour is: \n",tour_distance )

t = TwoOPT('ch130.tsp')
t.get_best_tour()