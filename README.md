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

Iteration 1 - Static grid renderer
In the first version, I only represent a 5x5 grid using 0 and 1.

- 0 means a dead cell
- 1 means a live cell
- . is printed for a dead cell
- `#` is printed for a live cell

At this stage, there are no Conway rules yet. The goal is only to understand the grid as memory and the print loop as scanning that memory.