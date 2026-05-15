# Conway's Game of Life - Iteration 2
# Goal: separate the grid data from the display logic

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

print_grid(grid)
