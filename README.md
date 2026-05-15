# Conway's Game of Life

This is a small Python demonstration of Conway's Game of Life for the RISC-V mentorship coding challenge.

I am building it step by step instead of writing the final version directly, 
because I want the git history to show how the idea evolves from first principles.

The main ideas I want to understand through this demo are:

- how a grid can represent memory
- how iteration scans through rows and columns
- why the current generation and next generation must be separate
- how simple local rules can create complex behavior
- how this kind of computation could later be rewritten in C and compiled for RISC-V

## Running

```bash
python3 conway.py
```

# Iteration Log

### Iteration 1 - Static grid renderer
In the first version, I only represent a 5x5 grid using 0 and 1.

- 0 means a dead cell
- 1 means a live cell
- . is printed for a dead cell
- `#` is printed for a live cell

At this stage, there are no Conway rules yet. The goal is only to understand the grid as memory and the print loop as scanning that memory.

### Iteration 2 - Move display logic into a function
In this version, I moved the printing logic into a `print_grid(grid)` function.

The output is still the same, but the structure is better now:

- the grid stores the state
- the function knows how to display that state
- the main program can simply call `print_grid(grid)`

I am thinking of this like a tiny display module. Later, when the grid changes from one 
generation to the next, I can reuse the same function instead of rewriting the print loop.

The iteration is still visible inside the function it scans each row and then each cell inside that row.

### Iteration 3 - Count live neighbors for one cell
In this version, I added `count_live_neighbors(grid, row_index, col_index)`.

This is the first part that feels like the actual Conway machine. 
A cell does not know the whole world. It only reads the 8 nearby positions around itself.

I used `neighbor_offsets` to describe those 8 positions:

- one row above
- same row
- one row below
- one column left
- same column
- one column right

The center cell itself is skipped because a cell should not count itself as its own neighbor.

I also added boundary checks so the program does not try to read outside the grid.

For the vertical blinker pattern, the center cell has 2 live neighbors: one above it and one below it.

### Iteration 4 - Compute the next generation
In this version, I added the actual Conway rule logic.

The important idea here is that I do not modify the current grid directly. I read from `current_grid` and write into a separate `next_grid`.

This matters because all cells should observe the same generation. If I update the grid in place, then later cells would read a partially changed world.

I added two functions:

- `next_cell_state(current_cell, live_neighbors)` applies Conway's rules for one cell
- `next_generation(current_grid)` scans the full grid and builds the next grid

The vertical blinker now turns into a horizontal blinker after one generation.

### Iteration 5 - Animate multiple generations
In this version, I added a loop that runs the simulation for multiple generations.

This is where the program starts to feel like a tiny clocked system:

- print the current grid
- wait briefly
- compute the next grid
- replace the current grid with the next grid
- repeat

The outer `for generation in range(8)` loop acts like a clock. Each loop iteration is one tick of the simulation.

The blinker pattern keeps flipping between vertical and horizontal, which is 
useful because it proves the update logic is working repeatedly and not just once.

### Iteration 6 - Add a main simulation function
In this version, I moved the simulation loop into `run_simulation(starting_grid, generations)`.

The behavior is still the same, but the structure is clearer now:

- `grid` stores the starting state
- helper functions handle display, neighbor counting, and rule application
- `run_simulation` controls the repeated clock ticks
- `main` is the entry point of the script

This makes the script easier to extend later without mixing setup code and simulation code.

### Iteration 7 - Add named starting patterns
In this version, I separated the starting pattern from the simulation logic.

Earlier, the program only had one `grid`. Now I have:

- `blinker_grid`, which shows oscillation
- `glider_grid`, which shows movement across the grid

This is important because the Conway engine did not need to change. I only changed the input pattern.

That makes the code feel more like a reusable machine: different initial memory states can run through the same rules and produce different behavior.

### Iteration 8 - Choose the starting pattern from the command line
In this version, I added a small command-line choice for the starting pattern.

Now I can run:

```bash
python3 conway.py glider
python3 conway.py blinker
```

The important idea is that the Conway engine is still unchanged. 
I am only choosing a different initial memory state before starting the simulation.

This also explains why the output is predictable: there is no randomness here. 
The same pattern and the same rules will always produce the same generations.

### Iteration 9 - Choose the number of generations
In this version, I added one more command-line argument for the generation count.

Now I can run:

```bash
python3 conway.py glider 40
python3 conway.py blinker 10
```

The first argument chooses the starting pattern. 
The second argument chooses how many clock ticks the simulation should run.

This makes the program feel less hardcoded. 
The Conway rules are still the same, but I can now control the experiment from the terminal.

### Iteration 10 - Add usage help and safer command-line parsing
In this version, I added a small `print_usage()` function and validation for the generation count.

Now the program can explain itself:

```bash
python3 conway.py --help
```
I also added checks for invalid input. For example, this should not crash with a Python traceback:
- python3 conway.py glider abc


This step is less about Conway itself and more about making the script behave like a small usable tool.

### Iteration 11 - Generate help text from available patterns
In this version, I changed `print_usage()` so it reads the available pattern names from the `patterns` dictionary.

Earlier, the program had the pattern names in two places:

- inside `patterns`
- inside the help text

That kind of duplication can become a bug later. 
If I add a new pattern, I want the help text to update automatically.


