# Conway's Game of Life - Iteration 1
# Goal: represent a grid and print it with simple terminal graphics

grid = [
    [0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0],
]

# We visit each row then each cell inside that row
for row in grid:
    line = ""

    for cell in row:
        if cell == 1:
            line += "#"
        else:
            line += "."

    print(line)
