# Conway's Game of Life - Iteration 3
# Goal: count live neighbors around one cell

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


print_grid(grid)

print()
print("Live neighbors around center cell:", count_live_neighbors(grid, 2, 2))
