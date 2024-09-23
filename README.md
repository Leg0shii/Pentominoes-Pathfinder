# Pentominoes Pathfinding

This is an optimization project where the goal is to maximize the path length by fitting pentominoes into a grid and then choosing the shortest path between the start and end points.
Inspiration: https://www.youtube.com/watch?v=39YYZcwCuv0

### Getting Started
To understand the problem better, I played around with pentomino puzzles online. The idea is to figure out a way to algorithmically solve this or maybe brute-force through it. Fitting all possible pentominoes sounds way too computationally heavy.

### Approach #1: Brute Force
I started by trying to generate all possible longest paths first and then fitting the pentominoes into the remaining spaces.

- **First Idea:** Generate all possible combinations of path blocks and space blocks. Check if the configuration is valid, and then find a layout that fits the pentominoes and maintains the path.
- **Issue:** This doesn’t scale. For example, a 5x5 grid has around 43.6 billion possible 17-path-long configurations, which is just insane to handle.

<img src="https://github.com/user-attachments/assets/9107c937-09db-46ca-b339-0430de3ec047" width="300" height="400"/>

### Approach #2: Pathfinding
I tried multiple DFS variants, with the final one being a greedy DFS using a heuristic based on distance from the center. It worked okay for small grids, but performance tanked on larger ones.

- **Problem:** 7x7 grids took over 100 seconds even with optimizations. Bigger grids are out of reach for this method. I then looked into MILP (Mixed Integer Linear Programming) to see if formulating the problem with constraints and using a solver would work.

### Approach #3: MILP for Pentominoes Fitting
I tried implementing MILP directly on pentomino fitting but hit a wall. It was too complex, and I couldn’t debug it properly. I had to scale down multiple times, and it still didn’t work. It is however promising as it can find complex solutions quite quickly, but modelling my problem in constraints and now using too many constraints is were the challenge arises. This 12x12 grid took the same time the 7x7 took and considering more than exponential groth, this is very astonishing.

<img src="https://github.com/user-attachments/assets/cd82097b-93ef-48ce-8049-5412ced03392" width="600" height="400"/>

### Where the Project is Heading
Right now, I’m still looking for a good way to tackle this problem. Possible ideas revolve around getting deeper into MILP to optimize number of constraints or attempting different pruning approaches. My goal would be to optimally solve an 8x8 grid with pentomino fittings as this would be above the current best algorithm.
