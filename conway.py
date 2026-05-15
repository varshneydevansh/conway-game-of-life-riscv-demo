# Conway's Game of Life - Iteration 4
# Goal: compute the next generation using Conway's rules

grid = [
    [0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0],
]

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


print("Current generation:")
print_grid(grid)

print()
print("Next generation:")
print_grid(next_generation(grid))
