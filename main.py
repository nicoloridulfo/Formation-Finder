import pandas as pd
from FormationFinder import *
from tqdm import tqdm
from sklearn.model_selection import train_test_split
if __name__ == "__main__":
    daysBack = 3
    daysHold = 5
    commission = 0.005
    nGenerations = 5
    #tickers = ["SENS.ST", "ATCO-B.ST", "GETI-B.ST","AF-B.ST"]
    tickers = []
    #tickers = [ticker.replace(".csv", "") for ticker in os.listdir("Data/data/")]
    #tickers = tickers[:int(len(tickers)/5)]
    with open("Data/OMX-Tickers.txt", "r") as f:
        tickers = f.read().split("\n")
    stocksDF = [pd.read_csv(f"Data/data/{stock}.csv", sep=',', header = 0) for stock in tickers]
    desc, profits = generateDescription(stocksDF, daysBack, daysHold)

    desc_train, desc_test, profits_train, profits_test = train_test_split(desc, profits, test_size=0.5)
    print("Length Training data:", len(desc_train))
    print("Length validation data:", len(desc_test))
    
    population = Population(40**2, daysBack)
    print("Training:")
    for n in range(nGenerations):
        print("Generation:", n+1)
        population.trade(desc_train, profits_train, commission)
        population.sortPop()
        for n in range(5):
            formation:Formation = population.population[n]
            print("n: ", formation.nTrades, "acc: ", formation.accumulated,"avg: ", formation.average)

        population.breed()

    print("Validating:")
    population.trade(desc_test, profits_test, commission)
    population.sortPop()
    for n in range(5):
        f = population.population[n]
        print("n: ", f.nTrades, "acc: ", f.accumulated,"avg: ", f.average)
        







