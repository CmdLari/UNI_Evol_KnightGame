from differentialEvolution.individual import Individual
import random

class Population:
    def __init__(self, size, board):
        self.individuals = [self._random_individual(board) for _ in range(size)]

    def _random_individual(self, board):
        position = [random.randint(0, board.width - 1), random.randint(0, board.height - 1)]
        return Individual(position, board.width, board.height )
