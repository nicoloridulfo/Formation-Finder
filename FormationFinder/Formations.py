import random
import numpy as np
from tqdm import tqdm
from numba import njit
def randomMatrix(width = 1, height = 1):
	'''
	Generates random array with -1's and 1's
	'''
	matrix = np.random.choice([-1, 1], size=height*width, p=[.5, .5])
	return np.reshape(matrix, (height, width))

class Formation:
	'''
	A formation
	'''
	geneChoice = [0]*5 + [1,-1]
	def __init__(self, candles: int):

		assert candles > 1, "Candles must be greater than 1"

		self.candles = candles

		self.genes = []
		for _ in range(8 * (candles-1)**2 + 8*(candles-1)):
			self.genes.append(random.choice(self.geneChoice))

	def getGenes(self)->np.array:
		return np.array(self.genes)
	
	def __str__(self):
		return str(self.__dict__)

class Population:
	def __init__(self, size, candles):
		self.size = size
		self.candles = candles

		self.population = []
		for _ in range(size):
			self.population.append(Formation(candles))

	def trade(self, descriptions, profits, cost):
		for formation in tqdm(self.population):
			genes = formation.getGenes()
			trades = _doTrade(formation.getGenes(), descriptions, profits)
			formation.trades = np.array(trades) - cost
		
		self.calculateStatistics()

	def calculateStatistics(self):
		for formation in self.population:
			formation.nTrades = len(formation.trades)

			formation.accumulated = 1
			formation.winloose = 0
			formation.std = 0
			formation.average = 0
			formation.sum = 0

			if formation.nTrades>0:
				formation.accumulated = np.product(formation.trades)
				formation.winloose = len(formation.trades[formation.trades>1])/len(formation.trades)
				formation.std = np.std(formation.trades)
				formation.average = np.average(formation.trades)
				formation.sum = np.sum(formation.trades-1)

	def sortPop(self):
		self.population.sort(key=lambda x: x.accumulated, reverse=True)
		
	def breed(self):
		topFormations = self.population[:int(self.size**0.5)]
		newPopulation = []
		for formation1 in topFormations:
			for formation2 in topFormations:
				f = Formation(self.candles)
				f.genes = self.merge(formation1.genes, formation2.genes)
				newPopulation.append(f)
		self.population = newPopulation

	def merge(self, genes1, genes2):
		breakPoint = random.randint(0,len(genes1))
		newGenes = genes1[0:breakPoint] + genes2[breakPoint:]
		if random.random()<0.1:
			newGenes[random.randint(0,len(newGenes)-1)] = random.choice([-1,0,1])
		return newGenes

@njit
def _doTrade(genom, OHLC, profits):
	trades = []
	for day in range(len(OHLC)):
		makeTrade = True
		for index in range(len(OHLC[day])-1):
			if genom[index]==0: continue

			if OHLC[day][index] != genom[index]:
				makeTrade = False
				break
		
		if makeTrade:
			trades.append(profits[day])
	return trades