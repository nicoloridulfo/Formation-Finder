from typing import Union, List
import pandas as pd
from tqdm import tqdm
import numpy as np
from numba import njit

def generateDescription(data: Union[pd.DataFrame, List[pd.DataFrame]],
                        daysBack: int,
                        daysHold: int):
    '''
    Generates the description for a dataframe
    
    Returns:
        numpy-ndarray with description and a numpy-array with the profits
    '''
    if isinstance(data, pd.DataFrame):
        stockData = data[["Open", "High", "Low", "Close"]].to_numpy().copy()
        return _generate(stockData, daysBack, daysHold)
        
    elif isinstance(data, list):
        accumulatedDesc = accumulatedProfit = None
        for i, stock in tqdm(list(enumerate(data))):
            stockData = stock[["Open", "High", "Low", "Close"]].to_numpy().copy()
            if i == 0:
                accumulatedDesc, accumulatedProfit = _generate(stockData, daysBack, daysHold)
            else:
                stockData = stock[["Open", "High", "Low", "Close"]].to_numpy().copy()
                resDesc, resProfit = _generate(stockData, daysBack, daysHold)

                accumulatedDesc = np.append(accumulatedDesc, resDesc, axis = 0)
                accumulatedProfit = np.append(accumulatedProfit, resProfit)
        return accumulatedDesc, accumulatedProfit
@njit
def _generate(stockData, nCandles, daysHold):
    assert nCandles>=2
    
    '''
    ## Let's say that the data is of 6 days, nCandles = 2 and dayshold = 2
    #### XXXX
    #### XXXX <-- Starts here
    #### XXXX
    #### XXXX <-- last possible purchase
    #### XXXX
    #### XXXX <-- Last sell here

    => 3 description rows
    '''
    numDesc = 8 * (nCandles-1)**2 + 8*(nCandles-1)
    lenDesc = len(stockData) - (nCandles-1) - daysHold
    desc = np.zeros(shape=(lenDesc, numDesc))
    profits = np.zeros(shape=(lenDesc,))

    for row in range(nCandles-1, len(stockData)-daysHold): # Day iterator
        profits[row-(nCandles-1)] = stockData[row+daysHold][3] / stockData[row][3]
        genomIndex = -1
        for i in range(0, nCandles-1): # today's candle
            for j in range(i+1, nCandles): # yesterday's candle
                for home in range(4): #reverse of range(4) to get 3,2,1,0 since that is the order of the line
                    for away in range(4):
                        genomIndex+=1

                        todayPrice = stockData[row-i][home]
                        yesterdayPrice = stockData[row-j][away]

                        desc[row-(nCandles-1)][genomIndex] = 1 if todayPrice > yesterdayPrice else -1
    return desc, profits