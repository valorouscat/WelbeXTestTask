import unittest
from utils import simulated_annealing, total_distance, distance
import math

class TestSimulatedAnnealing(unittest.TestCase):
    def validayion_test_simulated_annealing(self):
        points = [{'lat': x, 'lng': x} for x in range(11)]
        temp = 100
        cooling_rate = 0.003
        stop_temp = 0.001

        order, distance = simulated_annealing(points, temp, cooling_rate, stop_temp)

        # Check that the order is a permutation of the points
        self.assertEqual(set(order), set(range(len(points))))

        # Check that the distance is non-negative
        self.assertGreaterEqual(distance, 0)

        # Check that the function does not crash for different input sizes
        points = [{'lat': x, 'lng': x} for x in range(3)]
        order, distance = simulated_annealing(points, temp, cooling_rate, stop_temp)
        self.assertEqual(set(order), set(range(len(points))))
        self.assertGreaterEqual(distance, 0)

        points = [{'lat': x, 'lng': x} for x in range(10)]
        order, distance = simulated_annealing(points, temp, cooling_rate, stop_temp)
        self.assertEqual(set(order), set(range(len(points))))
        self.assertGreaterEqual(distance, 0)

        # Check that the function does not crash for different temperatures
        temp = 10
        order, distance = simulated_annealing(points, temp, cooling_rate, stop_temp)
        self.assertEqual(set(order), set(range(len(points))))
        self.assertGreaterEqual(distance, 0)

        temp = 0.1
        order, distance = simulated_annealing(points, temp, cooling_rate, stop_temp)
        self.assertEqual(set(order), set(range(len(points))))
        self.assertGreaterEqual(distance, 0)

        # Check that the function does not crash for different cooling rates
        cooling_rate = 0.01
        order, distance = simulated_annealing(points, temp, cooling_rate, stop_temp)
        self.assertEqual(set(order), set(range(len(points))))
        self.assertGreaterEqual(distance, 0)

        cooling_rate = 0.001
        order, distance = simulated_annealing(points, temp, cooling_rate, stop_temp)
        self.assertEqual(set(order), set(range(len(points))))
        self.assertGreaterEqual(distance, 0)

        # Check that the function does not crash for different stop temperatures
        stop_temp = 0.0001
        order, distance = simulated_annealing(points, temp, cooling_rate, stop_temp)
        self.assertEqual(set(order), set(range(len(points))))
        self.assertGreaterEqual(distance, 0)

        stop_temp = 0.00001
        order, distance = simulated_annealing(points, temp, cooling_rate, stop_temp)
        self.assertEqual(set(order), set(range(len(points))))
        self.assertGreaterEqual(distance, 0)

    
    def test_path_is_optimal(self):
        points = [
            {'lat': 0, 'lng': 0},
            {'lat': 0, 'lng': 1},
            {'lat': 1, 'lng': 1},
            {'lat': 1, 'lng': 0},
        ]

        # Check that total_distance is correct
        order = [0, 1, 2, 3]
        self.assertEqual(total_distance(points, order), 3)

        order = [0, 2, 1, 3]
        self.assertAlmostEqual(total_distance(points, order), 1+2*math.sqrt(2))

        order = [0, 3, 2, 1]
        self.assertEqual(total_distance(points, order), 3)

        order = [0, 1, 3, 2]
        self.assertAlmostEqual(total_distance(points, order), 2 + math.sqrt(2))


        # Check that simulated_annealing is correct
        optimal_order, optimal_distance = simulated_annealing(points)

        self.assertIn(optimal_order, [[0, 1, 2, 3], [0, 3, 2, 1]])
        self.assertAlmostEqual(optimal_distance, 3)
        



if __name__ == '__main__':
    unittest.main()