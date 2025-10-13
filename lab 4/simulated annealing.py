import math
import random

def calculate_total_distance(tour, cities):
    """
    Calculates the total distance of a tour.
    A tour is a list of city indices in the order they are visited.
    """
    total_distance = 0
    num_cities = len(tour)
    for i in range(num_cities):
        # Get the current city and the next city in the tour
        from_city_index = tour[i]
        # If it's the last city, the next city is the starting city
        to_city_index = tour[(i + 1) % num_cities]

        # Get city coordinates from the cities dictionary
        city1 = cities[from_city_index]
        city2 = cities[to_city_index]

        # Calculate Euclidean distance between the two cities
        distance = math.sqrt((city1['x'] - city2['x'])**2 + (city1['y'] - city2['y'])**2)
        total_distance += distance

    return total_distance

def acceptance_probability(current_energy, new_energy, temperature):
    """
    Calculates the probability of accepting a new, worse solution.
    If the new solution is better, it's always accepted (prob=1.0).
    Otherwise, the probability is calculated based on the energy difference
    and the current temperature, following the Metropolis criterion.
    """
    if new_energy < current_energy:
        return 1.0
    return math.exp((current_energy - new_energy) / temperature)

def simulated_annealing(cities, initial_temp, cooling_rate):
    """
    Implements the Simulated Annealing algorithm to find the shortest tour for TSP.

    Args:
        cities (dict): A dictionary where keys are city indices and values are
                       dictionaries with 'x' and 'y' coordinates.
        initial_temp (float): The starting temperature for the annealing process.
        cooling_rate (float): The rate at which the temperature decreases.

    Returns:
        tuple: A tuple containing the best tour found (list of city indices) and
               its total distance (float).
    """
    # 1. Initialization
    city_indices = list(cities.keys())
    # Start with a random tour
    current_solution = random.sample(city_indices, len(city_indices))
    current_energy = calculate_total_distance(current_solution, cities)

    print(f"Initial random tour distance: {current_energy:.2f}")

    # Keep track of the best solution found so far
    best_solution = list(current_solution)
    best_energy = current_energy

    temp = initial_temp

    # 2. Main Loop
    # The algorithm stops when the system has "cooled" enough
    while temp > 1:
        # 3. Generate a Neighboring Solution
        # Create a new solution by swapping two random cities in the current tour
        new_solution = list(current_solution)
        pos1 = random.randint(0, len(cities) - 1)
        pos2 = random.randint(0, len(cities) - 1)
        # Ensure pos1 and pos2 are different
        while pos1 == pos2:
            pos2 = random.randint(0, len(cities) - 1)

        new_solution[pos1], new_solution[pos2] = new_solution[pos2], new_solution[pos1]

        # 4. Calculate Energy of the Neighbor
        new_energy = calculate_total_distance(new_solution, cities)

        # 5. Decide Whether to Accept the Neighbor
        if acceptance_probability(current_energy, new_energy, temp) > random.random():
            current_solution = list(new_solution)
            current_energy = new_energy

        # Update the best solution found if the current one is better
        if current_energy < best_energy:
            best_solution = list(current_solution)
            best_energy = current_energy
        
        # 6. Cool the Temperature
        temp *= (1 - cooling_rate)

    return best_solution, best_energy

# --- Main execution block ---
if __name__ == '__main__':
    # Define a set of cities with their (x, y) coordinates
    # For simplicity, we use a dictionary. The keys are identifiers.
    cities = {
        0: {'x': 60, 'y': 200},
        1: {'x': 180, 'y': 200},
        2: {'x': 80, 'y': 180},
        3: {'x': 140, 'y': 180},
        4: {'x': 20, 'y': 160},
        5: {'x': 100, 'y': 160},
        6: {'x': 200, 'y': 160},
        7: {'x': 140, 'y': 140},
        8: {'x': 40, 'y': 120},
        9: {'x': 100, 'y': 120},
        10: {'x': 180, 'y': 100},
        11: {'x': 60, 'y': 80},
        12: {'x': 120, 'y': 80},
        13: {'x': 180, 'y': 60},
        14: {'x': 20, 'y': 40},
        15: {'x': 100, 'y': 40},
        16: {'x': 200, 'y': 40},
        17: {'x': 20, 'y': 20},
        18: {'x': 60, 'y': 20},
        19: {'x': 160, 'y': 20}
    }

    # Set algorithm parameters
    initial_temperature = 10000
    # Cooling rate should be close to 1, e.g., 0.999, but we use a faster one for quick demo
    cooling_rate = 0.003

    # Run the simulated annealing algorithm
    best_tour, best_distance = simulated_annealing(cities, initial_temperature, cooling_rate)

    # Print the results
    print("\n--- Simulated Annealing Results ---")
    print(f"Final tour distance: {best_distance:.2f}")
    print(f"Optimal tour order: {best_tour}")
    print("---------------------------------")
