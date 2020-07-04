from tqdm import tqdm
import numpy as np
import cupy as cp
from numba import njit

class NumpyTrading:    
	def __init__(self, stockdata:dict):
		'''
		stockdata:
		A dictionary with the stockname as key and a dictionary as word.
		The dictionary contains dates, OHLC, profits.
		'''
		self.stockdata = stockdata

	def trade(self, formations):
		for stockname in self.stockdata.keys():
			assert len(self.stockdata[stockname]["OHLC"]) == len(self.stockdata[stockname]["profits"])

			for formation in tqdm(formations):
				if not hasattr(formation, "trades"):
					formation.trades = []

				genes = formation.getGenes()

				match = genes * self.stockdata[stockname]["OHLC"]
				tradesTaken = self.stockdata[stockname]["profits"][np.min(match, axis=1)>=0]

				formation.trades = np.append(formation.trades, tradesTaken)

class NumpyTrading2:    
	def __init__(self, stockdata:dict):
		for stockname in stockdata.keys():
			assert len(stockdata[stockname]["OHLC"]) == len(stockdata[stockname]["profits"])
			if not hasattr(self, "OHLC"):
				self.OHLC = stockdata[stockname]["OHLC"]
				self.profits = stockdata[stockname]["profits"]
			else:
				self.OHLC = np.append(self.OHLC,stockdata[stockname]["OHLC"], axis = 0)
				self.profits = np.append(self.profits, stockdata[stockname]["profits"])

		self.OHLC = cp.asarray(self.OHLC, dtype="float32")
		self.profits = cp.asarray(self.profits, dtype="float32")

	def trade(self, formations):
		formationMatrix:np.array = formations[0].getGenes()
		for formation in formations:
			np.append(formationMatrix, formation.getGenes(), axis=1)
		print(formationMatrix.shape)
		from time import time
		t0 = time()
		results = np.einsum("fg,dg->dfg", formationMatrix, self.OHLC)
		print((time()-t0)*1000)
		exit()


class CupyTrading:
	def __init__(self, stockdata):

		for stockname in stockdata.keys():
			assert len(stockdata[stockname]["OHLC"]) == len(stockdata[stockname]["profits"])
			if not hasattr(self, "OHLC"):
				self.OHLC = stockdata[stockname]["OHLC"]
				self.profits = stockdata[stockname]["profits"]
			else:
				self.OHLC = np.append(self.OHLC,stockdata[stockname]["OHLC"], axis = 0)
				self.profits = np.append(self.profits, stockdata[stockname]["profits"])

		self.OHLC = cp.asarray(self.OHLC, dtype="float32")
		self.profits = cp.asarray(self.profits, dtype="float32")

	def trade(self, formations):
		for formation in tqdm(formations):
			if not hasattr(formation, "trades"):
				formation.trades = []

			genes = cp.asarray(formation.getGenes(), dtype="float32")

			match = genes * self.OHLC
			tradesTaken = self.profits[cp.min(match, axis=1)>=0]

			formation.trades = cp.asnumpy(tradesTaken)

class NumbaTrading:
	def __init__(self, stockdata):

		for stockname in stockdata.keys():
			assert len(stockdata[stockname]["OHLC"]) == len(stockdata[stockname]["profits"])
			if not hasattr(self, "OHLC"):
				self.OHLC = stockdata[stockname]["OHLC"]
				self.profits = stockdata[stockname]["profits"]
			else:
				self.OHLC = np.append(self.OHLC,stockdata[stockname]["OHLC"], axis = 0)
				self.profits = np.append(self.profits, stockdata[stockname]["profits"])

	def trade(self, formations):
		for formation in tqdm(formations):
			genes = formation.getGenes()
			trades = _doTrade(formation.getGenes(), self.OHLC, self.profits)
			formation.trades = np.array(trades)
@njit
def _doTrade(genom, OHLC, profits):
	trades = []
	for day in range(len(OHLC)):
		makeTrade = True
		for index in range(len(OHLC)):
			if OHLC[day][index] != genom[index]:
				makeTrade = False
				break
		
		if makeTrade:
			trades.append(profits[day])
	return trades

