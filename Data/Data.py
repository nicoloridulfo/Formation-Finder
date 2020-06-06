from typing import List, Dict
import pandas as pd
from tqdm import tqdm
import os
from pandas_datareader import data
import numpy as np

class DataManager:
    '''
    This object manages the data.
    '''
    def __init__(self, path:str, tickers:List[str]):
        self.path = path
        self.tickers = tickers
        self.panel:Dict = {}

        #self._download()
        self._importData()

    def _download(self):
        for ticker in tqdm(self.tickers):
            if ticker in os.listdir("data"): continue

            try:
                data.DataReader(ticker, "yahoo", start="1980-01-01").to_csv(f"Data/data/{ticker}.csv", sep=',')
            except Exception as e:
                print(e)
                print(f"Could not download: {ticker}\n")
    
    def _importData(self):
        print("Loading data: ")
        for ticker in tqdm(self.tickers):
           self.panel[ticker] = pd.read_csv(f"Data/data/{ticker}.csv", sep=',', header = 0)

    def generateDescription(self, daysBack, daysHold, commission):
        """
        Returns a dictionary with {ticker:{OHLC:ndArray, profits:array}}
        """
        datas = {}
        for ticker in tqdm(self.panel.keys()):
            OHLC, profits = self._dataDescriptor(self.panel[ticker], daysBack, daysHold)
            profits = profits-commission
            datas[ticker] = {"OHLC":OHLC, "profits":profits}
        return datas


    def _dataDescriptor(self, stockData:pd.DataFrame, daysBack = 2, daysHold = 1):
        """
        Converts a OHLC dataframe to the signals and profit
        """
        stockData = stockData[["Open", "High", "Low", "Close"]]
        
        stockData["Profit"] = stockData["Close"].pct_change(periods=daysHold).shift(-1*daysHold)+1
        stockData=stockData.dropna() # Remove the last days where profit cant be calculated

        descriptions = []
        profits = []
        for row in range(daysBack-1, len(stockData)): # Day iterator

            todaysDescription = []
            for i in range(0, daysBack-1): # today's candle
                for j in range(i+1, daysBack): # yesterday's candle
                    genomIndex = -1
                    for home in range(4): #reverse of range(4) to get 3,2,1,0 since that is the order of the line
                        for away in range(4):
                            genomIndex+=1

                            todayPrice = stockData.iloc[row-i, home]
                            yesterdayPrice = stockData.iloc[row-j, away]
                            todaysDescription.append(1 if todayPrice>yesterdayPrice else -1)
            descriptions.append(todaysDescription)
            profits.append(stockData.iloc[row, stockData.shape[1]-1])
        return (np.array(descriptions), np.array(profits))
