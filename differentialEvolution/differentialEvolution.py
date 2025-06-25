import random

from differentialEvolution.population import Population 
from differentialEvolution.individual import Individual

class DifferentialEvolution:
    def __init__(self, problem, pop_size, mutation_factor, crossover_rate, generations):
        self.problem = problem
        self.pop_size = pop_size
        self.mutation_factor = mutation_factor
        self.crossover_rate = crossover_rate
        self.generations = generations
        self.population = Population(pop_size, problem.vector_length, problem.bounds)
        self.best = None

    def run(self):
        for ind in self.population.individuals:
            ind.evaluate(self.problem)

        for _ in range(self.generations):
            new_population = []
            for i, target in enumerate(self.population.individuals):
                donor = self.mutate(i)
                trial = self.crossover_rateossover(target, donor)
                trial.evaluate(self.problem)
                if trial.fitness < target.fitness:
                    new_population.append(trial)
                else:
                    new_population.append(target)

            self.population.individuals = new_population
            self.best = min(new_population, key=lambda ind: ind.fitness)

    def mutate(self, target_index):
        # z. B. rand/1 strategy
        indices = list(range(self.pop_size))
        indices.remove(target_index)
        r1, r2, r3 = random.sample(indices, 3)
        x1 = self.population.individuals[r1].vector
        x2 = self.population.individuals[r2].vector
        x3 = self.population.individuals[r3].vector
        mutant = [x1[i] + self.mutation_factor * (x2[i] - x3[i]) for i in range(len(x1))]
        return Individual(mutant)

    def crossover_rateossover(self, target, donor):
        trial_vector = []
        for i in range(len(target.vector)):
            if random.random() < self.crossover_rate or i == random.randint(0, len(target.vector) - 1):
                trial_vector.append(donor.vector[i])
            else:
                trial_vector.append(target.vector[i])
        return Individual(trial_vector)
