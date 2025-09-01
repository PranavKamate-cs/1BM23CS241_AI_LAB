from collections import deque

moves = {
    'U': -3, 'D': 3, 'L': -1, 'R': 1
}

def valid_move(pos, move):
    if move == 'U' and pos < 3: return False
    if move == 'D' and pos > 5: return False
    if move == 'L' and pos % 3 == 0: return False
    if move == 'R' and pos % 3 == 2: return False
    return True

def apply_move(state, move, pos):
    new_state = list(state)
    new_pos = pos + moves[move]
    new_state[pos], new_state[new_pos] = new_state[new_pos], new_state[pos]
    return tuple(new_state), new_pos

def dls(state, pos, goal, limit, path, visited):
    if state == goal:
        return path
    if limit <= 0:
        return None

    visited.add(state)

    for move in moves:
        if valid_move(pos, move):
            new_state, new_pos = apply_move(state, move, pos)
            if new_state not in visited:
                result = dls(new_state, new_pos, goal, limit - 1, path + [move], visited)
                if result is not None:
                    return result
    return None

def ids(start, goal, max_depth=50):
    for depth in range(max_depth):
        visited = set()
        result = dls(start, start.index(0), goal, depth, [], visited)
        if result is not None:
            return result
    return None

# Print 3x3 matrix
def print_matrix(state):
    for i in range(0, 9, 3):
        print(state[i:i+3])
    print()

print("Enter initial state (3x3 matrix, use 0 for blank):")
initial = []
m=0
for _ in range(3):
    row = list(map(int, input().split()))
    initial.extend(row)

start = tuple(initial)
goal  = (1,2,3,4,5,6,7,8,0)

print("\n--- Using IDS ---")
solution_ids = ids(start, goal)
if solution_ids is None:
    print("No solution found (IDS within depth limit).")
else:
    state = start
    pos = state.index(0)
    print("Initial State:")
    print_matrix(state)
    for move in solution_ids:
        state, pos = apply_move(state, move, pos)
        print(f"Move: {move}")
        print_matrix(state)
        m+=1
print("moves =",m)
