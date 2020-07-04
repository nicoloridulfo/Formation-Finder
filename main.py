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
    
    if os.path.isfile("stockdata.p"):
        desc, profits = pickle.load(open("stockdata.p", "rb"))
    else:
        tickers = [ticker.replace(".csv", "") for ticker in os.listdir("Data/data/")]
        tickers = tickers[:int(len(tickers)/2)]
        stocksDF = [pd.read_csv(f"Data/data/{stock}.csv", sep=',', header = 0) for stock in tickers]
        desc, profits = generateDescription(stocksDF, daysBack, daysHold)
        pickle.dump((desc, profits), open("stockdata.p", "wb"))

    population = Population(40**2, daysBack)
    for n in range(5):
        population.trade(desc, profits)
        population.sortPop()
        for n in range(5):
            print(population.population[n])
        population.breed()

    population.trade(desc, profits)
    population.sortPop()
    print(population.population[0].__dict__)
        







