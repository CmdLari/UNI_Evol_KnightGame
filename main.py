import pygame
import random
from typing import List

from chessset.board import Board
from differentialEvolution.differentialEvolution import Individual
from differentialEvolution.differentialEvolution import DifferentialEvolution

class Main:
    BOARD_SIZE = 3
    def __init__(self) -> None:
        '''Initialize the main game with a board and a knight'''
        pygame.init()

        # Set up base parameters
        self.BOARD_WIDTH = self.BOARD_SIZE
        self.BOARD_HEIGHT = self.BOARD_SIZE
        self.OBSTACLES: bool = False
        self.POPULATION_SIZE: int = self.BOARD_WIDTH * self.BOARD_HEIGHT
        self.GENERATIONS: int = self.BOARD_WIDTH * self.BOARD_HEIGHT * 10
        self.STEPSIZE_PARAM = 0.5
        self.CROSSOVER_RATE: float = 0.9
        self.STEPS: int = self.BOARD_WIDTH * self.BOARD_HEIGHT * 2

        # Randomly select a starting position for the knight
        self.starting_position: List[int] = [
            random.randint(0, self.BOARD_WIDTH - 1),
            random.randint(0, self.BOARD_HEIGHT - 1)
        ]

        # Set up base game
        self.screen: pygame.Surface = pygame.display.set_mode(
            (self.BOARD_WIDTH * 50, self.BOARD_HEIGHT * 50)
        )
        pygame.display.set_caption("Knight's Tour")
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.running: bool = True

        self.board: Board = Board(self.screen, self.BOARD_WIDTH, self.BOARD_HEIGHT, self.starting_position, self.OBSTACLES)

        ## SHOW PONY ##
        self.knight: Individual = None

        self.de = DifferentialEvolution(self.POPULATION_SIZE, self.board, self.GENERATIONS, self.STEPSIZE_PARAM, self.CROSSOVER_RATE, self.STEPS)
        self.best_path = []
        self.current_step = 0
        self.is_over: bool = False

    def run(self) -> None:
        while self.running:
            self._check_events()

            self.screen.fill((255, 255, 255))
            self.board.draw_board(self.knight)
            self.knight.draw_knight(self.screen)
        
            if self.current_step < len(self.best_path):
                dx, dy = self.best_path[self.current_step]
                self.knight.move_for_show(dx, dy)
                self.current_step += 1
            else:
                self.is_over = True
            if self.is_over:
                font = pygame.font.Font("assets\Jersey10-Regular.ttf", 35)
                text = font.render("XO", True, (215, 228, 222))
                text_rect = text.get_rect(center=(self.BOARD_WIDTH * 25, self.BOARD_HEIGHT * 25))
                textbg_rect = pygame.Rect(
                    text_rect.x - 10, text_rect.y - 10,
                    text_rect.width + 20, text_rect.height + 20
                )
                self.screen.fill((42, 42, 30), textbg_rect)
                self.screen.blit(text, text_rect)
                

            pygame.display.flip()
            self.clock.tick(60) # Adjust speed of the game to generation size

    def _check_events(self) -> None:
        '''Check for events and handle them'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def solve_with_de(self) -> None:
        self.de.run()
        print("Best fitness:", self.de.best.fitness)
        print("Worst fitness:", self.de.worst.fitness)
        print(self.de.best.visited_tiles)
        print(self.de.worst.visited_tiles)
        self.knight = self.de.best
        self.best_path = self.de.best.visited_tiles
        self.knight.position = self.starting_position.copy()
        self.board.visited_positions = set()

if __name__ == "__main__":
    game = Main()
    game.solve_with_de()
    game.run()
    pygame.quit()
