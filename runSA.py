from readData import ReadData
from SA import SimAnneal
import matplotlib.pyplot as plt
import random
import numpy as np


import sys 
if len(sys.argv)<2:
	print("need inpute file")
	sys.exit(1)
filename = sys.argv[1]
D = ReadData(filename)

if __name__ == "__main__":
    # coords = [[random.uniform(-1000, 1000), random.uniform(-1000, 1000)] for i in range(100)]
    sa = SimAnneal(D.GetDistanceMat(),filename)#, stopping_iter=2)
    sa.anneal()
    #sa.batch_anneal()
    #sa.visualize_routes()
    sa.plot_learning()
