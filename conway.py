# Conway's Game of Life - Iteration 21
# Goal: choose which cell to explain from the command line

import os
import sys
import time

blinker_grid = [
    [0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0],
]

glider_grid = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

block_grid = [
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 0, 0],
    [0, 0, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
]

lonely_cell_grid = [
    [0, 0, 0],
    [0, 1, 0],
    [0, 0, 0],
]

patterns = {
    "blinker": blinker_grid,
    "glider": glider_grid,
    "block": block_grid,
    "lonely": lonely_cell_grid,
}

def print_usage():
    available_patterns = ", ".join(patterns)

    print("Usage: python3 conway.py [pattern] [generations] [delay] [--no-clear] [--explain row col]")
    print("Patterns:", available_patterns)
    print("Example: python3 conway.py glider 40 0.5 --no-clear --explain 2 2")

def print_grid(grid):
    # We scan the grid row by row, then cell by cell
    for row in grid:
        line = ""

        for cell in row:
            if cell == 1:
                line += "#"
            else:
                line += "."

        print(line)

def count_live_cells(grid):
    live_cells = 0

    # We scan the whole grid and count every cell that is alive
    for row in grid:
        for cell in row:
            live_cells += cell

    return live_cells

def has_live_cell_on_edge(grid):
    last_row_index = len(grid) - 1
    last_col_index = len(grid[0]) - 1

    # We check every cell and report if a live cell is on the boundary
    for row_index in range(len(grid)):
        for col_index in range(len(grid[0])):
            is_live = grid[row_index][col_index] == 1
            is_edge = (
                row_index == 0
                or row_index == last_row_index
                or col_index == 0
                or col_index == last_col_index
            )

            if is_live and is_edge:
                return True

    return False

def grid_to_key(grid):
    rows = []

    # Convert the grid into a tuple so it can be stored in a set
    for row in grid:
        rows.append(tuple(row))

    return tuple(rows)

def count_live_neighbors(grid, row_index, col_index):
    live_neighbors = 0

    neighbor_offsets = [
        [-1, -1], [-1, 0], [-1, 1],
        [0, -1],           [0, 1],
        [1, -1],  [1, 0],  [1, 1],
    ]

    # For one cell we inspect the 8 nearby positions around it
    for row_offset, col_offset in neighbor_offsets:
        neighbor_row = row_index + row_offset
        neighbor_col = col_index + col_offset

        row_is_inside = 0 <= neighbor_row < len(grid)
        col_is_inside = 0 <= neighbor_col < len(grid[0])

        if row_is_inside and col_is_inside:
            live_neighbors += grid[neighbor_row][neighbor_col]

    return live_neighbors


def next_cell_state(current_cell, live_neighbors):
    # CONWAY RULES:
    # A live cell survives only with 2 or 3 live neighbors.
    if current_cell == 1:
        if live_neighbors == 2 or live_neighbors == 3:
            return 1
        return 0

    # A dead cell becomes alive only with exactly 3 live neighbors.
    if live_neighbors == 3:
        return 1

    return 0

def cell_state_name(cell):
    if cell == 1:
        return "alive"

    return "dead"

def next_generation(current_grid):
    next_grid = []

    # We scan every cell in the current grid and compute its next state
    for row_index in range(len(current_grid)):
        next_row = []

        for col_index in range(len(current_grid[0])):
            current_cell = current_grid[row_index][col_index]
            live_neighbors = count_live_neighbors(
                current_grid,
                row_index,
                col_index,
            )

            next_row.append(next_cell_state(current_cell, live_neighbors))

        next_grid.append(next_row)

    return next_grid

def explain_cell(grid, row_index, col_index):
    current_cell = grid[row_index][col_index]
    live_neighbors = count_live_neighbors(grid, row_index, col_index)
    next_state = next_cell_state(current_cell, live_neighbors)

    print(
        "Cell",
        "(" + str(row_index) + ", " + str(col_index) + "):",
        cell_state_name(current_cell),
        "| Live neighbors:",
        live_neighbors,
        "| Next state:",
        cell_state_name(next_state),
    )

def run_simulation(starting_grid, generations, delay, clear_screen, explain_row, explain_col):
    current_grid = starting_grid
    seen_grids = set()

    # This outer loop is the simulation clock
    # Each pass shows one generation and then computes the next one
    for generation in range(generations):
        if clear_screen:
            os.system("clear")
        
        grid_key = grid_to_key(current_grid)

        if grid_key in seen_grids:
            print("Grid has entered a repeating cycle. Stopping simulation.")
            return

        seen_grids.add(grid_key)

        if explain_row is None:
            explain_row = len(starting_grid) // 2
            explain_col = len(starting_grid[0]) // 2
        
        live_cells = count_live_cells(current_grid)
        edge_text = "yes" if has_live_cell_on_edge(current_grid) else "no"

        print(
            "Generation:",
            generation,
            "| Live cells:",
            live_cells,
            "| Touching edge:",
            edge_text,
        )
        print_grid(current_grid)
        print()

        if generation == 0:
            explain_cell(current_grid, explain_row, explain_col)
            print()
        
        if live_cells == 0:
            print("All cells are dead. Stopping simulation.")
            return


        next_grid = next_generation(current_grid)

        if next_grid == current_grid:
            print("Grid is stable. Stopping simulation.")
            return

        time.sleep(delay)

        current_grid = next_grid


def main():
    pattern_name = "glider"
    generations = 20
    delay = 0.5
    clear_screen = True
    explain_row = None
    explain_col = None

    if len(sys.argv) > 1:
        if sys.argv[1] == "--help":
            print_usage()
            return

        pattern_name = sys.argv[1]

    if len(sys.argv) > 2:
        try:
            generations = int(sys.argv[2])
        except ValueError:
            print("Generation count must be a number.")
            print_usage()
            return

    if generations < 1:
        print("Generation count must be at least 1.")
        print_usage()
        return
    
    if len(sys.argv) > 3:
        try:
            delay = float(sys.argv[3])
        except ValueError:
            print("Delay must be a number.")
            print_usage()
            return
    
    option_index = 4

    while option_index < len(sys.argv):
        option = sys.argv[option_index]

        if option == "--no-clear":
            clear_screen = False
            option_index += 1
        elif option == "--explain":
            if option_index + 2 >= len(sys.argv):
                print("--explain needs a row and column.")
                print_usage()
                return

            try:
                explain_row = int(sys.argv[option_index + 1])
                explain_col = int(sys.argv[option_index + 2])
            except ValueError:
                print("Explain row and column must be numbers.")
                print_usage()
                return

            option_index += 3
        else:
            print("Unknown option:", option)
            print_usage()
            return
    
    if delay < 0:
        print("Delay cannot be negative.")
        print_usage()
        return

    if pattern_name not in patterns:
        print("Unknown pattern:", pattern_name)
        print_usage()
        return

    selected_grid = patterns[pattern_name]

    if explain_row is not None:
        row_is_inside = 0 <= explain_row < len(selected_grid)
        col_is_inside = 0 <= explain_col < len(selected_grid[0])

        if not row_is_inside or not col_is_inside:
            print("Explain cell is outside the grid.")
            print_usage()
            return
    
    run_simulation(patterns[pattern_name], generations, delay, clear_screen, explain_row, explain_col)




if __name__ == "__main__":
    main()

