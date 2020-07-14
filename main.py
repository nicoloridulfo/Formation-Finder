import pandas as pd
from Data.Data import *
from Formations.Formations import *
from Formations.Trading import *
import pickle
import os
from tqdm import tqdm

if __name__ == "__main__":
    daysBack = 4
    daysHold = 5
    commission = 0.005

    #tickers = ["SENS.ST", "ATCO-B.ST", "GETI-B.ST","AF-B.ST"]
    tickers = []
    #tickers = [ticker.replace(".csv", "") for ticker in os.listdir("Data/data/")]
    #tickers = tickers[:int(len(tickers)/5)]
    with open("Data/OMX-Tickers.txt", "r") as f:
        tickers = f.read().split("\n")
    print(tickers)
    print(tickers[0:-2])
    stocksDF = [pd.read_csv(f"Data/data/{stock}.csv", sep=',', header = 0) for stock in tickers[0:-2]]
    desc, profits = generateDescription(stocksDF, daysBack, daysHold)

    population = Population(40**2, daysBack)
    print("Training:")
    for n in range(10):
        print("Generation:", n+1)
        population.trade(desc, profits, 0.005)
        population.sortPop()
        for n in range(5):
            f = population.population[n]
            print("n: ", f.nTrades, "acc: ", f.accumulated,"avg: ", f.average)

        population.breed()

    print(tickers)
    print(tickers[-2])
    stocksDF = [pd.read_csv(f"Data/data/{stock}.csv", sep=',', header = 0) for stock in tickers[-2:]]
    desc, profits = generateDescription(stocksDF, daysBack, daysHold)
    print("Validating:")
    population.trade(desc, profits, 0.005)
    population.sortPop()
    for n in range(5):
        f = population.population[n]
        print("n: ", f.nTrades, "acc: ", f.accumulated,"avg: ", f.average)
        







