from differentialEvolution.individual import Individual
import random
from typing import List, Tuple

class Population:
    def __init__(self, size, vector_length, bounds):
        self.individuals = [self._random_individual(vector_length, bounds) for _ in range(size)]

    def _random_individual(self, length, bounds):
        vector = [random.uniform(bounds[i][0], bounds[i][1]) for i in range(length)]
        return Individual(vector)
