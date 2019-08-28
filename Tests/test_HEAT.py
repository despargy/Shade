import HEAT as heat
from threading import Thread
import time
import unittest


"""
script to test heating control using fake data
    modify time_to_run parameter
        and
    path if needed
"""
class TestHEAT(unittest.TestCase):

    heat = heat.HEAT()
    heat.start()
    #def test_num(self, heat):
        #self.assertAlmostEqual(heat.consider_data([2,1,3]), True)
        #self.assertAlmostEqual(heat.consider_data([10,15,19]),False)
        #self.assertAlmostEqual(heat.consider_data([-10, 22.4, 22.8]), False)


    def test_values(self,heat):
        self.assertRaises(ValueError, heat.consider_data(),[False])



