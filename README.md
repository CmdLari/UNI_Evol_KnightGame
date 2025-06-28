# Knight's Tour with Differential Evolution

This project is a simulation of the **Knight's Tour problem** on a customizable chessboard using a **Differential Evolution (DE)** algorithm.
The goal is to guide a knight to visit as many unique tiles as possible, avoiding obstacles and staying within bounds.

## Features

- 2D graphical board using **Pygame**
- Dynamic obstacle generation (optional)
- Knight tour guided by an **Differential-Evolution Algorithm**
- Fitness evaluation based on tile visitation, legality, and obstacle avoidance
- Modular architecture for evolution, visualization, and logic

## Project Structure

- `main.py` - Entry point for the application

- `chessset/` - Board and game logic

  - `board.py` - Handles board layout and rendering
  - `field.py` - Represents individual board tiles

- `differentialEvolution/` - Evolutionary algorithm components

  - `differentialEvolution.py` - Main DE algorithm loop
  - `individual.py` - Individual representation with vector + fitness (represents the knight)
  - `population.py` - Manages a population of individuals

- `utils.py` - Image loading, tour visualisation, result dump

- `assets/` - provides the graphical assets and fonts
- `results/` - contains json dumps of knight tours
  - `results/` contains averages calculated from acumulating runs
  - `results/<date>_gen_doc_<details>` contains documentation for each generation of a run, as well as the accumulated runs

## Fitness Evaluation

Fitness is calculated based on:

### Positive

- Valid moves
- New tiles visited
- all tiles have been visited

### Negative

- Re-visiting tiles
- Hitting obstacles
- Going off the board
- unnecessarily high number of moves

## Parameters

- **SHOW_PONY:** Use pygame to visualize the latest iteration of the algorithm
- **BOARD_SIZE:** Sets lenght AND width of board
- **NUMBER_OF_RUNS:** How many times is a board solved by the DE
- **DOCUMENT_GENERATIONS:** Is EVERY Generation of EVERY run documented (for graphs eg)
- **BOARD_WIDTH:** Set to BOARD_SIZE (could be used for non square boards)
- **BOARD_HEIGHT:** Set to BOARD_SIZE (could be used for non square boards)
- **POPULATION_SIZE:** number of individuals
- **GENERATIONS:** evolution cycles
- **CROSSOVER_RATE:** probability of mixing individuals
- **STEPSIZE_PARAM (F):** mutation scaling factor
- **STEPS:** number of moves per individual

You can adjust these in main.py.

## TO-DOs

- Compare DE performance when varying **one parameter at a time**:

  - Population size
  - Number of generations
  - Step size (`F`)
  - Crossover rate (`CR`)
  - Number of knight steps

- Evaluate best configurations across:

  - 3 different board sizes
  - Obstacle mode: `obstacles = True`

- Implement **elitism**
- Repeat all above benchmarks with elitism enabled
