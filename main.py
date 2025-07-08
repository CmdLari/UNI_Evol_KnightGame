import pygame
import random
from typing import List
import time
import argparse
import cmath
from math import sqrt

from utils import (draw_board, save_results_to_json, plot_fitness_over_generations, process_accumulated_runs)
from chessset.board import Board
from differentialEvolution.differentialEvolution import Individual
from differentialEvolution.differentialEvolution import DifferentialEvolution

def str2bool(v):
    return str(v).lower() in ("yes", "true", "t", "1")

class Main:

    def __init__(self, BOARD_SIZE: int = 4, NUMBER_OF_RUNS: int = 100, 
                 DOCUMENT_GENERATIONS: bool = False, SHOW_PONY: bool = True, 
                 CROSSOVER_RATE: float = 0.9, STEPSIZE_PARAM: float = 0.5, OBSTACLES: bool = False, 
                 ELITISM: bool = False, ELITISM_RATE: float = 0.1, POPULATION_SIZE: int = 100, 
                 GENERATIONS: int = 100, STEPS: int = 100) -> None:
        if SHOW_PONY:
            pygame.init()

        self.BOARD_SIZE = BOARD_SIZE
        self.NUMBER_OF_RUNS = NUMBER_OF_RUNS
        self.DOCUMENT_GENERATIONS = DOCUMENT_GENERATIONS
        self.SHOW_PONY = SHOW_PONY
        self.CROSSOVER_RATE = CROSSOVER_RATE
        self.STEPSIZE_PARAM = STEPSIZE_PARAM
        self.OBSTACLES = OBSTACLES
        self.ELITISM = ELITISM
        self.ELITISM_RATE = ELITISM_RATE
        self.POPULATION_SIZE = POPULATION_SIZE
        self.GENERATIONS = GENERATIONS
        self.STEPS = STEPS

        self.BOARD_WIDTH = int(sqrt(self.BOARD_SIZE))
        self.BOARD_HEIGHT = int(sqrt(self.BOARD_SIZE))

        self.starting_position: List[int] = [
            random.randint(0, self.BOARD_WIDTH - 1),
            random.randint(0, self.BOARD_HEIGHT - 1)
        ]

        self.board: Board = Board(self.BOARD_WIDTH, self.BOARD_HEIGHT, self.starting_position, self.OBSTACLES)
        self.knight: Individual = None
        self.de = DifferentialEvolution(self.POPULATION_SIZE, self.board, self.GENERATIONS, self.STEPSIZE_PARAM, self.CROSSOVER_RATE, self.STEPS, self.ELITISM, self.ELITISM_RATE)

        self.best_path = []
        self.current_step = 0
        self.is_over: bool = False

    def visualize(self) -> None:
        self.screen: pygame.Surface = pygame.display.set_mode(
            (self.BOARD_WIDTH * 50, self.BOARD_HEIGHT * 50)
        )
        pygame.display.set_caption("Knight's Tour")
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.running: bool = True

        ctr = 0
        while self.running:
            self._check_events()

            self.screen.fill((255, 255, 255))
            draw_board(self.screen, self.board, self.knight, ctr)
            if not self.is_over and ctr < len(self.best_path) - 1:
                ctr += 1

            if self.current_step < len(self.best_path):
                dx, dy = self.best_path[self.current_step]
                self.knight.move_for_show(dx, dy)
                self.current_step += 1
            else:
                self.is_over = True

            if self.is_over:
                font = pygame.font.Font("assets/Jersey10-Regular.ttf", 35)
                text = font.render("DONE", True, (215, 228, 222))
                text_rect = text.get_rect(center=(self.BOARD_WIDTH * 25, self.BOARD_HEIGHT * 25))
                textbg_rect = pygame.Rect(
                    text_rect.x - 10, text_rect.y - 10,
                    text_rect.width + 20, text_rect.height + 20
                )
                self.screen.fill((42, 42, 30), textbg_rect)
                self.screen.blit(text, text_rect)

            pygame.display.flip()
            self.clock.tick(5)

    def _check_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def solve_with_de(self) -> None:
        self.de.run(self.DOCUMENT_GENERATIONS)
        print("Best fitness:", self.de.best.fitness)
        print("Worst fitness:", self.de.worst.fitness)
        print("Average fitness:", sum(ind.fitness for ind in self.de.population.individuals) / len(self.de.population.individuals))
        print(self.de.best.attempted_moves)

        self.knight = self.de.best
        self.best_path = self.de.best.visited_tiles
        self.knight.position = self.starting_position.copy()
        self.board.visited_positions = set()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--BOARD_SIZE", type=int, default=64)
    parser.add_argument("--NUMBER_OF_RUNS", type=int, default=1)
    parser.add_argument("--DOCUMENT_GENERATIONS", type=str2bool, default=False)
    parser.add_argument("--SHOW_PONY", type=str2bool, default=False)
    parser.add_argument("--CROSSOVER_RATE", type=float, default=0.9)
    parser.add_argument("--STEPSIZE_PARAM", type=float, default=0.5)
    parser.add_argument("--OBSTACLES", type=str2bool, default=False)
    parser.add_argument("--ELITISM", type=str2bool, default=True)
    parser.add_argument("--ELITISM_RATE", type=float, default=0.2)
    parser.add_argument("--POPULATION_SIZE", type=int, default=None)
    parser.add_argument("--GENERATIONS", type=int, default=None)
    parser.add_argument("--STEPS", type=int, default=None)
    args = parser.parse_args()

    if args.POPULATION_SIZE is None:
        args.POPULATION_SIZE = args.BOARD_SIZE * 2
    if args.GENERATIONS is None:
        args.GENERATIONS = args.BOARD_SIZE * 20
    if args.STEPS is None:
        args.STEPS = args.BOARD_SIZE * 3

    game = Main(**vars(args))

    start = time.time()
    for _ in range(game.NUMBER_OF_RUNS):
        game.solve_with_de()
        full_path = save_results_to_json(game, {
            "board_size": game.BOARD_HEIGHT * game.BOARD_WIDTH,
            "obstacles": game.OBSTACLES,
            "population_size": game.POPULATION_SIZE,
            "generations": game.GENERATIONS,
            "stepsize_param": game.STEPSIZE_PARAM,
            "crossover_rate": game.CROSSOVER_RATE,
            "steps": game.STEPS,
            "best_fitness": game.de.best.fitness,
            "best_fitness_per_step": game.de.best.fitness / game.STEPS,
            "worst_fitness": game.de.worst.fitness,
            "worst_fitness_per_step": game.de.worst.fitness / game.STEPS,
            "average_fitness": sum(ind.fitness for ind in game.de.population.individuals) / len(game.de.population.individuals),
            "average_fitness_per_step": sum(ind.fitness for ind in game.de.population.individuals) / len(game.de.population.individuals) / game.STEPS,
            "best_attempted_moves": game.de.best.attempted_moves
        })

        if game.DOCUMENT_GENERATIONS:
            plot_fitness_over_generations(game.de.filename, game.de)

        solved = len(game.de.best.visited_tiles) == game.BOARD_SIZE
        print(game.de.best.visited_tiles)
        game.de = DifferentialEvolution(game.POPULATION_SIZE, game.board, game.GENERATIONS, game.STEPSIZE_PARAM, game.CROSSOVER_RATE, game.STEPS, game.ELITISM, game.ELITISM_RATE)

    end = time.time()
    time_in_minutes = round((end - start) / 60, 3)
    time_per_run = round(time_in_minutes / game.NUMBER_OF_RUNS, 3)

    process_accumulated_runs(game, full_path, time_per_run, solved)

    if game.SHOW_PONY:
        game.visualize()

    if game.SHOW_PONY:
        pygame.quit()
