# Conway's Game of Life - Iteration 14
# Goal: choose the display delay from the command line

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

patterns = {
    "blinker": blinker_grid,
    "glider": glider_grid,
    "block": block_grid,
}

def print_usage():
    available_patterns = ", ".join(patterns)

    print("Usage: python3 conway.py [pattern] [generations] [delay]")
    print("Patterns:", available_patterns)
    print("Example: python3 conway.py glider 40 0.5")

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


def run_simulation(starting_grid, generations, delay):
    current_grid = starting_grid

    # This outer loop is the simulation clock
    # Each pass shows one generation and then computes the next one
    for generation in range(generations):
        os.system("clear")

        print("Generation:", generation, "| Live cells:", count_live_cells(current_grid))
        print_grid(current_grid)

        time.sleep(delay)

        current_grid = next_generation(current_grid)


def main():
    pattern_name = "glider"
    generations = 20
    delay = 0.5

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
    
    if delay < 0:
        print("Delay cannot be negative.")
        print_usage()
        return

    if pattern_name not in patterns:
        print("Unknown pattern:", pattern_name)
        print_usage()
        return

    run_simulation(patterns[pattern_name], generations, delay)




if __name__ == "__main__":
    main()

