import random
import statistics
import time

def random_board(n):
    """Generate a random board configuration"""
    return [random.randint(0, n - 1) for _ in range(n)]

def compute_heuristic(board):
    """Count the number of pairs of queens attacking each other"""
    h = 0
    n = len(board)
    for i in range(n):
        for j in range(i + 1, n):
            if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                h += 1
    return h

def get_neighbors(board):
    """Generate all neighbors by moving one queen in its column"""
    neighbors = []
    n = len(board)
    for col in range(n):
        for row in range(n):
            if row != board[col]:
                new_board = board.copy()
                new_board[col] = row
                neighbors.append(new_board)
    return neighbors

def hill_climb(n, max_steps=1000):
    board = random_board(n)
    steps = 0
    while steps < max_steps:
        current_h = compute_heuristic(board)
        if current_h == 0:
            return board, steps, True
        neighbors = get_neighbors(board)
        neighbor_h = [compute_heuristic(nb) for nb in neighbors]
        min_h = min(neighbor_h)
        if min_h >= current_h:
            return board, steps, False  # stuck
        board = neighbors[neighbor_h.index(min_h)]
        steps += 1
    return board, steps, False

def hill_climb_sideways(n, max_steps=1000, max_sideways=100):
    board = random_board(n)
    steps = 0
    sideways_moves = 0
    while steps < max_steps:
        current_h = compute_heuristic(board)
        if current_h == 0:
            return board, steps, True
        neighbors = get_neighbors(board)
        neighbor_h = [compute_heuristic(nb) for nb in neighbors]
        min_h = min(neighbor_h)
        if min_h < current_h:
            board = neighbors[neighbor_h.index(min_h)]
            sideways_moves = 0
        elif min_h == current_h and sideways_moves < max_sideways:
            board = neighbors[neighbor_h.index(min_h)]
            sideways_moves += 1
        else:
            return board, steps, False
        steps += 1
    return board, steps, False

def random_restart_hill_climb(n, allow_sideways=False, max_restarts=1000):
    restarts = 0
    total_steps = 0
    while restarts < max_restarts:
        if allow_sideways:
            board, steps, success = hill_climb_sideways(n)
        else:
            board, steps, success = hill_climb(n)
        total_steps += steps
        if success:
            return board, restarts, total_steps, True
        restarts += 1
    return board, restarts, total_steps, False

def show_sequences(n):
    print("\n===== Example Search Sequences (4 Random Configurations) =====")
    for algo_name, func in [
        ("Hill Climbing", hill_climb),
        ("Hill Climbing with Sideways", hill_climb_sideways)
    ]:
        print(f"\n--- {algo_name} ---")
        for i in range(4):
            board = random_board(n)
            print(f"\nInitial {i+1}: {board}, h={compute_heuristic(board)}")
            steps = 0
            while steps < 50:  # Limit to avoid long loops
                current_h = compute_heuristic(board)
                if current_h == 0:
                    print(f"Solution found in {steps} steps -> {board}")
                    break
                neighbors = get_neighbors(board)
                h_values = [compute_heuristic(nb) for nb in neighbors]
                min_h = min(h_values)
                if min_h >= current_h:
                    print(f"Stopped at step {steps} -> {board}, h={current_h}")
                    break
                board = neighbors[h_values.index(min_h)]
                steps += 1

def experiment(n=8, runs=[50, 100, 200, 500, 1000, 1500]):
    print(f"\n===== N-Queens Hill Climbing Experiments (N={n}) =====")

    # Show 4 example sequences first
    show_sequences(n)

    # Main experiments (success/failure rate)
    for algo_name, func in [
        ("Hill Climbing", hill_climb),
        ("Hill Climbing with Sideways", hill_climb_sideways),
    ]:
        print(f"\n### {algo_name} ###")
        for r in runs:
            success_steps = []
            fail_steps = []
            success_count = 0
            for _ in range(r):
                _, steps, success = func(n)
                if success:
                    success_count += 1
                    success_steps.append(steps)
                else:
                    fail_steps.append(steps)
            print(f"Runs: {r}")
            success_rate = success_count / r * 100
            failure_rate = 100 - success_rate
            print(f"Success Rate: {success_rate:.2f}%")
            print(f"Failure Rate: {failure_rate:.2f}%")
            if success_steps:
                print(f"Avg Steps (Success): {statistics.mean(success_steps):.2f}")
            if fail_steps:
                print(f"Avg Steps (Fail): {statistics.mean(fail_steps):.2f}")
            print("-" * 40)

    # Random-Restart Experiments (for your table)
    print("\n### Random-Restart Hill Climbing Summary ###")
    for r in runs:
        restarts_no_sideways = []
        steps_no_sideways = []
        restarts_with_sideways = []
        steps_with_sideways = []

        # Without sideways
        for _ in range(r):
            _, restarts, steps, _ = random_restart_hill_climb(n, allow_sideways=False)
            restarts_no_sideways.append(restarts)
            steps_no_sideways.append(steps)

        # With sideways
        for _ in range(r):
            _, restarts, steps, _ = random_restart_hill_climb(n, allow_sideways=True)
            restarts_with_sideways.append(restarts)
            steps_with_sideways.append(steps)

        # Calculate averages
        avg_restarts_no_sideways = statistics.mean(restarts_no_sideways)
        avg_steps_no_sideways = statistics.mean(steps_no_sideways)
        avg_restarts_with_sideways = statistics.mean(restarts_with_sideways)
        avg_steps_with_sideways = statistics.mean(steps_with_sideways)

        # Print results like your image
        print(f"\n=== Results for {r} Runs ===")
        print(f"The average number of random restarts required without sideways move: {avg_restarts_no_sideways:.2f}")
        print(f"The average number of steps required without sideways move: {avg_steps_no_sideways:.2f}")
        print(f"The average number of random restarts used with sideways move: {avg_restarts_with_sideways:.2f}")
        print(f"The average number of steps required with sideways move: {avg_steps_with_sideways:.2f}")
        print("-" * 80)

if __name__ == "__main__":
    n = int(input("Enter value of N (e.g., 8): "))
    experiment(n)
