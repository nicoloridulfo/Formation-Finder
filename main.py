import pandas as pd
import numpy as np
from Data.Data import DataManager
from Formations.Formations import *
from Formations.Trading import *
import pickle
import os.path
if __name__ == "__main__":
    daysBack = 7
    daysHold = 5
    commission = 0.005

    data = DataManager("Data/data/", ["SENS.ST", "ATCO-B.ST", "GETI-B.ST","AF-B.ST"])#open("Data/allTickers.txt","r").read().split("\n"))

    if os.path.isfile("stockdata.p"):
        stockdata = pickle.load(open("stockdata.p", "rb"))
    else:
        stockdata = data.generateDescription(daysBack, daysHold, commission)
        pickle.dump(stockdata, (open("stockdata.p", "wb")))


    population = Population(200**2, daysBack)
    population.setTrader(NumbaTrading(stockdata))
    #population.setTrader(CupyTrading(stockdata))
    #population.setTrader(NumpyTrading(stockdata))
    #population.setTrader(NumpyTrading2(stockdata))

    for n in range(5):
        population.trade()
        population.sortPop()
        for n in range(5):
            print(population.population[n])
        population.breed()

    population.trade(stockdata,commission)
    population.sortPop()
    print(population.population[0].__dict__)
        







