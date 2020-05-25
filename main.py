import pandas as pd
import numpy as np
from Data import DataManager
from Formations import *
daysBack = 2
daysHold = 5
commission = 0.005

data = DataManager("Data/data/", ["SENS.ST", "ATCO-B.ST", "GETI-B.ST","AF-B.ST", "SSAB-B.ST"])#open("Data/allTickers.txt","r").read().split("\n"))

stockdata = data.get(daysBack, daysHold)

population = Population(70**2, daysBack)
for n in range(5):
    population.trade(stockdata, commission)
    population.sortPop()
    for n in range(5):
        print(population.population[n])
    population.breed()

population.trade(stockdata,commission)
population.sortPop()
print(population.population[0].__dict__)
    







