# coding: utf-8
# Author: Vinay Chourasiya

from math import sin, cos, sqrt, atan2, radians
import sys
import os
from scipy.spatial.distance import pdist, squareform
import numpy as np


class ReadData():
    def __init__(self, filename):

        self.name = filename[:-4]
        self.size = self.getSize()
        self.EdgeWeightType = self.getEdgeWeightType()
        self.format_ = self.getFormat()  # for EXPLICIT data only

    def getFormat(self):
        format_ = "None"
        try:
            with open(f'TSP_Data/{self.name}.tsp') as data:
                datalist = data.read().split()
                for ind, elem in enumerate(datalist):
                    if elem == "EDGE_WEIGHT_FORMAT:":
                        format_ = datalist[ind + 1]
                        break
                    elif elem == "EDGE_WEIGHT_FORMAT":
                        format_ = datalist[ind + 2]
                        break
            return format_

        except IOError:
            print("Input file not found")
            sys.exit(1)

    def getEdgeWeightType(self):
        EdgeType = "None"
        try:
            with open(f'TSP_Data/{self.name}.tsp') as data:
                datalist = data.read().split()
                for ind, elem in enumerate(datalist):
                    if elem == "EDGE_WEIGHT_TYPE:":
                        EdgeType = datalist[ind + 1]
                        #print(EdgeType)
                        break
                    elif elem == "EDGE_WEIGHT_TYPE":
                        EdgeType = datalist[ind + 2]
                        #print(EdgeType)
                        break
            return EdgeType

        except IOError:
            print("Input file not found")
            sys.exit(1)

    def getSize(self):
        """
        Return size of instances (i.e. Number of
        cities)
        
        """
        size = 0
        try:
            with open(f'TSP_Data/{self.name}.tsp') as data:
                datalist = data.read().split()
                for ind, elem in enumerate(datalist):
                    if elem == "DIMENSION:":
                        size = datalist[ind + 1]
                        #print(size)
                        break
                    elif elem == "DIMENSION":
                        size = datalist[ind + 2]
                        #print(size)
                        break
            return int(size)
        except IOError:
            print("Input file not found")
            sys.exit(1)

    def read_Data(self):
        with open(f'TSP_Data/{self.name}.tsp') as data:
            cities = []
            Isdata = True
            while (Isdata):
                line = data.readline().split()
                if len(line) <= 0:
                    break
                tempcity = []
                for i, elem in enumerate(line):
                    try:
                        temp = float(elem)
                        tempcity.append(temp)
                    except ValueError:
                        break
                if len(tempcity) > 0:
                    cities.append(np.array(tempcity))
        return np.array(cities)

    def GetDistanceMat(self):
        if self.EdgeWeightType == "EXPLICIT":
            DistanceMat = self.getMat()
            return DistanceMat
        elif self.EdgeWeightType == "EUC_2D" or "CEIL_2D":
            DistanceMat = self.EuclidDist()
            return DistanceMat
        elif self.EdgeWeightType == "GEO":
            DistanceMat = self.GeographicDist()
            return DistanceMat
        else:
            return None

    def EuclidDist(self):
        cities = self.read_Data()
        #DistanceDict = {}
        A = cities[:, 1:3]
        DistanceMat = np.round(squareform(pdist(A)))
        return DistanceMat

    def GeographicDist(self):
        R = 6373.0
        cities = self.read_Data()
        DistanceMat = np.zeros((self.size, self.size))
        for i in range(self.size):
            for j in range(0, i + 1):
                node1 = cities[i]
                node2 = cities[j]
                lat1 = radians(node1[1])
                lat1 = radians(node1[1])
                lon1 = radians(node1[2])
                lat2 = radians(node2[1])
                lon2 = radians(node2[2])
                dlon = lon2 - lon1
                dlat = lat2 - lat1
                a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
                c = 2 * atan2(sqrt(a), sqrt(1 - a))
                distance = R * c
                DistanceMat[i, j] = distance
                DistanceMat[j, i] = distance
        return DistanceMat

    def getMat(self):
        DataFormat = self.getFormat()
        if DataFormat == "FULL_MATRIX":
            cities = self.read_Data()
            DistanceMat = cities[:self.size]
            return DistanceMat

        elif DataFormat == "LOWER_DIAG_ROW":
            with open(f'TSP_Data/{self.name}.tsp') as file:
                indicator = False
                data = file.read().split()
                templist = []
                cities = []
                for elem in data:
                    if elem == "EDGE_WEIGHT_SECTION":
                        indicator = True
                        continue
                    if indicator:
                        try:
                            it = float(elem)
                            templist.append(it)
                        except:
                            break
                        if it == 0:
                            cities.append(templist)
                            templist = []
                DistanceMat = np.zeros((self.size, self.size))
                for i in range(self.size):
                    temp = []
                    l = len(cities[i])
                    for j in range(self.size):
                        if j <= (l - 1):
                            temp.append(cities[i][j])
                        else:
                            temp.append(cities[j][i])
                    DistanceMat[i] = temp
                return DistanceMat
        elif DataFormat == "UPPER_DIAG_ROW":
            with open(f'TSP_Data/{self.name}.tsp') as file:
                indicator = False
                data = file.read().split()
                templist = []
                cities = []
                for elem in data:
                    if elem == "EDGE_WEIGHT_SECTION":
                        indicator = True
                        continue
                    if indicator:
                        try:
                            it = float(elem)
                            templist.append(it)
                        except ValueError:
                            break
                        if it == 0:
                            cities.append(templist)
                            templist = []
                print("Need to complete it")
        else:
            sys.exit("No Format Match for EXPLICIT data")

