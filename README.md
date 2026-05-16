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


### Iteration 12 - Add a stable block pattern
In this version, I added `block_grid`, which is a still-life pattern.

Unlike the blinker or glider, the block does not move or oscillate. 
It stays the same because each live cell has exactly 3 live neighbors, 
so every live cell survives and no surrounding dead cell has exactly 3 neighbors.

This also tests the improvement from the previous iteration. I only added 
the pattern to the `patterns` dictionary, and the help text now includes it automatically.

### Iteration 13 - Show live cell count
In this version, I added `count_live_cells(grid)`.

This function scans the whole grid and counts how many cells are alive in the current generation.

Now each frame prints both the generation number and the live cell count. 
This gives me a tiny measurement layer on top of the visual output.

For example:

- the block stays at 4 live cells
- the blinker stays at 3 live cells
- the glider usually stays at 5 live cells while moving

This connects to a systems idea: sometimes visual output is useful, but adding a small numeric signal makes behavior easier to verify.


### Iteration 14 - Choose the display delay
In this version, I added a third command-line argument for the delay between generations.

Now I can run:

```bash
python3 conway.py glider 40 0.2
python3 conway.py block 5 1
```

The delay controls only how fast the frames are displayed. It does not change the grid, the neighbor counting, or Conway's rules.

This is a useful separation: simulation behavior and display timing are related when I watch the program, but they are not the same part of the logic.

### Iteration 15 - Add no-clear mode
In this version, I added a `--no-clear` option.

Normally the program clears the terminal before each generation,
 which makes the animation easier to watch. But for debugging, 
 logs, and documentation, it is useful to keep every generation visible.

Now I can run:

```bash
python3 conway.py blinker 4 0 --no-clear
```


This prints each generation one after another. It makes the blinker easier 
to inspect because I can see the vertical and horizontal states in the same terminal output.

### Iteration 16 - Detect live cells on the grid edge
In this version, I added `has_live_cell_on_edge(grid)`.

The current Conway world is finite. That means the cells outside the grid are 
treated as dead because the neighbor-counting logic ignores positions outside the boundary.

This matters most for the glider. A glider moves across the grid, and once it 
touches the edge, its behavior can change because it no longer has the same space around it.

The new output tells me whether any live cell is touching the boundary of the grid.


### Iteration 17 - Stop when all cells are dead
In this version, I added an early stop condition.

If `count_live_cells(current_grid)` becomes 0, then the simulation stops because an empty grid will stay empty forever.

I also added a `lonely` pattern with one live cell. 
In Conway's rules, a single live cell has no live neighbors, so it dies after one generation.

Now I can test that behavior with:

```bash
python3 conway.py lonely 5 0 --no-clear
```

This is a small optimization and also a state-machine lesson: once the system reaches a terminal state, there is no useful future work to compute.

### Iteration 18 - Stop when the grid becomes stable
In this version, I added stable-state detection.

After printing the current generation, the program computes `next_grid`. If `next_grid == current_grid`, then the state has reached a fixed point.

That means applying Conway's rules again will not change anything, so the simulation can stop early.

This is useful for the `block` pattern:

```bash
python3 conway.py block 10 0 --no-clear
```


The block is a still-life pattern, so the program should print it once and then stop because the next generation is identical.

### Iteration 19 - Detect repeating cycles
In this version, I added cycle detection.

A stable grid is one kind of repeated state, but there are also oscillators like 
the blinker. The blinker does not stay fixed, but it returns to an earlier state after a few generations.

I added `grid_to_key(grid)` so each grid can be converted into a tuple and stored in a `set`.

Now the simulation remembers previous states. If the current grid has been seen before, the program stops because the future will repeat from that point.

This is useful for testing the blinker:

```bash
python3 conway.py blinker 10 0 --no-clear
```

### Iteration 20 - Explain one cell decision
In this version, I added a small debugging/explanation function called `explain_cell(grid, row_index, col_index)`.

The full grid can look complex, but each generation is made from one-cell decisions. For one selected cell, the program now prints:

- whether the cell is currently alive or dead
- how many live neighbors it has
- whether it will be alive or dead in the next generation

This helps connect the visual grid back to Conway's rules. 
If I can understand one cell's transition, then the full grid is just the same logic repeated across every cell.


### Iteration 21 - Choose which cell to explain
In this version, I made the cell explanation configurable from the command line.

Earlier, the program always explained the center cell. 
Now I can choose a specific row and column:

```bash
python3 conway.py blinker 3 0 --no-clear --explain 2 2
```

### Iteration 22 - Show grid size
In this version, I added `grid_size_text(grid)`.

The program now prints the grid dimensions with each generation, for example `5x5` or `10x10`.

This matters because different patterns use different grid sizes. 
The blinker is small, the glider needs more room to move, and the block is a separate still-life example.

This is also a memory-layout idea: before scanning a grid, I should understand its shape.



