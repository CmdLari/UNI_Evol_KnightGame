import pygame
import random
from typing import List
from datetime import datetime
import time

from utils import (draw_board, save_results_to_json, plot_fitness_over_generations, process_accumulated_runs)
from chessset.board import Board
from differentialEvolution.differentialEvolution import Individual
from differentialEvolution.differentialEvolution import DifferentialEvolution

class Main:
    BOARD_SIZE = 8
    NUMBER_OF_RUNS = 5
    DOCUMENT_GENERATIONS: bool = True
    SHOW_PONY: bool = True
    def __init__(self) -> None:
        '''Initialize the main game with a board and a knight'''
        pygame.init()

        # Set up base parameters
        self.BOARD_WIDTH = self.BOARD_SIZE
        self.BOARD_HEIGHT = self.BOARD_SIZE
        self.OBSTACLES: bool = False
        self.ELITISM: bool = False
        self.ELITISM_RATE: float = 0.3
        self.POPULATION_SIZE: int = self.BOARD_WIDTH * self.BOARD_HEIGHT
        self.GENERATIONS: int = self.BOARD_WIDTH * self.BOARD_HEIGHT * 10
        self.STEPSIZE_PARAM = 0.5
        self.CROSSOVER_RATE: float = 0.9
        self.STEPS: int = self.BOARD_WIDTH * self.BOARD_HEIGHT * 5

        # Randomly select a starting position for the knight
        self.starting_position: List[int] = [
            random.randint(0, self.BOARD_WIDTH - 1),
            random.randint(0, self.BOARD_HEIGHT - 1)
        ]

        self.board: Board = Board(self.BOARD_WIDTH, self.BOARD_HEIGHT, self.starting_position, self.OBSTACLES)

        ## SHOW PONY ##
        self.knight: Individual = None

        self.de = DifferentialEvolution(self.POPULATION_SIZE, self.board, self.GENERATIONS, self.STEPSIZE_PARAM, self.CROSSOVER_RATE, self.STEPS, self.ELITISM, self.ELITISM_RATE)
        self.best_path = []
        self.current_step = 0
        self.is_over: bool = False

    def visualize(self) -> None:
        # Set up base game
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
            draw_board(self.screen, self.board,self.knight, ctr)
            if not self.is_over and ctr < len(self.best_path)-1:
                ctr += 1

            if self.current_step < len(self.best_path):
                dx, dy = self.best_path[self.current_step]
                self.knight.move_for_show(dx, dy)
                self.current_step += 1
            else:
                self.is_over = True
            if self.is_over:
                font = pygame.font.Font("assets\Jersey10-Regular.ttf", 35)
                text = font.render("DONE", True, (215, 228, 222))
                text_rect = text.get_rect(center=(self.BOARD_WIDTH * 25, self.BOARD_HEIGHT * 25))
                textbg_rect = pygame.Rect(
                    text_rect.x - 10, text_rect.y - 10,
                    text_rect.width + 20, text_rect.height + 20
                )
                self.screen.fill((42, 42, 30), textbg_rect)
                self.screen.blit(text, text_rect)
                

            pygame.display.flip()
            self.clock.tick(5) # Adjust speed of the game to generation size

    def _check_events(self) -> None:
        '''Check for events and handle them'''
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
        print ("Average fitness:", sum(ind.fitness for ind in self.de.population.individuals) / len(self.de.population.individuals))
        print (self.de.best.attempted_moves)
        self.knight = self.de.best
        self.best_path = self.de.best.visited_tiles
        self.knight.position = self.starting_position.copy()
        self.board.visited_positions = set()

if __name__ == "__main__":
    game = Main()
    #not starting time
    start = time.time()
    for _ in range(game.NUMBER_OF_RUNS):
        game.solve_with_de()
        # Save results to JSON for later analysis
        full_path = save_results_to_json(game,{
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
        # plot fitness of ONE de
        if game.DOCUMENT_GENERATIONS:
            plot_fitness_over_generations(game.de.filename, game.de)
        game.de = DifferentialEvolution(game.POPULATION_SIZE, game.board, game.GENERATIONS, game.STEPSIZE_PARAM, game.CROSSOVER_RATE, game.STEPS)
    end = time.time()
    # reduce time to minute (3 floating point)
    time_in_minutes = round((end - start) / 60, 3)
    time_per_run = round(time_in_minutes / game.NUMBER_OF_RUNS, 3)
    # Process accumulated runs
    process_accumulated_runs(full_path, time_per_run)
    if game.SHOW_PONY:
        game.visualize() # Comment this line to skip visualization - shows LAST run of the knight tour
    pygame.quit()
