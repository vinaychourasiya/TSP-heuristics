# TSP-heuristics
Implementing various heuristics for Travelling Salesman Problem (TSP), Namely Lin-Kernighan Heuristic, Nearest Neighour Heuristic, genetic algorithm, Simulated Annealing

#abouts files attached
	TSP_Data: is directory of All TSPLIB instances
	readData.py: is reading file from TSP_Data
	All other python files or implemetation of algorithm

Steps for running algorithms
# terminal commands
	$ python 'algorithm.py' 'filename'  #for nearest-neighbour
-'algorithm.py': 2-opt.py, nn.py, ga_2-opt_tsp.py, ga_tsp.py	   
-'filename' picked any file from TSP_Data folder eg. ch130.tsp or a280.tsp

# Example runs			
	$ python nn.py kroB100.tsp
	$ python 2-opt.py kroB100.tsp
	$ python ga_tsp.py kroB100.tsp
	$ python ga_2-opt_tsp.py kroB100.tsp
	$ python runSA.py kroB100.tsp
	$ python runSA2opt.py kroB100.tsp 
 
# Some Results:
![TSP Tour](a280_2opt.png?raw=true "a280_2opt Tour")
![TSP Tour](kroE100_2opt.png?raw=true "kroE100_2opt.png")
 
 
