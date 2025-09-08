import heapq

# Goal state
goal_state = [1, 2, 3, 
              4, 5, 6, 
              7, 8, 0]

# Moves for the blank tile (up, down, left, right)
moves = {
    0: [1, 3],          # Blank at index 0 can move right or down
    1: [0, 2, 4],
    2: [1, 5],
    3: [0, 4, 6],
    4: [1, 3, 5, 7],
    5: [2, 4, 8],
    6: [3, 7],
    7: [4, 6, 8],
    8: [5, 7]
}

# Manhattan distance heuristic
def manhattan_distance(state):
    distance = 0
    for i in range(9):
        if state[i] != 0:
            x1, y1 = divmod(i, 3)  # current position
            x2, y2 = divmod(goal_state.index(state[i]), 3)  # goal position
            distance += abs(x1 - x2) + abs(y1 - y2)
    return distance

# Generate new states after moving blank
def get_neighbors(state):
    neighbors = []
    zero_index = state.index(0)
    for move in moves[zero_index]:
        new_state = state[:]
        new_state[zero_index], new_state[move] = new_state[move], new_state[zero_index]
        neighbors.append(new_state)
    return neighbors

# A* search
def a_star(start_state):
    pq = []  # priority queue
    heapq.heappush(pq, (manhattan_distance(start_state), 0, start_state, []))
    visited = set()

    while pq:
        f, g, state, path = heapq.heappop(pq)
        state_tuple = tuple(state)

        if state == goal_state:
            return path + [state]

        if state_tuple in visited:
            continue
        visited.add(state_tuple)

        for neighbor in get_neighbors(state):
            if tuple(neighbor) not in visited:
                new_g = g + 1
                new_f = new_g + manhattan_distance(neighbor)
                heapq.heappush(pq, (new_f, new_g, neighbor, path + [state]))
    return None

# Helper function to print puzzle state
def print_puzzle(state):
    for i in range(0, 9, 3):
        print(state[i:i+3])
    print()

# Example Usage
if __name__ == "__main__":
    start = [1, 2, 3,
             4, 0, 6,
             7, 5, 8]

    print("Initial State:")
    print_puzzle(start)

    solution = a_star(start)
    if solution:
        print("Solution found in", len(solution)-1, "moves:")
        for step in solution:
            print_puzzle(step)
    else:
        print("No solution exists!")
