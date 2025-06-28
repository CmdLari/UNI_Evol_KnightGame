import random
from datetime import datetime

from chessset import board
from differentialEvolution.population import Population
from differentialEvolution.individual import Individual
from utils import document_generation_in_json

class DifferentialEvolution:
    def __init__(self, pop_size, board, generations, stepsize_param, crossover_rate, steps):
        self.pop_size = pop_size
        self.generations = generations
        self.crossover_rate = crossover_rate
        self.stepsize_param = stepsize_param
        self.board = board
        self.population = Population(pop_size, board, steps)
        self.steps = steps
        self.best = None
        self.worst = None

        self.filename = f"{datetime.now().date()}_{random.randint(1, 10000)}_generation.json"


    def run(self):
        for ind in self.population.individuals:
            ind.evaluate(self.board)  # Evaluate initial fitness

        for _ in range(self.generations):
            document_generation_in_json(self.filename,
                                        self.best.fitness if self.best else 0,
                                        self.worst.fitness if self.worst else 0,
                                        sum(ind.fitness for ind in self.population.individuals) / len(self.population.individuals) if self.population.individuals else 0,
                                        self.best.attempted_moves if self.best else 0)
            new_population = []

            for i, target in enumerate(self.population.individuals):
                # --- Mutation (rand/1) ---
                indices = list(range(self.pop_size))
                indices.remove(i)
                r1, r2, r3 = random.sample(indices, 3)
                x1 = self.population.individuals[r1].vector
                x2 = self.population.individuals[r2].vector
                x3 = self.population.individuals[r3].vector

                mutant = [
                    max(0.0, min(1.0, x1[j] + self.stepsize_param * (x2[j] - x3[j])))
                    for j in range(self.steps)
                ]

                # --- Crossover ---
                trial_vector = [
                    mutant[j] if random.random() < self.crossover_rate else target.vector[j]
                    for j in range(self.steps)
                ]

                # --- Evaluation ---
                trial = Individual(trial_vector, target.starting_position, self.board.width, self.board.height, self.board)
                trial.evaluate(self.board)

                # --- Selection ---
                if trial.fitness > target.fitness:
                    new_population.append(trial)
                else:
                    new_population.append(target)

            self.population.individuals = new_population

            self.best = max(self.population.individuals, key=lambda x: x.fitness)
            self.worst = min(self.population.individuals, key=lambda x: x.fitness)
