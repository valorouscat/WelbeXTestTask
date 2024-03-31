import math
import random

def distance(point1: dict, point2: dict):
    return math.sqrt((point1['lat'] - point2['lat'])**2 + (point1['lng'] - point2['lng'])**2)

def total_distance(points, order):
    return sum(distance(points[order[i]], points[order[i - 1]]) for i in range(1, len(order)))

def simulated_annealing(points, temp=100, cooling_rate=0.003, stop_temp=0.001):
    # Start with the first point and then randomize the order of the remaining points
    current_order = list(range(len(points)))
    current_order[1:] = random.sample(current_order[1:], len(points) - 1)
    current_distance = total_distance(points, current_order)

    while temp > stop_temp:
        new_order = list(current_order)
        # Swap two points
        idx1, idx2 = random.sample(range(1, len(points)), 2)  # Ensure we don't swap the first point
        new_order[idx1], new_order[idx2] = new_order[idx2], new_order[idx1]
        new_distance = total_distance(points, new_order)

        # Accept new solution if it's better or with a certain probability
        if new_distance < current_distance or random.random() < math.exp((current_distance - new_distance) / temp):
            current_order = new_order
            current_distance = new_distance

        # Cool down
        temp *= 1 - cooling_rate

    return current_order, current_distance