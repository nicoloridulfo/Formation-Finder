import unittest
from Formations import Formation, Population
import numpy as np

class FormationTest(unittest.TestCase):
    def test_Genes(self):
        formation = Formation(2)
        self.assertEqual(len(formation.genes),16)

        for gene in formation.genes:
            self.assertTrue(gene==1 or gene==-1 or gene==0)

class PopulationTest(unittest.TestCase):
    def test_Population(self):
        population = Population(10,2)
        self.assertEqual(len(population.population), 10)
        for formation in population.population:
            self.assertEqual(type(formation), Formation)

    def test_trade(self):
        population = Population(1,2)
        genes = [0]*16
        #genes[0] = -1
        population.population[0].genes = genes

        data = [[1]*16]*2
        profit = [42,43]

        population.trade((np.reshape(np.array(data), (2,16)), np.array(profit)))
        tradesTaken = population.population[0].trades
        self.assertEqual(len(profit), len(tradesTaken), "Should be the name number of trades")
        for n in range(len(data)):
            self.assertEqual(profit[n], tradesTaken[n])

 
if __name__ == '__main__':
    unittest.main()