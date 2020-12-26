# TSP-heuristics
Implementing various heuristics for Travelling Salesman Problem (TSP), Namely Lin-Kernighan Heuristic, Nearest Neighour Heuristic, genetic algorithm, Simulated Annealing

# Description 
	TSP_Data: this folder has all TSPLIB instances (e.g ch130.tsp, a280.tsp) 
	readData.py: this python file is used for reading the TSP instances.  
	All other python files are implemetation of algorithm

Steps for running algorithms
# Terminal commands
	$ python 'algorithm.py' 'filename'  
-'algorithm.py': 2-opt.py, nn.py, ga_2-opt_tsp.py, ga_tsp.py
-'filename' pick any file from TSP_Data folder eg. ch130.tsp or a280.tsp

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
 
 
