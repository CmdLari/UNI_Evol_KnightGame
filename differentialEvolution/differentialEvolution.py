import random

from chessset import board
from differentialEvolution.population import Population
from differentialEvolution.individual import Individual

class DifferentialEvolution:
    def __init__(self, pop_size, board, generations, stepsize_param, crossover_rate, steps):
        self.pop_size = pop_size
        self.generations = generations
        self.crossover_rate = crossover_rate
        self.stepsize_param = stepsize_param
        self.board = board
        self.population = Population(pop_size, board)
        self.steps = steps
        self.best = None
        self.worst = None

    def run(self):

        for _ in range(self.generations):
            new_population = []
            for ind in self.population.individuals:
                ind.move(self.board, self.steps)

                if random.random()<self.crossover_rate:
                    r1 = ind
                    r2 = ind
                    while r2 == ind:
                        r2 = self.population.individuals[random.randint(0, len(self.population.individuals) - 1)]
                    outer = min(len(r1.visited_tiles), len(r2.visited_tiles))
                    new_ind = Individual(r1.visited_tiles[0], self.board.width, self.board.height)
                    if outer >= 2:
                        for i in range(outer-1):
                            new_pos_x = r1.visited_tiles[i+1][0]-r2.visited_tiles[i+1][0]
                            new_pos_y = r1.visited_tiles[i+1][1]-r2.visited_tiles[i+1][1]
                            if ((new_pos_x-new_ind.position[0]), (new_pos_y-new_ind.position[1])) in new_ind.knight_moves:
                                new_ind.evaluate(self.board, new_pos_x, new_pos_y)
                        if new_ind.fitness > ind.fitness:
                            new_population.append(new_ind)
                        else:
                            new_population.append(ind)
                    else:
                        new_population.append(ind)
                else:
                    new_population.append(ind)
            self.population.individuals = new_population


        self.best = max(self.population.individuals, key=lambda x: x.fitness)
        self.worst = min(self.population.individuals, key=lambda x: x.fitness)



    def mutate(self, target_index):
        pass
