import random
from datetime import datetime

from chessset import board
from differentialEvolution.population import Population
from differentialEvolution.individual import Individual
from utils import document_generation_in_json

class DifferentialEvolution:
    def __init__(self, pop_size, board, generations, stepsize_param, crossover_rate, steps, elitism, elitism_rate=0.3):
        self.pop_size = pop_size
        self.generations = generations
        self.crossover_rate = crossover_rate
        self.stepsize_param = stepsize_param
        self.elitism = elitism
        self.elitism_rate = elitism_rate
        self.board = board
        self.population = Population(pop_size, board, steps)
        self.steps = steps
        self.best = None
        self.worst = None

        self.filename = f"{datetime.now().date()}_{random.randint(1, 10000)}_generation.json"


    def run(self, document_generation=True):
        for ind in self.population.individuals:
            ind.evaluate(self.board)  # Evaluate initial fitness

        for _ in range(self.generations):
            new_population = []
            all_indices = list(range(self.pop_size))

            if not self.elitism:
                for i, target in enumerate(self.population.individuals):
                    self.mutation_crossover_evaluation_selection(i, target, new_population, all_indices)

            else:
                population_sorted = sorted(self.population.individuals, key=lambda x: x.fitness, reverse=True)
                elite_population = population_sorted[:int(self.pop_size * self.elitism_rate)]
                ctr = 0
                while ctr < (self.pop_size * self.elitism_rate)-1:
                    new_population.append(elite_population[ctr])
                    ctr += 1
                while ctr < self.pop_size:
                    for i, target in enumerate(self.population.individuals):
                        self.mutation_crossover_evaluation_selection(i, target, new_population, all_indices)
                        ctr += 1
                        if ctr == self.pop_size-1:
                            break

            self.population.individuals = new_population

            self.best = max(self.population.individuals, key=lambda x: x.fitness)
            self.worst = min(self.population.individuals, key=lambda x: x.fitness)

            if document_generation:
                document_generation_in_json(self, self.filename,
                                            self.best.fitness if self.best else 0,
                                            self.worst.fitness if self.worst else 0,
                                            sum(ind.fitness for ind in self.population.individuals) / len(self.population.individuals) if self.population.individuals else 0,
                                            self.best.attempted_moves if self.best else 0,
                                            self.steps)

    def mutation_crossover_evaluation_selection(self, i, target, new_population, all_indices):
        r1, r2, r3 = random.sample([x for x in all_indices if x != i], 3)
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