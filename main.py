import pygame
import random
from typing import List

from chessset.board import Board
from chessset.knight import Knight
from differentialEvolution.differentialEvolution import DifferentialEvolution
from knightTourProblem import KnightTourProblem

class Main:
    def __init__(self) -> None:
        '''Initialize the main game with a board and a knight'''
        pygame.init()

        # Set up base parameters
        self.POPULATION_SIZE: int = 50
        self.GENERATIONS: int = 100
        self.MUTATION_FACTOR: float = 0.8
        self.CROSSOVER_RATE: float = 0.9
        self.BOARD_WIDTH: int = 20
        self.BOARD_HEIGHT: int = 20

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

        self.board: Board = Board(self.screen, self.BOARD_WIDTH, self.BOARD_HEIGHT, self.starting_position)
        self.knight: Knight = Knight(self.starting_position, self.BOARD_WIDTH, self.BOARD_HEIGHT)

        self.max_steps = 100  # or any step cap
        self.problem = KnightTourProblem(self.board, self.knight, self.max_steps)
        self.de = DifferentialEvolution(self.problem, self.POPULATION_SIZE, self.MUTATION_FACTOR, self.CROSSOVER_RATE, self.GENERATIONS)
        self.best_path = []
        self.current_step = 0

    def run(self) -> None:
        while self.running:
            self._check_events()

            if self.current_step < len(self.best_path):
                dx, dy = self.best_path[self.current_step]
                self.knight.move(dx, dy, self.board)
                self.current_step += 1

            self.screen.fill((255, 255, 255))
            self.board.draw_board(self.knight)

            pygame.display.flip()
            self.clock.tick(4)

    def _check_events(self) -> None:
        '''Check for events and handle them'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            ### OPTION TO MOVE THE KNIGHT USING KEYS###
            # elif event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_q:
            #         change = (-1, -2)
            #     elif event.key == pygame.K_w:
            #         change = (1, -2)
            #     elif event.key == pygame.K_a:
            #         change = (-2, -1)
            #     elif event.key == pygame.K_s:
            #         change = (-2, 1)
            #     elif event.key == pygame.K_e:
            #         change = (2, -1)
            #     elif event.key == pygame.K_d:
            #         change = (2, 1)
            #     elif event.key == pygame.K_z:
            #         change = (-1, 2)
            #     elif event.key == pygame.K_x:
            #         change = (1, 2)
            #     self.knight.move(change[0], change[1], self.board)
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                

    def _draw_board(self) -> None:
        '''Draws the board and knight (placeholder function)'''
        self.board.draw()
        self.knight.draw(self.screen)

    def solve_with_de(self) -> None:
        self.de.run()
        print("Best fitness:", self.de.best.fitness)
        self.best_path = self.problem.decode_vector_to_moves(self.de.best.vector)
        self.knight.position = self.starting_position.copy()
        self.board.visited_positions = set()

if __name__ == "__main__":
    game = Main()
    game.solve_with_de()
    game.run()  # ← this was missing
    pygame.quit()
