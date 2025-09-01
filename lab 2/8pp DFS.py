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

def dfs(start, goal, depth_limit=100):
    stack = [(start, start.index(0), [])]
    visited = set()

    while stack:
        state, pos, path = stack.pop()

        if state == goal:
            return path

        if tuple(state) in visited or len(path) >= depth_limit:
            continue
        visited.add(tuple(state))

        for move in moves:
            if valid_move(pos, move):
                new_state, new_pos = apply_move(state, move, pos)
                stack.append((new_state, new_pos, path + [move]))
    return None

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

solution = dfs(start, goal)

if solution is None:
    print("No solution found within depth limit.")
else:
    print("\nSolution Path (as matrices):\n")
    state = start
    pos = state.index(0)
    print_matrix(state)  # initial state
    for move in solution:
        state, pos = apply_move(state, move, pos)
        print(f"Move: {move}")
        print_matrix(state)
        m+=1
print("moves =",m)
