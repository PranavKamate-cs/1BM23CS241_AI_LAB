def print_board(board):
    n = len(board)
    print("Board Visualization:")
    for row in range(n):
        line = ""
        for col in range(n):
            if board[col] == row:
                line += "Q "
            else:
                line += ". "
        print(line)
    print("-" * (2 * n))

def calculate_heuristic(board):
    n = len(board)
    attacking_pairs = 0
    for i in range(n):
        for j in range(i + 1, n):
            if board[i] == board[j]:
                attacking_pairs += 1
            if abs(board[i] - board[j]) == abs(i - j):
                attacking_pairs += 1
    return attacking_pairs

def solve_and_show_steps(initial_board):
    current_board = list(initial_board)
    n = len(current_board)
    step = 1

    while True:
        current_heuristic = calculate_heuristic(current_board)

        print(f"\n{'='*10} Step {step} {'='*10}")
        print(f"Current State: {current_board}")
        print_board(current_board)
        print(f"Current Cost (h) = {current_heuristic}")

        if current_heuristic == 0:
            print("\nGoal configuration reached! No more attacking pairs.")
            print("Algorithm terminated successfully.")
            break

        # --- Neighbor Evaluation ---
        print("\nEvaluating all neighbor nodes:")
        best_neighbor = None
        best_heuristic = current_heuristic

        for col_to_move in range(n):
            original_row = current_board[col_to_move]
            for new_row in range(n):
                if new_row == original_row:
                    continue  # Skip the current configuration

                neighbor_board = list(current_board)
                neighbor_board[col_to_move] = new_row
                neighbor_heuristic = calculate_heuristic(neighbor_board)
                
                print(f"  - Neighbor {neighbor_board} -> Cost (h) = {neighbor_heuristic}")

                if neighbor_heuristic < best_heuristic:
                    best_heuristic = neighbor_heuristic
                    best_neighbor = neighbor_board
        
        print("-" * 30)
        # --- Decision Making ---
        if best_heuristic >= current_heuristic:
            print("Decision: No neighbor has a lower cost.")
            print("Stuck at a local minimum. Algorithm cannot proceed.")
            break
        
        # Otherwise, move to the best neighbor state.
        print(f"Decision: The best neighbor is {best_neighbor} with a cost of {best_heuristic}.")
        print(f"Moving to this state as {best_heuristic} < {current_heuristic}.")
        current_board = best_neighbor
        step += 1


# --- Main execution ---
if __name__ == "__main__":
    N = 4
    initial_board = [3, 1, 3, 1]
    
    print(f"--- Solving {N}-Queens with Hill Climbing (Detailed Steps) ---")
    print(f"Initial board state: {initial_board}")
    
    solve_and_show_steps(initial_board)
