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

- `main.py` — Entry point for the application

- `chessset/` — Board and game logic

  - `board.py` — Handles board layout and rendering
  - `field.py` — Represents individual board tiles
  - `utils.py` — Image loading and helper functions

- `differentialEvolution/` — Evolutionary algorithm components

  - `differentialEvolution.py` — Main DE algorithm loop
  - `individual.py` — Individual representation with vector + fitness (represents the knight)
  - `population.py` — Manages a population of individuals

- `assets/` — provides the graphical assets and fonts

## Fitness Evaluation

Fitness is calculated based on:

### Positive

- Valid moves
- New tiles visited

### Negative

- Re-visiting tiles
- Hitting obstacles
- Going off the board

## Parameters

POPULATION_SIZE: number of individuals

GENERATIONS: evolution cycles

CROSSOVER_RATE: probability of mixing individuals

STEPSIZE_PARAM (F): mutation scaling factor

STEPS: number of moves per individual

You can adjust these in main.py.

## TO-DOs

- Create a **simulation factory** to run large batches automatically

- **Export results** to `.txt`, `.csv`, or other formats

  - results should contain: [Obstacles Y/N | Board-Size | Population Size | Number of Generations | Step Size | Crossover Rate | Number of Steps | Best Fitness | Worst Fitness | Average Fitness]

- **Visualize** (Potentially via Numpy?) the results (Take Average of Big Numbers)

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
