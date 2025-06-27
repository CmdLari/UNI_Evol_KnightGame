from differentialEvolution.individual import Individual
import random

class Population:
    def __init__(self, size: int, board, vector_length: int):
        self.individuals = [self._random_individual(board, vector_length) for _ in range(size)]

    def _random_individual(self, board, vector_length: int) -> Individual:
        position = [random.randint(0, board.width - 1), random.randint(0, board.height - 1)]
        vector = [random.random() for _ in range(vector_length)]  # values in [0.0, 1.0]
        return Individual(vector, position, board.width, board.height)
