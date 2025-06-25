import pygame
import random
from typing import List

from board import Board
from knight import Knight

class Main:
    def __init__(self) -> None:
        '''Initialize the main game with a board and a knight'''
        pygame.init()

        # Set up base parameters
        self.BOARD_WIDTH: int = 20
        self.BOARD_HEIGHT: int = 20
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

        self.board: Board = Board(self.screen, self.BOARD_WIDTH, self.BOARD_HEIGHT)
        self.knight: Knight = Knight(self.starting_position, self.BOARD_WIDTH, self.BOARD_HEIGHT)

    def run(self) -> None:
        while self.running:
            self._check_events()

            self.screen.fill((255, 255, 255))
            self.board.draw_board(self.knight)

            pygame.display.flip()
            self.clock.tick(60)

    def _check_events(self) -> None:
        '''Check for events and handle them'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                # TODO: more intuitive controls
                if event.key == pygame.K_q:
                    change = (-1, -2)
                elif event.key == pygame.K_w:
                    change = (1, -2)
                elif event.key == pygame.K_a:
                    change = (-2, -1)
                elif event.key == pygame.K_s:
                    change = (-2, 1)
                elif event.key == pygame.K_e:
                    change = (2, -1)
                elif event.key == pygame.K_d:
                    change = (2, 1)
                elif event.key == pygame.K_z:
                    change = (-1, 2)
                elif event.key == pygame.K_x:
                    change = (1, 2)
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                self.knight.move(change[0], change[1], self.board)

    def _draw_board(self) -> None:
        '''Draws the board and knight (placeholder function)'''
        self.board.draw()
        self.knight.draw(self.screen)

if __name__ == "__main__":
    game = Main()
    game.run()
    pygame.quit()
